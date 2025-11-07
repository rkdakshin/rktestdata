import streamlit as st

# ---------------------------
# QUIZ DATA
# ---------------------------
quiz = [
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "Madrid", "Paris", "Rome"],
        "answer": "Paris"
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Earth", "Mars", "Jupiter", "Venus"],
        "answer": "Mars"
    },
    {
        "question": "Who wrote the play 'Romeo and Juliet'?",
        "options": ["Charles Dickens", "William Shakespeare", "Leo Tolstoy", "Mark Twain"],
        "answer": "William Shakespeare"
    },
    {
        "question": "What is the square root of 64?",
        "options": ["6", "8", "10", "12"],
        "answer": "8"
    },
    {
        "question": "Which gas do plants absorb from the atmosphere?",
        "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
        "answer": "Carbon Dioxide"
    }
]

# ---------------------------
# STREAMLIT APP
# ---------------------------
st.set_page_config(page_title="Quiz App", page_icon="🧠", layout="centered")

st.title("🧠 Multiple Choice Quiz")
st.write("Test your general knowledge! Select the correct answers below:")

# Initialize session state
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Store user answers
user_answers = {}

# Display questions
for i, q in enumerate(quiz):
    st.subheader(f"Q{i+1}. {q['question']}")
    user_answers[i] = st.radio(
        "Choose one:",
        q["options"],
        key=f"q_{i}"
    )

st.write("---")

# Submit button
if st.button("Submit Quiz"):
    st.session_state.submitted = True

# Evaluate answers
if st.session_state.submitted:
    score = 0
    st.subheader("📊 Results:")
    for i, q in enumerate(quiz):
        correct = q["answer"]
        chosen = user_answers[i]
        if chosen == correct:
            st.success(f"✅ Q{i+1}: Correct! ({chosen})")
            score += 1
        else:
            st.error(f"❌ Q{i+1}: Wrong. You chose '{chosen}', correct answer is '{correct}'.")
    st.write("---")
    st.write(f"🎯 **Your Final Score: {score} / {len(quiz)}**")
    if score == len(quiz):
        st.balloons()
    elif score >= len(quiz) * 0.7:
        st.success("Great job!")
    else:
        st.info("Keep practicing!")

