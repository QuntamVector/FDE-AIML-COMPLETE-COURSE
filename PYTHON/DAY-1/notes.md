# FDE — Forward Deployed Engineer

## 1. What is an FDE?

**FDE stands for Forward Deployed Engineer.**

An FDE is an engineer who works closely with customers to understand their real-world technical and business problems and builds practical solutions for those problems.

A traditional software engineer may primarily work on features defined by a product team.

An FDE goes one step closer to the customer:

```text
Customer Problem
       ↓
Understand the Problem
       ↓
Technical Discovery
       ↓
Design the Solution
       ↓
Build a Prototype
       ↓
Deploy the Solution
       ↓
Collect Customer Feedback
       ↓
Improve the Solution
```

### Simple Definition

> **An FDE is an engineer who combines software engineering, problem-solving, customer interaction, and production engineering to deliver solutions for real customer problems.**

---

# 2. Why is the FDE Role Important?

Many companies have customers who know **what problem they have**, but they don't necessarily know **how to technically solve it**.

For example:

> "Our employees spend hours searching company documents."

The customer knows the problem.

The FDE needs to figure out:

* What data exists?
* Where is the data stored?
* Who needs access?
* What type of answers are required?
* Should we use RAG?
* Which LLM should we use?
* How do we evaluate the answers?
* How do we deploy it?
* How do we scale it?
* How do we monitor it?

Therefore, an FDE converts:

```text
Business Problem
       ↓
Technical Problem
       ↓
Engineering Solution
       ↓
Production System
```

---

# 3. FDE vs Software Engineer

| Software Engineer                       | FDE                                        |
| --------------------------------------- | ------------------------------------------ |
| Primarily builds software/products      | Builds solutions for customer problems     |
| Usually works from defined requirements | Often discovers requirements directly      |
| Product-focused                         | Customer + solution-focused                |
| May work on one component               | Often works across multiple technologies   |
| Less customer interaction               | High customer interaction                  |
| Focuses on implementation               | Focuses on problem → solution → deployment |

An FDE is **not simply a developer**.

An FDE may need to understand:

* Software development
* Cloud
* DevOps
* AI/GenAI
* Databases
* APIs
* Security
* Monitoring
* Customer requirements
* Business workflows

---

# 4. The FDE Mindset

The most important skill for an FDE is **problem-solving**.

Do not start with:

> "Which technology should I use?"

Start with:

> "What problem are we trying to solve?"

For example:

### Customer says:

> "We need an AI chatbot."

An inexperienced engineer may immediately start building a chatbot.

An FDE asks:

### Business Questions

* Who will use the chatbot?
* What problem will it solve?
* How often does this problem occur?
* How much time is currently being spent?
* What does success look like?

### Technical Questions

* What data does the chatbot need?
* Where is the data stored?
* Are APIs available?
* How frequently does the data change?
* What security restrictions exist?
* What systems need to be integrated?

### AI Questions

* Do we need RAG?
* Do we need an agent?
* Which LLM should we use?
* How will we evaluate responses?
* How do we handle hallucinations?

The FDE first **understands the problem**, then chooses the technology.

---

# 5. FDE Problem-Solving Lifecycle

A typical FDE workflow can be represented as:

```text
                    Customer
                       ↓
                Problem Discovery
                       ↓
              Requirement Gathering
                       ↓
               Technical Discovery
                       ↓
                  Architecture
                       ↓
                   Prototype
                       ↓
                 Implementation
                       ↓
                Testing & Evaluation
                       ↓
                   Deployment
                       ↓
                 Monitoring
                       ↓
              Customer Feedback
                       ↓
                  Improvement
```

This cycle may repeat multiple times.

---

# 6. Important FDE Skills

An FDE generally needs skills in five major areas.

## 6.1 Software Engineering

Important skills:

* Python
* APIs
* Git
* Databases
* REST APIs
* Backend development
* Testing
* Debugging

---

## 6.2 GenAI / AI Engineering

Important skills:

* LLMs
* Prompt engineering
* Embeddings
* RAG
* Vector databases
* Agents
* Tool calling
* Structured outputs
* MCP
* AI evaluation

---

## 6.3 Cloud & DevOps

Important skills:

* AWS
* Docker
* Kubernetes
* CI/CD
* Infrastructure
* Networking
* Security
* Monitoring

