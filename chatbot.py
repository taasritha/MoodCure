import os
import json
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as gen_ai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

def initialize_chat():
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

def save_user_summary(summary, mood):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_summary = {
        "timestamp": timestamp,
        "chat_summary": summary,
        "overall_mood": mood
    }

    file_path = "json_files/chat_responses.json"

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    except json.JSONDecodeError:
        st.error("Error reading the JSON file. Please check file contents.")
        data = []

    data.append(user_summary)

    try:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        st.success("Summary and mood saved successfully!")
    except Exception as e:
        st.error(f"Failed to save data: {e}")

def get_gemini_response(user_input, context=""):
    prompt = f"""
    You are a friendly, supportive assistant, and your role is to help the user navigate their emotions. 
    When the user shares their feelings or experiences, respond in a gentle, understanding way. 
    Offer advice and encouragement as a good friend would, and suggest activities, tips, or thoughts that could help improve their mood. 
    Make sure to always keep the tone positive and calming.

    Context: {context}
    User: {user_input}
    Respond in caring, friendly manner.
    Response should be short.
    """

    gemini_response = st.session_state.chat_session.send_message(prompt)
    return gemini_response.text

def summarize_chat(chat_history):
    prompt = f"Summarize this conversation in 3 lines:\n{chat_history}"
    summary_response = st.session_state.chat_session.send_message(prompt)
    return summary_response.text

def classify_mood(summary):
    mood = "Happy"
    if any(keyword in summary.lower() for keyword in ["sad", "down", "unhappy"]):
        mood = "Sad"
    elif any(keyword in summary.lower() for keyword in ["angry", "frustrated", "irritated"]):
        mood = "Anger"
    elif any(keyword in summary.lower() for keyword in ["stressed", "overwhelmed", "anxious"]):
        mood = "Stress"
    return mood

def chatbot():
    initialize_chat()

    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    user_prompt = st.chat_input("Ask me anything...")

    if len(st.session_state.messages) == 0:
        start_time = datetime.now().strftime("%H:%M")
        st.session_state.messages.append({"role": "assistant", "content": f"Hello! How are you feeling today? (Started at {start_time})"})

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        st.chat_message("user").markdown(user_prompt)

        if user_prompt.lower() in ["bye", "goodbye", "see you"]:
            st.session_state.messages.append({"role": "assistant", "content": f"Bye! Take care🫂"})
            chat_history = "\n".join([message["content"] for message in st.session_state.messages])
            summary = summarize_chat(chat_history)
            mood = classify_mood(summary)

            # st.write(f"Chat Summary:\n{summary}\n\nConcluding Mood: {mood}")

            save_user_summary(summary, mood)
        else:
            context = "This is a chatbot to provide emotional support, so be friendly and supportive."
            response_text = get_gemini_response(user_prompt, context)

            st.session_state.messages.append({"role": "assistant", "content": response_text})
            with st.chat_message("assistant"):
                st.markdown(response_text)
