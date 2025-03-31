import os 
import requests
from dotenv import load_dotenv
import streamlit as st
import time

# Custom Styling for a Warm and Dreamy Theme
def set_page_style():
    st.markdown(
        """
        <style>
        body {
            font-family: 'Poppins', sans-serif;
            background-color: #2E1A47;
            color: #E0B0FF;
        }
        .stApp {
            max-width: 800px;
            margin: auto;
            padding: 20px;
            text-align: center;
            display: flex;
            flex-direction: column;
            height: 100vh;
            justify-content: space-between;
        }
        .title-container {
            text-align: center;
            margin-bottom: 15px;
        }
        .title-container h1 {
            font-size: 28px;
            color: #E0B0FF;
            font-weight: 600;
        }
        .title-container h2 {
            font-size: 18px;
            color: #D8BFD8;
            font-weight: 400;
        }
        .chat-container {
            background-color: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0px 4px 10px rgba(255, 255, 255, 0.2);
            max-height: 400px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
        }
        .user-message {
            background-color: #6A0DAD;
            padding: 10px;
            border-radius: 15px 15px 0px 15px;
            margin-bottom: 8px;
            max-width: 75%;
            color: white;
            align-self: flex-end;
            text-align: left;
            margin-left: auto;
        }
        .bot-message {
            background-color: #4B2A67;
            padding: 10px;
            border-radius: 15px 15px 15px 0px;
            margin-bottom: 8px;
            max-width: 75%;
            color: white;
            align-self: flex-start;
            text-align: left;
        }
        .timestamp {
            font-size: 10px;
            color: #D8BFD8;
            margin-top: 5px;
            text-align: right;
        }
        .input-box {
            border-radius: 10px;
            padding: 10px;
            width: 100%;
            background-color: #4B2A67;
            color: white;
            border: none;
        }
        .logo-container {
            text-align: center;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

class Arckybot:
    def __init__(self):
        """
        Initialize chatbot with Groq API for general troubleshooting.
        """
        load_dotenv()
        self.api_key = os.getenv('GROQ_API_KEY')
        self.url = 'https://api.groq.com/openai/v1/chat/completions'
    
    def generate_response(self, user_input):
        """
        Generate a helpful response via Groq API
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': 'llama-3.2-90b-vision-preview',
            'messages': [
                {"role": "system", "content": "You are Arckybot, a helpful AI assistant for troubleshooting and guidance."},
                {"role": "user", "content": user_input}
            ]
        }
        
        response = requests.post(self.url, headers=headers, json=payload)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"Error {response.status_code}: {response.json().get('error', 'Unknown error')}"

# Initialize chatbot
chatbot = Arckybot()

# Streamlit app setup
st.set_page_config(page_title="Arckybot - Your AI Assistant", page_icon="🤖")
set_page_style()

# Display the company logo in the center
st.markdown("<div class='logo-container'>", unsafe_allow_html=True)
st.image("C:/Users/Lina/coffee-machine-chatbot/logo.png", width=200)
st.markdown("</div>", unsafe_allow_html=True)

# Title and Subtitle
st.markdown("<div class='title-container'><h1>Welcome to Arckybot!</h1><h2>How can I assist you today?</h2></div>", unsafe_allow_html=True)

# Initialize conversation state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'awaiting_response' not in st.session_state:
    st.session_state.awaiting_response = False
if 'user_message' not in st.session_state:
    st.session_state.user_message = ""

# Function to process user input on submit
def process_input():
    user_input = st.session_state.user_input
    if user_input:
        # Store the message
        st.session_state.user_message = user_input
        
        # Flag that we're awaiting a response
        st.session_state.awaiting_response = True
        
        # Clear the input field
        st.session_state.user_input = ""

# Chat container with dynamic content
chat_container = st.container()

with chat_container:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    
    # Display existing chat history
    for timestamp, sender, message in st.session_state.history:
        if sender == "User":
            st.markdown(f"<div class='user-message'>{message}<div class='timestamp'>{timestamp}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-message'>{message}<div class='timestamp'>{timestamp}</div></div>", unsafe_allow_html=True)
    
    # Display the current user message immediately if there is one
    if st.session_state.awaiting_response and st.session_state.user_message:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        st.markdown(f"<div class='user-message'>{st.session_state.user_message}<div class='timestamp'>{timestamp}</div></div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Process the awaiting message if needed
if st.session_state.awaiting_response:
    # Get the message
    user_input = st.session_state.user_message
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Add to history
    st.session_state.history.append((timestamp, "User", user_input))
    
    # Reset the flags
    st.session_state.awaiting_response = False
    st.session_state.user_message = ""
    
    # Get bot response with typing effect
    bot_message_container = st.empty()
    full_response = chatbot.generate_response(user_input)
    
    # Display typing effect for bot response
    displayed_message = ""
    for char in full_response:
        displayed_message += char
        bot_message_container.markdown(
            f"""<div class="bot-message">{displayed_message}<div class="timestamp">{timestamp}</div></div>""",
            unsafe_allow_html=True
        )
        time.sleep(0.01)  # Adjust speed as needed
    
    # Add bot response to history
    st.session_state.history.append((timestamp, "Arckybot", full_response))

# User input with callback to process submission
user_input = st.text_input(
    "Message", 
    key="user_input",
    label_visibility="collapsed",
    on_change=process_input
)