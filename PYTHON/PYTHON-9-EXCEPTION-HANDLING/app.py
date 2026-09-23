import streamlit as st

st.set_page_config(
    page_title="Safe Calculator",
    page_icon="🧮",
    layout="centered"
)

st.title("🧮 Safe Calculator")

# Initialize result in session state
if "result" not in st.session_state:
    st.session_state.result = None


# -------------------------------
# Calculator UI
# -------------------------------

a = st.number_input(
    "First number:",
    value=0.0,
    format="%.2f"
)

b = st.number_input(
    "Second number:",
    value=0.0,
    format="%.2f"
)

op = st.selectbox(
    "Operations:",
    ["+", "-", "*", "/"]
)


# -------------------------------
# Calculate
# -------------------------------

if st.button("Calculate 🧮"):

    try:
        # Same backend logic
        if op == "+":
            result = a + b

        elif op == "-":
            result = a - b

        elif op == "*":
            result = a * b

        elif op == "/":
            result = a / b

        else:
            st.error(
                "❌ Invalid operator. USE ONLY OPERATION (+,-,*,/)"
            )

        st.session_state.result = result

        st.success(
            f"✅ Result: {a} {op} {b} = {result}"
        )

    except ValueError:
        st.error(
            "❌ Please enter number only..."
        )

    except ZeroDivisionError:
        st.error(
            "❌ You cannot divide by zero..."
        )

    except Exception as e:
        st.error(
            f"❌ Unexpected error: {e}"
        )

    finally:
        st.info(
            "Calculation attempt is completed"
        )


# -------------------------------
# Result
# -------------------------------

if st.session_state.result is not None:

    st.divider()

    st.subheader("📊 Calculation Result")

    st.metric(
        label="Result",
        value=st.session_state.result
    )


# -------------------------------
# Calculate Again
# -------------------------------

st.divider()

again = st.radio(
    "Do you want to calculate again?",
    ["yes", "no"],
    horizontal=True
)

if again == "no":
    st.success("👋🏻 Good Bye...")