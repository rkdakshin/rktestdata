import streamlit as st

st.title("🧮 BMI Calculator")

# Input fields
height = st.number_input("Enter your height (cm)", min_value=50.0, max_value=250.0, step=0.1)
weight = st.number_input("Enter your weight (kg)", min_value=5.0, max_value=300.0, step=0.1)

# Calculate BMI when both values are entered
if height > 0 and weight > 0:
    height_m = height / 100  # convert cm to meters
    bmi = weight / (height_m ** 2)

    st.subheader(f"Your BMI: **{bmi:.2f}**")

    # Determine category
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    st.success(f"Category: **{category}**")

else:
    st.info("Please enter height and weight to calculate BMI.")
