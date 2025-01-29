import streamlit as st
import openai

# Replace with your OpenAI API key
openai.api_key = ""

def generate_response(prompt):
    """Generates a response from ChatGPT based on the user prompt."""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a friendly and motivational gym assistant. Help users create and track workout plans while offering encouragement and fitness tips."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Streamlit App Setup
st.set_page_config(page_title="Gym Assistant", layout="centered")

st.title("🏋️ Gym Assistant")
st.markdown(
    "Welcome to your Gym Assistant! This app helps you plan workouts, track progress, and stay motivated."
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar for Workout Details
st.sidebar.header("📋 Workout Tracker")
st.sidebar.markdown("Track your progress during workouts.")
exercise = st.sidebar.text_input("Exercise Name", placeholder="e.g., Bench Press")
sets = st.sidebar.number_input("Number of Sets", min_value=1, step=1)
reps = st.sidebar.number_input("Reps per Set", min_value=1, step=1)
weight = st.sidebar.number_input("Weight (lbs)", min_value=0.0, step=0.5)

if st.sidebar.button("Add to Workout Log"):
    if exercise and sets > 0 and reps > 0:
        st.session_state.chat_history.append(("assistant", f"Logged: {sets} sets of {reps} reps at {weight} lbs for {exercise}."))
    else:
        st.sidebar.error("Please fill out all fields correctly.")

# Chat Interface
chat_container = st.container()
user_input = st.text_input("Ask me anything about fitness or workouts:", placeholder="e.g., Suggest a chest and back workout")

if user_input.strip() and st.button("Send"):
    st.session_state.chat_history.append(("user", user_input))
    bot_response = generate_response(user_input)
    st.session_state.chat_history.append(("assistant", bot_response))

for entry in st.session_state.chat_history:
    role, message = entry
    if role == "user":
        chat_container.markdown(f"**You:** {message}")
    else:
        chat_container.markdown(f"**Gym Assistant:** {message}")

# Styling
st.markdown(
    """
    <style>
    div.stTextInput > div > input {
        border-radius: 8px;
        padding: 10px;
        border: 1px solid #ccc;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    div.stButton > button {
        padding: 10px 20px;
        border-radius: 8px;
        background-color: #007BFF;
        color: white;
        border: none;
        cursor: pointer;
    }
    div.stButton > button:hover {
        background-color: #0056b3;
    }
    div.sidebar .stTextInput, div.sidebar .stNumberInput {
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)