---

## 6.4 Customer Engineering

An FDE should know how to:

* Ask the right questions
* Understand customer workflows
* Explain technical concepts
* Conduct technical discussions
* Build demos
* Debug customer problems
* Present solutions

---

## 6.5 Product Thinking

An FDE should understand:

> "Can we build this?"

but also:

> "Should we build this?"

The best technical solution is not always the best business solution.

---

# 7. Core FDE Technology Stack

For this learning journey, we will focus on:

```text
Python
   ↓
GenAI / LLM
   ↓
LLM Evaluation
   ↓
AWS
   ↓
Docker
   ↓
Kubernetes
```

Each technology should be learned by solving a **real customer problem**.

---

# 8. Problem Statement 1 — Enterprise Knowledge AI Assistant

## Customer Problem

A company has thousands of:

* PDFs
* SOPs
* Policies
* Technical documents
* Internal guides
* Knowledge-base articles

Employees spend a lot of time searching through these documents.

### Customer Requirement

> "Build an AI assistant that allows employees to ask questions about company documents and receive accurate answers."

---

## FDE Approach

First understand:

* What documents exist?
* Who can access them?
* How frequently are documents updated?
* What type of questions will users ask?
* Should answers contain citations?
* What happens when information is unavailable?

---

## Technical Solution

```text
Company Documents
        ↓
Document Processing
        ↓
Chunking
        ↓
Embeddings
        ↓
Vector Database
        ↓
Retriever
        ↓
LLM
        ↓
Answer
```

### Technologies

* Python
* LLM
* RAG
* Embeddings
* Vector Database
* LLM Evaluation
* Docker
* Kubernetes
* AWS

---

# 9. Problem Statement 2 — AI Customer Support Agent

## Customer Problem

A company receives thousands of customer support questions.

Many questions are repetitive:

* Where is my order?
* How can I reset my password?
* What is your refund policy?
* How do I cancel my subscription?

Customer support employees spend significant time answering these questions.

### Customer Requirement

> "Build an AI support agent that can answer questions and interact with internal systems."

---

## Solution

```text
Customer
   ↓
Chat Interface
   ↓
AI Agent
   ├── Knowledge Base
   ├── Order API
   ├── Ticket API
   └── Human Escalation
```

The AI should not only generate text.

It may need to **use tools**.

For example:

```text
User:
"Where is my order?"

        ↓

LLM Agent

        ↓

Order API

        ↓

Order Status

        ↓

LLM

        ↓

Customer Response
```

### Technologies

* Python
* LLM
* GenAI
* RAG
* Agents
* Tool Calling
* APIs
* LLM Evaluation
* Docker
* Kubernetes
* AWS

---

# 10. Problem Statement 3 — AI SRE / DevOps Assistant

## Customer Problem

A company's application is running on Kubernetes.

When something goes wrong, engineers manually investigate:

* Pod logs
* Kubernetes events
* Metrics
* Application errors
* Deployment history

This can take hours.

### Customer Requirement

> "Build an AI assistant that helps engineers investigate production incidents."

---

## Example

Engineer asks:

> "Why did my application restart multiple times?"

The system investigates:

```text
Kubernetes
    ↓
Pod Status
    ↓
Events
    ↓
Logs
    ↓
Metrics
    ↓
AI Analysis
    ↓
Root Cause
```

Possible response:

> "The container was repeatedly terminated because it exceeded its configured memory limit."

The AI assistant should provide:

* Possible root cause
* Evidence
* Relevant logs
* Recommended investigation steps

---

## Technologies

* Python
* LLM
* AI Agents
* Kubernetes API
* AWS
* Docker
* Monitoring
* Logs
* LLM Evaluation

This is an excellent example of combining:

**DevOps + Kubernetes + GenAI.**

---

# 11. Problem Statement 4 — AI SQL/Data Analyst

## Customer Problem

Business users depend on engineers to get answers from databases.

For example:

> "What were our top 10 products last month?"

Instead of manually writing SQL, users can ask questions in natural language.

---

## Architecture

```text
User Question
      ↓
LLM
      ↓
SQL Generation
      ↓
SQL Validation
      ↓
Database
      ↓
Query Result
      ↓
LLM
      ↓
Business Answer
```

