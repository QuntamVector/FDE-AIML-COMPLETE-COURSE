import os
import json
import boto3
import duckdb
import streamlit as st
from dotenv import load_dotenv
from typing import Annotated, TypedDict, List
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# Load environment variables from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Page Config ---
st.set_page_config(page_title="AWS S3 LangGraph Analyst", page_icon="🪣", layout="wide")
st.title("🪣 AWS S3 LangGraph Analyst & Manager Chatbot")

# --- Sidebar: AWS Credentials & Settings ---
with st.sidebar:
    st.header("🔑 AWS Configuration")
    aws_access_key = st.text_input("AWS Access Key ID", type="password", value="")
    aws_secret_key = st.text_input("AWS Secret Access Key", type="password", value="")
    aws_region = st.text_input("AWS Region", value="ap-northeast-1")
    model_name = st.selectbox("Model", ["gpt-4o", "gpt-4o-mini"], index=0)

    if OPENAI_API_KEY:
        st.success("✅ OpenAI API Key loaded from .env")
    else:
        st.error("❌ OPENAI_API_KEY missing in .env")

    st.divider()
    st.subheader("💡 Quick Sample Prompts")
    sample_prompts = [
        "Analyze all S3 buckets in my account and summarize storage usage.",
        "List all buckets in ap-northeast-1 and identify empty ones.",
        "Analyze bucket 'skillopstatichosting' and show the top 10 largest files.",
        "Create a new S3 bucket named 'my-test-bucket-2026-jp'.",
        "Delete the S3 bucket named 'my-test-bucket-2026-jp'.",
    ]
    for prompt in sample_prompts:
        if st.button(prompt, use_container_width=True):
            st.session_state["prefill_prompt"] = prompt

    st.divider()
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# --- Structured Output Schema (OpenAI Strict Schema Compatible) ---
class MetricItem(BaseModel):
    name: str = Field(description="Name of the metric or action status (e.g., total_buckets, bucket_created, object_count)")
    value: str = Field(description="Value of the metric or status as a string")


class S3AnalysisReport(BaseModel):
    scope: str = Field(description="'all_buckets', 'single_bucket', or 'bucket_management'")
    buckets_analyzed: List[str] = Field(description="List of bucket names analyzed, created, or deleted")
    summary: str = Field(description="High-level summary of findings or bucket operation performed")
    metrics: List[MetricItem] = Field(description="Key storage metrics, counts, SQL aggregations, or operation status")
    findings: List[str] = Field(description="Detailed observations, anomalies, or confirmation details")


# --- Agent State ---
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    final_json: dict


