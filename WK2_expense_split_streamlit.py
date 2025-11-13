import streamlit as st

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="💰 Expense Splitter",
    page_icon="💸",
    layout="centered"
)

st.title("💰 Expense Splitter")
st.write("Easily calculate who owes or gets back money after a shared expense!")

# -------------------------------------------------
# Inputs
# -------------------------------------------------
total_expense = st.number_input("Enter the total expense (₹):", min_value=0.0, step=100.0)
num_people = st.number_input("Enter the number of people:", min_value=1, step=1)

# -------------------------------------------------
# Optional individual inputs
# -------------------------------------------------
if num_people > 0:
    st.subheader("🧍 Enter details (optional):")

    names = []
    contributions = []

    for i in range(int(num_people)):
        col1, col2 = st.columns([2, 1])
        with col1:
            name = st.text_input(f"Name of Person {i+1}", key=f"name_{i}", placeholder=f"Person {i+1}")
        with col2:
            contribution = st.number_input(f"Contribution ₹", key=f"contri_{i}", min_value=0.0, step=10.0)

        if not name.strip():
            name = f"Person {i+1}"
        names.append(name)
        contributions.append(contribution)

# -------------------------------------------------
# Calculation
# -------------------------------------------------
if st.button("💡 Calculate Settlement"):
    if total_expense == 0:
        total_expense = sum(contributions)

    if total_expense == 0:
        st.warning("⚠️ Please enter total expense or at least one contribution.")
    else:
        equal_share = total_expense / num_people
        st.write(f"### 🧾 Each person should pay: ₹{equal_share:.2f}")

        results = []
        for i in range(int(num_people)):
            balance = contributions[i] - equal_share
            results.append((names[i], balance))

        st.subheader("📊 Settlement Summary")

        for name, balance in results:
            if balance > 0:
                st.success(f"✅ {name} should get back ₹{abs(balance):.2f}")
            elif balance < 0:
                st.error(f"💰 {name} owes ₹{abs(balance):.2f}")
            else:
                st.info(f"👌 {name} is settled up!")

        # Show table
        st.subheader("📃 Detailed Breakdown")
        st.dataframe({
            "Name": names,
            "Contribution (₹)": contributions,
            "Net Balance (₹)": [round(c - equal_share, 2) for c in contributions],
        })

        st.balloons()
