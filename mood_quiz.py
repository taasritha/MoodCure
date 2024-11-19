import streamlit as st
import json
import os
from dotenv import load_dotenv
from datetime import datetime
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def get_gemini_response(input_text, prompt):
    response = genai.GenerativeModel('gemini-1.5-flash').generate_content((input_text, prompt))
    return response.text

def save_summary_to_file(user_summary):
    user_summary["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    file_path = 'json_files/quiz_responses.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    data.append(user_summary)
 
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


def mood_quiz():
    st.header("Mood Evaluation Quiz 🌈")
    st.subheader("Let's evaluate your mood with a few questions!")

    questions_with_options = [
        ("How would you describe your energy level today?", ["Very energetic", "Slightly energetic", "Neutral", "Low energy", "Extremely tired"]),
        ("If you had to describe your mood in one word today, what would it be?", ["Fun", "Up and down", "Stressed", "Productive"]),
        ("How are you feeling emotionally right now?", ["Very happy and content", "Calm and peaceful", "Anxious or worried", "Frustrated or irritated", "Sad or down"]),
        ("How are you handling stress today?", ["I feel completely relaxed", "I’m managing it well", "I’m feeling a little stressed", "I’m overwhelmed and struggling", "I’m completely stressed out"]),
        ("How do you feel about the day ahead?", ["Excited and optimistic", "Neutral, just going with the flow", "Anxious or nervous", "Dreading it", "Indifferent"]),
        ("How often do you find yourself feeling stressed or anxious?", ["Never", "Occasionally", "Often", "Almost all the time"]),
        ("When was the last time you laughed?", ["Today", "Yesterday", "A few days ago", "I can’t remember"]),
        ("How have you been sleeping lately?", ["I’ve been sleeping great", "I’ve been sleeping okay", "I’ve been having trouble sleeping", "I haven’t been able to sleep well at all", "I haven’t noticed any changes in my sleep"]),
        ("What’s your mood like when you wake up in the morning?", ["Excited to start the day", "Calm and ready", "Neutral", "Tired and groggy", "Grumpy or irritated"]),
        ("How would you rate your overall mood today?", ["Excellent", "Good", "Okay", "Bad", "Terrible"]),
        ("When dealing with challenges, how do you feel today?", ["Confident and capable", "Hopeful and determined", "Hesitant or unsure", "Frustrated and overwhelmed", "Defeated and hopeless"]),
    ]


    responses = []
    for i, (question, options) in enumerate(questions_with_options):
        if options:
            response = st.radio(question, options, key=f"response_{i}", index=None)
            responses.append(response)
        else:
            response = st.text_area(question, key=f"response_{i}")
            responses.append(response)

    submit = st.button("Let's Go!")

    if submit:
        summarization_prompt = f"""
        Summarize the following user responses into key phrases or keywords for mood evaluation.
        User Responses:
        {responses}
        """

        summary_response = get_gemini_response(summarization_prompt, "Summarization Request")
        summarized_keywords = summary_response.split(", ")

        def determine_overall_mood(keywords):
            mood_scores = {
                "happy": 0,
                "sad": 0,
                "angry": 0,
                "anxiety": 0
            }

            for keyword in keywords:
                keyword_lower = keyword.lower()
                if any(pos in keyword_lower for pos in ["happy", "excited", "energetic", "productive", "content"]):
                    mood_scores["happy"] += 1
                elif any(neg in keyword_lower for neg in ["sad", "tired", "down", "blue", "grumpy"]):
                    mood_scores["sad"] += 1
                elif any(ang in keyword_lower for ang in ["angry", "frustrated", "irritated"]):
                    mood_scores["angry"] += 1
                elif any(anx in keyword_lower for anx in ["anxiety", "stressed", "nervous", "worried"]):
                    mood_scores["anxiety"] += 1
            
            overall_mood = max(mood_scores, key=mood_scores.get)
            return overall_mood

        overall_mood = determine_overall_mood(summarized_keywords)

        mood_messages = {
            "happy": "You're feeling happy today! 🌟. Keep spreading that positivity! Explore uplifting suggestions or chat with our chatbot anytime for a friendly boost!",
            "sad": "Your mood seems to be a bit down today. Treat yourself with some self-care. Whether it's through music, a funny video, or chatting with our chatbot, you deserve a boost.",
            "angry": "It seems like you're experiencing some frustration today. Remember to take some time to relax and unwind. Try calming content or talk to someone you trust.",
            "anxiety": "Today feels a bit overwhelming. Remember to take care of yourself and practice relaxation. Explore our calming suggestions, and our chatbot is here for you anytime."
        }
        
        st.subheader("Here's what you need to know about your mood today!")
        st.write(mood_messages.get(overall_mood, "Take it easy and give yourself time to recharge."))
        
        user_summary = {
            "user_responses": responses,
            "overall_mood": overall_mood
        }
        save_summary_to_file(user_summary)
