import streamlit as st
import openai

# Replace with your OpenAI API key
openai.api_key = "your_openai_api_key"

def generate_response(prompt):
    """Sends the user's message to OpenAI API and retrieves the response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a gym assistant. Help users build and track workout plans. You have the personality of Jim Halpert from the show The Office. Please make sure to add 'The Office' references and jokes in your responses."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Streamlit App
st.set_page_config(page_title="Gym Assistant", layout="centered")

st.title("🏋️ Gym Assistant")
st.markdown(
    "Welcome to your Gym Assistant! This chatbot helps you build and track your workout plans."
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
chat_container = st.container()
for entry in st.session_state.chat_history:
    role, message = entry
    if role == "user":
        chat_container.markdown(f"**You:** {message}")
    else:
        chat_container.markdown(f"**Gym Halpert:** {message}")

# User input
user_input = st.text_input("Type your message:", placeholder="e.g., Plan a workout for chest and back", key="user_input")

if st.button("Send") and user_input.strip():
    # Add user message to history
    st.session_state.chat_history.append(("user", user_input))

    # Get response from OpenAI
    bot_response = generate_response(user_input)
    st.session_state.chat_history.append(("assistant", bot_response))

    # Rerun to refresh the chat display
    user_input = ""
    st.experimental_update()

# Style
st.markdown(
    "<style>\n        div.stTextInput > div > input {\n            border-radius: 8px;\n            padding: 10px;\n            border: 1px solid #ccc;\n            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);\n        }\n        div.stButton > button {\n            padding: 10px 20px;\n            border-radius: 8px;\n            background-color: #007BFF;\n            color: white;\n            border: none;\n            cursor: pointer;\n        }\n        div.stButton > button:hover {\n            background-color: #0056b3;\n        }\n    </style>",
    unsafe_allow_html=True,
)
