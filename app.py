import streamlit as st
import pandas as pd
from modules.game_logic import generate_question, check_answer
from modules.scoring import start_timer, calculate_score
from modules.memory import UserProgress
from modules.speech_output import speak_text
from modules.quiz_engine import get_question
import altair as alt

CATEGORY_IDS = {
    "General Knowledge": 9,
    "Books": 10,
    "Film": 11,
    "Music": 12,
    "Science": 17,
    "Sports": 21,
    "History": 23,
    "Politics": 24,
    "Art": 25,
    "Celebrities": 26,
    "Animals": 27,
    "Vehicles": 28,
    "AI & Tech": 18  # We'll map this to Science: Computers
}

# --------------------
# Page Configuration
# --------------------
st.set_page_config(
    page_title="🧠 ThinkIt – AI Trivia Game",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --------------------
# Initialize Session State
# --------------------
if 'question_data' not in st.session_state:
    st.session_state.question_data = None

if 'start_time' not in st.session_state:
    st.session_state.start_time = None

if 'progress' not in st.session_state:
    st.session_state.progress = UserProgress()

# --------------------
# Sidebar – Avatar & Settings
# --------------------
with st.sidebar:
    st.image("assets/avatar.png", width=120)  # Avatar
    st.markdown("👋 Welcome to **ThinkIt!**")
    st.caption("An AI-powered trivia game. Test your skills, beat the timer, and challenge yourself across topics.")

st.header("🕹️ Game Settings")
category_display = st.selectbox(
    "Select a category",
    list(CATEGORY_IDS.keys())
)
difficulty = st.selectbox("Select difficulty", ["Easy", "Medium", "Hard"])

if st.button("🎯 Start New Question"):
    category_id = CATEGORY_IDS.get(category_display)
    st.session_state.question_data = generate_question(category_id, difficulty)

    # ✅ Check for errors or empty response
    if not st.session_state.question_data or "error" in st.session_state.question_data:
        error_msg = st.session_state.question_data.get(
            "error", f"Error generating question for {category_id} [{difficulty}]"
        )
        st.error(error_msg)
        speak_text(error_msg)
        st.stop()

    # ✅ Only start timer if question is valid
    st.session_state.start_time = start_timer()

# --------------------
# Main Area – Trivia Game
# --------------------
st.title("🧠 ThinkIt – AI Trivia Game")

if st.session_state.question_data:
    question = st.session_state.question_data["question"]
    options = st.session_state.question_data["options"]
    correct_answer = st.session_state.question_data["answer"]

    st.subheader("❓ Question")
    st.write(question)
    speak_text(question)  # Voice output

    user_answer = st.radio("Choose your answer:", options, key="user_choice")

    if st.button("✅ Submit Answer"):
        end_time = start_timer()
        time_taken = end_time - st.session_state.start_time
        score = calculate_score(user_answer, correct_answer, time_taken)

        result_text = check_answer(user_answer, correct_answer)
        st.success(result_text)
        speak_text(result_text)

        st.write(f"⏱️ Time Taken: `{round(time_taken, 2)}s`")
        st.write(f"🏆 Score: `{score}` points")

        st.session_state.progress.add_entry({
    "question": question,
    "user_answer": user_answer,
    "correct_answer": correct_answer,
    "score": score,
    "correct": result_text is True  # Ensure it's a boolean
})

        # Clear question after answer is submitted
        st.session_state.question_data = None

# --------------------
# Score History Chart
# --------------------
with st.expander("📈 Score Chart"):
    if st.session_state.progress.entries:
        df = pd.DataFrame(st.session_state.progress.entries)
        df['Question #'] = [f"Q{i+1}" for i in range(len(df))]

        # Ensure 'correct' column exists and use it to assign color
        if 'correct' in df.columns:
            df['Color'] = df['correct'].apply(lambda x: 'green' if x else 'orange')
        else:
            df['Color'] = 'gray'

        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Question #:O', title="Question"),
            y=alt.Y('score:Q', title="Score"),
            color=alt.Color('Color:N', scale=None, legend=None)
        ).properties(title="Score by Question")

        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No questions attempted yet.")

# --------------------
# Footer
# --------------------
st.markdown("---")
st.markdown("Made with ❤️ using LangChain, Streamlit & Open Source Tools | [GitHub](https://github.com/nabilshajahan3110/ThinkIt)")
