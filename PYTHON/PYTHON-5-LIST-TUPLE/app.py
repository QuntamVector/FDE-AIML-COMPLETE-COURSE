
import streamlit as st
from datetime import datetime

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="Python ATM",
    page_icon="🏦",
    layout="centered"
)

# -------------------------------
# Initialize application state
# -------------------------------
if "balance" not in st.session_state:
    st.session_state.balance = 10000

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "history" not in st.session_state:
    st.session_state.history = []

CORRECT_PIN = "1234"
MAX_ATTEMPTS = 3


# -------------------------------
# Helper function
# -------------------------------
def add_transaction(transaction_type, amount):
    """Store a successful transaction."""

    transaction = {
        "type": transaction_type,
        "amount": amount,
        "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    }

    st.session_state.history.insert(0, transaction)


# -------------------------------
# Login screen
# -------------------------------
def login_screen():
    st.title("🏦 Python ATM")
    st.write("Welcome! Please verify your PIN.")

    with st.form("login_form"):
        entered_pin = st.text_input(
            "Enter your PIN",
            type="password",
            max_chars=4
        )

        submitted = st.form_submit_button(
            "Login",
            use_container_width=True
        )

    if submitted:
        if entered_pin == CORRECT_PIN:
            st.session_state.logged_in = True
            st.session_state.attempts = 0
            st.rerun()

        else:
            st.session_state.attempts += 1

            remaining = (
                MAX_ATTEMPTS - st.session_state.attempts
            )

            if remaining > 0:
                st.error(
                    f"Incorrect PIN. {remaining} attempts remaining."
                )
            else:
                st.error(
                    "Maximum attempts reached. "
                    "Please restart the demo."
                )

    if st.session_state.attempts >= MAX_ATTEMPTS:
        st.warning("Login is disabled for this demo session.")


# -------------------------------
# Dashboard
# -------------------------------
def dashboard():
    st.title("🏦 ATM Dashboard")

    st.success("Login successful!")

    # Balance display
    st.metric(
        label="Available Balance",
        value=f"₹{st.session_state.balance:,.2f}"
    )

    st.divider()

    # Transaction menu
    tab1, tab2, tab3, tab4 = st.tabs([
        "💰 Balance",
        "💸 Withdraw",
        "➕ Deposit",
        "📜 History"
    ])

    # ---------------------------
    # Balance inquiry
    # ---------------------------
    with tab1:
        st.subheader("Account Balance")

        st.write(
            f"Your current balance is "
            f"₹{st.session_state.balance:,.2f}"
        )

    # ---------------------------
    # Withdrawal
    # ---------------------------
    with tab2:
        st.subheader("Withdraw Money")

        amount = st.number_input(
            "Enter withdrawal amount (₹)",
            min_value=1,
            max_value=100000,
            value=1000,
            step=500,
            key="withdraw_amount"
        )

        if st.button(
            "Withdraw",
            use_container_width=True
        ):
            if amount <= st.session_state.balance:

                # Update account balance
                st.session_state.balance -= amount

                # Record transaction
                add_transaction("Withdrawal", amount)

                st.success(
                    f"Please collect ₹{amount:,.2f}"
                )

                st.rerun()

            else:
                st.error("Insufficient balance!")

    # ---------------------------
    # Deposit
    # ---------------------------
    with tab3:
        st.subheader("Deposit Money")

        amount = st.number_input(
            "Enter deposit amount (₹)",
            min_value=1,
            max_value=100000,
            value=1000,
            step=500,
            key="deposit_amount"
        )

        if st.button(
            "Deposit",
            use_container_width=True
        ):
            st.session_state.balance += amount

            add_transaction("Deposit", amount)

            st.success(
                f"₹{amount:,.2f} deposited successfully!"
            )

            st.rerun()

    # ---------------------------
    # Transaction history
    # ---------------------------
    with tab4:
        st.subheader("Transaction History")

        if not st.session_state.history:
            st.info("No transactions yet.")

        else:
            for transaction in st.session_state.history:

                if transaction["type"] == "Withdrawal":
                    icon = "🔴"
                    sign = "-"

                else:
                    icon = "🟢"
                    sign = "+"

                st.write(
                    f"{icon} {transaction['type']} | "
                    f"{sign}₹{transaction['amount']:,.2f}"
                )

                st.caption(transaction["time"])

                st.divider()

    # ---------------------------
    # Logout
    # ---------------------------
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.sidebar.write("Demo PIN: 1234")


# -------------------------------
# Main application
# -------------------------------
if st.session_state.logged_in:
    dashboard()

else:
    login_screen()