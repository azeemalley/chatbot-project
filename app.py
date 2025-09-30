import os
import streamlit as st
from openai import OpenAI

# Load API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Page setup
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 My AI Chatbot")
st.markdown("Welcome! Type your message below and chat with an AI assistant. ✨")

# Setup session state for storing chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful, professional AI assistant."}
    ]

# Chat input (bottom)
user_input = st.chat_input("Type a message...")

if user_input:
    # Add user input
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Model response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )

    reply = response.choices[0].message.content

    # Add assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})

# Display conversation history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**🧑 You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**🤖 Bot:** {msg['content']}")