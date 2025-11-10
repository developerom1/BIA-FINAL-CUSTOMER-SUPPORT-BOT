import streamlit as st
try:
    import openai_whisper as whisper
    import numpy as np
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

from src.chatbot import CustomerSupportBot
import time

# Initialize the chatbot
bot = CustomerSupportBot()

# Load Whisper model for voice input
if WHISPER_AVAILABLE:
    @st.cache_resource
    def load_whisper_model():
        return whisper.load_model("base")

    whisper_model = load_whisper_model()
else:
    whisper_model = None

st.title("🛒 E-Commerce Customer Support Chatbot")

# Sidebar for user information
st.sidebar.header("User Information")
user_email = st.sidebar.text_input("Enter your email (optional)", placeholder="user@example.com")

# Chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input methods
input_method = st.radio("Choose input method:", ("Text", "Voice"))

if input_method == "Text":
    user_input = st.chat_input("Type your message here...")
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Process the message
        with st.spinner("Thinking..."):
            start_time = time.time()
            result = bot.process_message(user_input, user_email)
            response_time = time.time() - start_time

        # Add bot response to history
        response_content = f"{result['response']}\n\n*Intent: {result['intent']} (Confidence: {result['confidence']:.2f})*"
        st.session_state.chat_history.append({"role": "assistant", "content": response_content})

        # Display the new messages
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            st.markdown(response_content)

        # Display additional info
        st.write(f"Response time: {response_time:.2f} seconds")
        st.write(f"Sentiment: {result['sentiment']}")
        if result['entities']:
            st.write(f"Entities detected: {result['entities']}")

elif input_method == "Voice":
    if WHISPER_AVAILABLE:
        st.write("Click the button below and speak your message:")
        audio_value = st.audio_input("Record your message")

        if audio_value is not None:
            # Transcribe audio
            with st.spinner("Transcribing..."):
                audio_np = np.frombuffer(audio_value.getvalue(), dtype=np.int16).astype(np.float32) / 32768.0
                result_whisper = whisper_model.transcribe(audio_np)
                transcribed_text = result_whisper["text"]

            st.write(f"Transcribed: {transcribed_text}")

            # Process the transcribed message
            with st.spinner("Processing..."):
                start_time = time.time()
                result = bot.process_message(transcribed_text, user_email)
                response_time = time.time() - start_time

            # Display response
            st.write(f"Bot: {result['response']}")
            st.write(f"Response time: {response_time:.2f} seconds")
            st.write(f"Intent: {result['intent']} (Confidence: {result['confidence']:.2f})")
            st.write(f"Sentiment: {result['sentiment']}")
            if result['entities']:
                st.write(f"Entities detected: {result['entities']}")
    else:
        st.error("Voice input is not available. Please install openai-whisper and numpy to enable voice functionality.")

# Feedback section
st.header("Feedback")
rating = st.slider("Rate this interaction (1-5)", 1, 5, 3)
feedback = st.text_area("Additional feedback (optional)")
if st.button("Submit Feedback"):
    st.success("Thank you for your feedback!")

# Clear chat history
if st.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()
