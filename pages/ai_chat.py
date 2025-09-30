import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="AI-guided First Aid Support", layout="centered")
st.header("🧠 AI-guided First Aid Support")

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY") or "YOUR_API_KEY"
genai.configure(api_key=api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Create model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get Gemini response
def get_gemini_response(history):
    prompt = ""
    for msg in history:
        role = "User" if msg["role"] == "user" else "AI"
        prompt += f"{role}: {msg['content']}\n"
    prompt += "AI:"
    response = model.generate_content(prompt)
    return response.text

# Input box
user_input = st.chat_input("💬 Talk to the AI counselor:")

if user_input:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    ai_response = get_gemini_response(st.session_state.messages)

    # Store AI response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})

    # Show AI response immediately
    with st.chat_message("assistant"):
        st.markdown(ai_response)

# Display chat history (without duplicating)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])