### Example

User:

> "Show me the top 5 products by revenue."

AI generates SQL.

The SQL is validated.

The query runs against the database.

The result is converted into a human-readable answer.

---

## FDE Challenges

The FDE must consider:

* SQL correctness
* Database permissions
* Read-only access
* Data privacy
* SQL injection
* Hallucinations
* Query performance
* Evaluation

### Technologies

* Python
* LLM
* SQL
* GenAI
* Database
* Agents
* LLM Evaluation
* Docker
* AWS
* Kubernetes

---

# 12. Problem Statement 5 — AI Document Processing

## Customer Problem

A company receives thousands of invoices and contracts.

Employees manually extract information from them.

### Customer Requirement

> "Automatically extract important information from documents."

---

## Architecture

```text
Document
   ↓
Upload
   ↓
Document Processing
   ↓
LLM
   ↓
Structured Output
   ↓
Validation
   ↓
Database
```

Example output:

```json
{
  "invoice_number": "INV-1023",
  "vendor": "ABC Technologies",
  "amount": 125000,
  "currency": "INR"
}
```

### Technologies

* Python
* LLM
* GenAI
* Structured Output
* Pydantic
* LLM Evaluation
* AWS S3
* Docker
* Kubernetes

---

# 13. Problem Statement 6 — AWS Cloud Cost Optimization Assistant

## Customer Problem

A company is spending too much money on AWS.

The engineering team doesn't know which resources are unnecessary.

### Customer Requirement

> "Build an AI assistant that analyzes AWS resources and provides cost optimization recommendations."

---

## Architecture

```text
AWS
 ↓
Cost / Resource Data
 ↓
Python
 ↓
Analysis
 ↓
LLM
 ↓
Recommendations
```

Example:

> "There are unused resources that may be contributing to unnecessary monthly cost."

The initial version should be **read-only**.

The AI can recommend actions, but it should not automatically delete production resources.

---

# 14. Why Python?

Python is one of the most useful languages for FDE and AI engineering.

We can use Python for:

* APIs
* Automation
* AWS SDK
* Data processing
* LLM applications
* RAG
* Agents
* Testing
* Backend services

Example:

```text
Customer Problem
       ↓
Python Application
       ↓
LLM / API / AWS / Database
       ↓
Production Solution
```

---

# 15. Why GenAI?

Traditional software follows predefined logic.

GenAI allows applications to work with:

* Natural language
* Documents
* Unstructured data
* Complex user requests
* Reasoning tasks
* Knowledge retrieval

For example:

Traditional application:

```text
Input → Fixed Rules → Output
```

GenAI application:

```text
User Question
      ↓
LLM
      ↓
Context / Tools / Knowledge
      ↓
Generated Response
```

---

# 16. Why LLM Evaluation?

Building an AI application is not enough.

We need to determine:

> **"Is the AI actually giving good answers?"**

Traditional software often uses:

```text
Input
  ↓
Expected Output
  ↓
Pass / Fail
```

LLM applications are more complex.

We need to evaluate things such as:

* Correctness
* Relevance
* Faithfulness
* Context relevance
* Hallucination
* Toxicity
* Latency
* Cost

Example:

### Question

> "What is the company's refund policy?"

### Expected answer

The answer should come from the company's actual policy.

If the LLM invents a policy:

**Hallucination ❌**

Therefore:

```text
AI Application
      ↓
Evaluation Dataset
      ↓
LLM Evaluation
      ↓
Quality Measurement
      ↓
Improvement
```

Evaluation becomes extremely important when moving from **prototype → production**.

---

# 17. Why AWS?

Customer solutions usually need to run in a reliable cloud environment.

AWS provides services for:

* Compute
* Storage
* Databases
* Networking
* Security
* Monitoring
* AI workloads

The FDE should understand how to deploy and operate applications in AWS.

---

# 18. Why Docker?

During development, an application may work on one developer's laptop but fail in another environment.

Docker packages the application and its dependencies into a container.

```text
Application
+
Dependencies
+
Runtime
       ↓
    Docker Image
       ↓
    Container
```

Benefits:

* Consistent environments
* Easier deployment
* Reproducibility
* Portability

---

# 19. Why Kubernetes?

Suppose our AI application becomes popular.

We may have:

