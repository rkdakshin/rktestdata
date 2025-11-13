import streamlit as st

# -------------------------------
# Page setup
# -------------------------------
st.set_page_config(
    page_title="Greeting App 🎉",
    page_icon="😊",
    layout="centered"
)

# -------------------------------
# Custom scrollable section (mouse drag enabled)
# -------------------------------
st.markdown("""
    <style>
    .scrollable-box {
        height: 300px;                /* Visible height */
        overflow-y: auto;             /* Enable vertical scrollbar */
        border: 2px solid #ccc;
        border-radius: 12px;
        padding: 20px;
        background-color: #f8f9fa;
        scrollbar-width: thin;        /* For Firefox */
    }

    /* Customize scrollbar for WebKit browsers (Chrome, Edge, Safari) */
    .scrollable-box::-webkit-scrollbar {
        width: 8px;
    }
    .scrollable-box::-webkit-scrollbar-thumb {
        background-color: #aaa;
        border-radius: 10px;
    }
    .scrollable-box::-webkit-scrollbar-thumb:hover {
        background-color: #666;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# Main UI
# -------------------------------
st.title("🎉 Interactive Greeting App")
st.write("👇 Scroll using your mouse or drag the scrollbar to explore!")

# Scrollable container content
scrollable_content = """
<div class="scrollable-box">
    <p style="font-size:16px; line-height:1.6;">
    Welcome! This is a small Streamlit demo that lets you scroll smoothly using your mouse
    and drag the scrollbar just like in a normal web page.
    <br><br>
    Enter your name and age below, and get a friendly personalized greeting 🎈
    <br><br>
    Keep scrolling — more space below ⬇️⬇️⬇️
    <br><br><br><br>
    </p>
</div>
"""

st.markdown(scrollable_content, unsafe_allow_html=True)

# -------------------------------
# Input section
# -------------------------------
st.subheader("💬 Tell us about yourself")

name = st.text_input("Your Name:")
age = st.slider("Your Age:", min_value=1, max_value=120, value=25)

if st.button("Say Hello 👋"):
    if not name.strip():
        st.warning("Please enter your name.")
    else:
        st.success(f"Hello **{name}**! 🎂 You are **{age}** years young!")
        st.balloons()
