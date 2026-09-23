import streamlit as st

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Quantam Vector Restaurant",
    page_icon="🍽️",
    layout="centered"
)


# --------------------------------------------------
# MENU
# --------------------------------------------------

menu = {
    "chicken_biryani": 220,
    "veg_biryani": 200,
    "cold_coffee": 100,
    "garlic_nan": 150
}


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "order" not in st.session_state:
    st.session_state.order = []

if "customers" not in st.session_state:
    st.session_state.customers = set()

if "sales" not in st.session_state:
    st.session_state.sales = {}

if "customer" not in st.session_state:
    st.session_state.customer = ""


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🍽️ Quantam Vector Restaurant")
st.subheader("Restaurant Management System")


# --------------------------------------------------
# CUSTOMER
# --------------------------------------------------

customer = st.text_input(
    "Enter Customer Name",
    value=st.session_state.customer
)

if customer:
    customer = customer.strip().title()
    st.session_state.customer = customer
    st.session_state.customers.add(customer)


# --------------------------------------------------
# MENU
# --------------------------------------------------

st.divider()

st.header("📋 Menu")


for item, price in menu.items():

    display_name = item.replace("_", " ").title()

    st.write(
        f"**{display_name}** — ₹{price}"
    )


# --------------------------------------------------
# ORDER
# --------------------------------------------------

st.divider()

st.header("🛒 Place Your Order")


selected_item = st.selectbox(
    "Select an item",
    options=list(menu.keys()),
    format_func=lambda item: item.replace("_", " ").title()
)


quantity = st.number_input(
    "Quantity",
    min_value=1,
    max_value=20,
    value=1
)


if st.button("➕ Add to Order"):

    if not customer:

        st.warning("Please enter customer name first.")

    else:

        # Add item multiple times based on quantity
        for _ in range(quantity):
            st.session_state.order.append(selected_item)

            # Count sales
            if selected_item in st.session_state.sales:
                st.session_state.sales[selected_item] += 1
            else:
                st.session_state.sales[selected_item] = 1

        display_name = selected_item.replace("_", " ").title()

        st.success(
            f"{quantity} x {display_name} added to your order!"
        )


# --------------------------------------------------
# CURRENT ORDER
# --------------------------------------------------

st.divider()

st.header("🧾 Current Order")


if not st.session_state.order:

    st.info("No items added yet.")

else:

    total = 0

    for item in st.session_state.order:

        price = menu[item]
        display_name = item.replace("_", " ").title()

        total += price

        st.write(
            f"{display_name} — ₹{price}"
        )

    st.markdown("---")

    st.subheader(f"💰 Total Bill: ₹{total}")


# --------------------------------------------------
# BILL
# --------------------------------------------------

if st.session_state.order:

    st.divider()

    st.header("🧾 Generate Bill")

    if st.button("Generate Bill"):

        total = 0

        st.success("Order completed successfully!")

        st.write(f"**Customer:** {st.session_state.customer}")

        st.markdown("### Ordered Items")

        for item in st.session_state.order:

            price = menu[item]
            display_name = item.replace("_", " ").title()

            st.write(
                f"- {display_name} — ₹{price}"
            )

            total += price

        st.markdown("---")

        st.subheader(f"Total Bill: ₹{total}")


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

st.divider()

st.header("📊 Restaurant Summary")


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Items Ordered",
        len(st.session_state.order)
    )

with col2:
    st.metric(
        "Unique Customers",
        len(st.session_state.customers)
    )

with col3:
    st.metric(
        "Different Items Sold",
        len(st.session_state.sales)
    )


# --------------------------------------------------
# SALES
# --------------------------------------------------

st.subheader("📈 Sales")


if st.session_state.sales:

    for item, count in st.session_state.sales.items():

        display_name = item.replace("_", " ").title()

        st.write(
            f"**{display_name}** → {count} sold"
        )

else:

    st.info("No sales recorded yet.")


# --------------------------------------------------
# BEST SELLING ITEM
# --------------------------------------------------

if st.session_state.sales:

    best_item = max(
        st.session_state.sales,
        key=st.session_state.sales.get
    )

    best_item_name = best_item.replace(
        "_", " "
    ).title()

    best_item_count = st.session_state.sales[best_item]

    st.success(
        f"🏆 Best Selling Item: "
        f"{best_item_name} "
        f"({best_item_count} sold)"
    )


# --------------------------------------------------
# CLEAR ORDER
# --------------------------------------------------

st.divider()

if st.button("🗑️ Clear Current Order"):

    st.session_state.order = []

    st.rerun()


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Thank you for visiting Quantam Vector Restaurant! 😊"
)