```text
1 user
 ↓
1 container
```

But in production:

```text
10,000 users
      ↓
Multiple containers
      ↓
Load balancing
      ↓
Scaling
      ↓
High availability
```

Kubernetes helps manage containerized applications.

Important Kubernetes concepts for FDE:

* Pods
* Deployments
* Services
* ConfigMaps
* Secrets
* Ingress
* Scaling
* Health checks
* Resource limits
* Rolling deployments

---

# 20. Prototype → Production

One of the most important FDE concepts is understanding the difference between a prototype and a production solution.

### Prototype

```text
Python
 ↓
LLM
 ↓
Simple UI
```

Good for demonstrating an idea.

### Production

```text
                 Users
                   ↓
             Load Balancer
                   ↓
              Kubernetes
                   ↓
             AI Application
              ↙         ↘
           LLM          APIs
            ↓
        Vector DB
            ↓
           Data
                   ↓
              Monitoring
```

Production also requires:

* Authentication
* Authorization
* Security
* Logging
* Monitoring
* Scaling
* Reliability
* Cost management
* Evaluation
* Error handling

---

# 21. FDE Technology Journey

The learning journey can be structured as:

```text
                  FDE
                   │
                   ↓
             Customer Problem
                   │
                   ↓
             Problem Discovery
                   │
                   ↓
              Python / APIs
                   │
                   ↓
              GenAI / LLM
                   │
                   ↓
            RAG / Agents / Tools
                   │
                   ↓
             LLM Evaluation
                   │
                   ↓
                 Docker
                   │
                   ↓
                  AWS
                   │
                   ↓
              Kubernetes
                   │
                   ↓
              Production
                   │
                   ↓
            Customer Solution
```

---

# 22. Recommended FDE Project Roadmap

## Project 1 — Enterprise Knowledge Assistant

Learn:

```text
Python
LLM
RAG
Vector Database
Evaluation
```

---

## Project 2 — AI Customer Support Agent

Learn:

```text
Python
LLM
Agents
Tools
APIs
RAG
Evaluation
```

---

## Project 3 — AI SRE Assistant

Learn:

```text
Python
LLM
Agents
AWS
Docker
Kubernetes
Logs
Monitoring
Evaluation
```

---

## Project 4 — AI Data Analyst

Learn:

```text
Python
LLM
SQL
Agents
Database
Evaluation
Docker
AWS
```

---

## Project 5 — Production AI Platform

Learn:

```text
Docker
AWS
Kubernetes
CI/CD
Security
Scaling
Monitoring
LLM Evaluation
```

---

# 23. Final FDE Capstone Project

For the final project, students should receive **only a customer problem statement**.

They should decide:

* What questions to ask?
* What requirements are needed?
* What architecture should be used?
* Which LLM?
* Whether RAG is required?
* Whether agents are required?
* How should the application be evaluated?
* How should it be containerized?
* How should it be deployed to AWS?
* How should Kubernetes be used?
* How should the application be monitored?

The final workflow:

```text
Customer Requirement
        ↓
Discovery
        ↓
Requirement Analysis
        ↓
Architecture
        ↓
Technology Selection
        ↓
Prototype
        ↓
GenAI Application
        ↓
LLM Evaluation
        ↓
Docker
        ↓
AWS
        ↓
Kubernetes
        ↓
Monitoring
        ↓
Customer Demo
```

---

# 24. Most Important FDE Principle

Remember:

> **FDE is not about knowing every technology.**

It is about knowing how to:

```text
Understand
    ↓
Analyze
    ↓
Design
    ↓
Build
    ↓
Deploy
    ↓
Debug
    ↓
Measure
    ↓
Improve
```

The technology is only the **tool**.

The actual skill is:

> **Taking an ambiguous customer problem and turning it into a working production solution.**

---

# 25. FDE Skill Formula

A strong FDE can be thought of as:

```text
              FDE
               =
    Engineering Skills
          +
       GenAI Skills
          +
      Cloud Skills
          +
     DevOps Skills
          +
   Problem Solving
          +
 Customer Communication
          +
    Product Thinking
```

### Final takeaway

> **Don't learn FDE by memorizing tools. Learn FDE by solving customer problems using the right tools.**

**Problem first. Technology second. Customer outcome always.**