# --- Build Agent Dynamically with Sidebar AWS Credentials & .env OpenAI Key ---
def build_s3_agent(access_key: str, secret_key: str, region: str, api_key: str, model: str):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    # --- Read / Analysis Tools ---
    @tool
    def list_all_buckets() -> str:
        """List all S3 buckets in the AWS account along with creation dates and regions."""
        try:
            response = s3_client.list_buckets()
            buckets = []
            for b in response.get("Buckets", []):
                name = b["Name"]
                try:
                    loc = s3_client.get_bucket_location(Bucket=name).get("LocationConstraint") or "us-east-1"
                except Exception:
                    loc = "unknown"
                buckets.append({
                    "bucket": name,
                    "created": str(b["CreationDate"]),
                    "region": loc,
                })
            return json.dumps(buckets, indent=2)
        except Exception as e:
            return f"Error listing buckets: {str(e)}"

    @tool
    def list_s3_objects(bucket: str, prefix: str = "", max_keys: int = 100) -> str:
        """List objects (keys, sizes in bytes, last modified, storage class) in a specific S3 bucket."""
        try:
            response = s3_client.list_objects_v2(
                Bucket=bucket, Prefix=prefix, MaxKeys=max_keys
            )
            contents = response.get("Contents", [])
            if not contents:
                return json.dumps({"bucket": bucket, "prefix": prefix, "objects": []})

            objects = [
                {
                    "key": obj["Key"],
                    "size_bytes": obj["Size"],
                    "last_modified": str(obj["LastModified"]),
                    "storage_class": obj.get("StorageClass", "STANDARD"),
                }
                for obj in contents
            ]
            return json.dumps({"bucket": bucket, "count": len(objects), "objects": objects}, indent=2)
        except Exception as e:
            return f"Error listing objects in {bucket}: {str(e)}"

    @tool
    def inspect_s3_file_preview(bucket: str, key: str, num_bytes: int = 4096) -> str:
        """Read the first few KB of a CSV/JSON/text/log file from S3 to check its schema or contents."""
        try:
            response = s3_client.get_object(
                Bucket=bucket, Key=key, Range=f"bytes=0-{num_bytes - 1}"
            )
            return response["Body"].read().decode("utf-8", errors="replace")
        except Exception as e:
            return f"Error previewing s3://{bucket}/{key}: {str(e)}"

    @tool
    def query_s3_with_sql(sql_query: str) -> str:
        """
        Execute a DuckDB SQL query directly on S3 CSV, Parquet, or JSON files.
        Example: SELECT * FROM 's3://my-bucket/data.parquet' LIMIT 10;
        """
        try:
            con = duckdb.connect(database=":memory:")
            con.execute("INSTALL httpfs; LOAD httpfs;")
            con.execute(f"""
                CREATE SECRET (
                    TYPE S3,
                    KEY_ID '{access_key}',
                    SECRET '{secret_key}',
                    REGION '{region}'
                );
            """)
            df = con.execute(sql_query).df()
            return df.head(100).to_json(orient="records", date_format="iso")
        except Exception as e:
            return f"SQL Error: {str(e)}"

    # --- Bucket Management Tools (Create & Delete) ---
    @tool
    def create_s3_bucket(bucket_name: str) -> str:
        """Create a new S3 bucket in the configured AWS region (e.g., ap-northeast-1)."""
        try:
            if region == "us-east-1":
                s3_client.create_bucket(Bucket=bucket_name)
            else:
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={"LocationConstraint": region},
                )
            return json.dumps({
                "status": "created",
                "bucket": bucket_name,
                "region": region,
            })
        except Exception as e:
            return f"Error creating bucket '{bucket_name}': {str(e)}"

    @tool
    def delete_s3_bucket(bucket_name: str, force: bool = False) -> str:
        """
        Delete an S3 bucket. Set force=True only if the user explicitly asks to delete a non-empty bucket
        (which removes all objects inside before deleting the bucket).
        """
        try:
            if force:
                paginator = s3_client.get_paginator("list_objects_v2")
                for page in paginator.paginate(Bucket=bucket_name):
                    objects = [{"Key": obj["Key"]} for obj in page.get("Contents", [])]
                    if objects:
                        s3_client.delete_objects(Bucket=bucket_name, Delete={"Objects": objects})

            s3_client.delete_bucket(Bucket=bucket_name)
            return json.dumps({
                "status": "deleted",
                "bucket": bucket_name,
                "forced_empty": force,
            })
        except Exception as e:
            return f"Error deleting bucket '{bucket_name}': {str(e)}"

    analysis_tools = [list_all_buckets, list_s3_objects, inspect_s3_file_preview, query_s3_with_sql]
    mgmt_tools = [create_s3_bucket, delete_s3_bucket]
    mgmt_tool_names = {t.name for t in mgmt_tools}
    all_tools = analysis_tools + mgmt_tools

    llm = ChatOpenAI(model=model, temperature=0, api_key=api_key)
    llm_with_tools = llm.bind_tools(all_tools)
    structured_llm = llm.with_structured_output(S3AnalysisReport)

    system_prompt = f"""You are an AWS S3 Analysis & Management Agent operating primarily in region {region}.
- For ALL-bucket analysis, call `list_all_buckets` first, then inspect relevant buckets.
- For INDIVIDUAL-bucket analysis, inspect that bucket directly with `list_s3_objects`.
- For structured files (CSV, Parquet, JSON), use `inspect_s3_file_preview` and `query_s3_with_sql`.
- To create a bucket, use `create_s3_bucket`. Bucket names must be globally unique, lowercase, and DNS-compliant.
- To delete a bucket, use `delete_s3_bucket`. Only set `force=True` if the user explicitly asks to force-delete a non-empty bucket.
- Use conversation history for follow-up questions."""

    def agent_node(state: AgentState):
        messages = [SystemMessage(content=system_prompt)] + state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}

    def format_json_node(state: AgentState):
        report: S3AnalysisReport = structured_llm.invoke(state["messages"])
        return {"final_json": report.model_dump()}

    # --- Custom Router: Analysis Node vs. Bucket Management Node vs. JSON Formatter ---
    def route_tools(state: AgentState):
        last_message = state["messages"][-1]
        tool_calls = getattr(last_message, "tool_calls", None)
        if not tool_calls:
            return "format_json"
        if any(tc["name"] in mgmt_tool_names for tc in tool_calls):
            return "bucket_mgmt_tools"
        return "analysis_tools"

    workflow = StateGraph(AgentState)
    workflow.add_node("agent", agent_node)
    workflow.add_node("analysis_tools", ToolNode(analysis_tools))
    workflow.add_node("bucket_mgmt_tools", ToolNode(mgmt_tools))
    workflow.add_node("format_json", format_json_node)

    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent",
        route_tools,
        {
            "analysis_tools": "analysis_tools",
            "bucket_mgmt_tools": "bucket_mgmt_tools",
            "format_json": "format_json",
        },
    )
    workflow.add_edge("analysis_tools", "agent")
    workflow.add_edge("bucket_mgmt_tools", "agent")
    workflow.add_edge("format_json", END)

    return workflow.compile()


# --- Session State for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render existing chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant" and "json_data" in msg:
            st.markdown(msg["content"])
            with st.expander("📄 View Raw JSON Output", expanded=True):
                st.json(msg["json_data"])
        else:
            st.markdown(msg["content"])

# Handle prefilled prompt from sidebar or user chat input
user_input = st.chat_input("Ask to analyze, create, or delete S3 buckets...")
if "prefill_prompt" in st.session_state:
    user_input = st.session_state.pop("prefill_prompt")

if user_input:
    if not OPENAI_API_KEY:
        st.error("⚠️ OPENAI_API_KEY not found. Please add it to your `.env` file and restart the app.")
        st.stop()

    if not (aws_access_key and aws_secret_key):
        st.error("⚠️ Please enter your AWS Access Key ID and AWS Secret Access Key in the sidebar.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    lc_messages = []
    for m in st.session_state.messages:
        if m["role"] == "user":
            lc_messages.append(HumanMessage(content=m["content"]))
        else:
            lc_messages.append(AIMessage(content=json.dumps(m.get("json_data", m["content"]))))

    with st.chat_message("assistant"):
        with st.spinner("Executing S3 workflow..."):
            try:
                agent = build_s3_agent(
                    access_key=aws_access_key,
                    secret_key=aws_secret_key,
                    region=aws_region,
                    api_key=OPENAI_API_KEY,
                    model=model_name,
                )
                result = agent.invoke({"messages": lc_messages})
                json_report = result["final_json"]
                summary_text = json_report.get("summary", "Operation complete.")

                st.markdown(summary_text)
                with st.expander("📄 View Raw JSON Output", expanded=True):
                    st.json(json_report)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": summary_text,
                    "json_data": json_report,
                })
            except Exception as e:
                st.error(f"Agent Error: {str(e)}")