import streamlit as st
from anthropic import Anthropic


# Initialize Anthropic client
anthropic = Anthropic(api_key='')  # Replace with your actual API key

# Set up the Streamlit page
st.title("Season App Chatbot")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Set initial message if chat history is empty
    if len(st.session_state.messages) == 0:
        initial_message = "Welcome! I'm CLEO, your sports companion. I'd love to understand what brings you to sports. Would you like to share what interests you most right now?"
        st.session_state.messages.append({"role": "assistant", "content": initial_message})


# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to ask?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    # Get Claude's response
    try:
        # Messages list to include chat history
        messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
        messages.append({"role": "user", "content": prompt})
        response = anthropic.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=1000,
            system="""You are CLEO, SEASON's intelligent sports companion designed to make sports accessible and engaging for everyone, with a special focus on creating a welcoming space for women. You understand that sports has historically been gatekept and over-explained to women in condescending ways.
Core Traits:
- Non-judgmental and welcoming to all levels of sports interest
- Patient and permission-seeking before detailed explanations
- Concise yet thorough in responses
- Adaptable to each user's interests and comfort level
- Understanding that sports fandom comes in many forms""",
            messages=messages
        )
        # Add follow-up context gathering question
        if len(st.session_state.messages) == 2:  # After first user response
            follow_up = "Thank you for sharing! Would it be helpful if I asked a few quick questions to better personalize our conversation?"
            response.content[0].text += f"\n\n{follow_up}"
       
        # Display assistant message
        with st.chat_message("assistant"):
            st.write(response.content[0].text)


        
        # Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": response.content[0].text})
    except Exception as e:
        st.error(f"Error: {str(e)}")