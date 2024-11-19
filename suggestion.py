import os
import streamlit as st
import requests
import json
from dotenv import load_dotenv
from datetime import datetime
from textblob import TextBlob

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

LOG_FILE = "json_files/suggestion_responses.json"

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w') as file:
        json.dump([], file) 

def determine_mood(user_input):
    blob = TextBlob(user_input)
    sentiment = blob.sentiment.polarity  # A value between -1 (negative) to 1 (positive)

    if sentiment > 0.5:
        return "happy"
    elif sentiment < -0.5:
        return "sad"
    else:
        return "neutral"

def interpret_user_request(user_input):
    recommendation_type = "uplifting playlist"
    mood_summary = "Mood summary unavailable"
    uplifting_message = "Stay positive! Here's something to lift your mood!"

    if "sad" in user_input.lower():
        mood_summary = "sad"
        uplifting_message = "Don't be sad, everyone has such days! Here are some recommendations that you can watch to feel good :)"
        recommendation_type = "uplifting songs"
    elif "happy" in user_input.lower():
        mood_summary = "happy"
        uplifting_message = "That's great! Keep up the positivity!"
        recommendation_type = "happy videos"
    elif "dance" in user_input.lower() or "dancing" in user_input.lower():
        mood_summary = "happy"
        uplifting_message = "Let's get some moves done!"
        recommendation_type = "dance videos"
    elif "angry" in user_input.lower():
        mood_summary = "angry"
        uplifting_message = "Take a deep breath. Here's something to help you relax."
        recommendation_type = "meditation exercises"
    elif "anxious" in user_input.lower() or "stressed" in user_input.lower() or "anxiety" in  user_input.lower():
        mood_summary = "anxiety"
        uplifting_message = "Don't worry, everything will be fine. Here's a calming suggestion."
        recommendation_type = "calming music"

    return recommendation_type, mood_summary, uplifting_message

def generate_youtube_query(recommendation_type, mood_summary):
    query = "uplifting playlist"

    if "meditation" in recommendation_type.lower():
        query = "relaxing meditation exercises"
    elif "song" in recommendation_type.lower():
        query = "uplifting songs"
    elif "telugu playlist" in recommendation_type.lower():
        query = "telugu song playlist"
    elif "audiobook" in recommendation_type.lower():
        query = "motivational audiobooks"
    elif "dance" in recommendation_type.lower():
        query = "dance tutorial"
    elif "uplifting" in recommendation_type.lower():
        query = "uplifting mood videos"

    return query




def youtube_search(query, result_type="video", max_results=5):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={max_results}&q={query}&type={result_type}&key={YOUTUBE_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # st.write("YouTube API Response:", data)  # actual response from YouTube
        
        results = []
        for item in data.get("items", []):
            video_title = item["snippet"]["title"]
            video_url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            thumbnail = item["snippet"]["thumbnails"]["default"]["url"]
            results.append({"title": video_title, "url": video_url, "thumbnail": thumbnail})
        return results
    else:
        st.error("Failed to fetch YouTube data.")
        return []


def log_user_interaction(timestamp, overall_mood):
    with open(LOG_FILE, 'r+') as file:
        data = json.load(file)
        data.append({"timestamp": timestamp, "overall_mood": overall_mood})
        file.seek(0)
        json.dump(data, file, indent=4)

def suggestions_page():
    user_input = st.text_input("Describe what you're feeling or what type of recommendation you'd like:")
    submit = st.button("Get Recommendation")

    if submit and user_input:
        recommendation_type, overall_mood, uplifting_message = interpret_user_request(user_input)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        youtube_query = generate_youtube_query(recommendation_type, overall_mood)

        results = youtube_search(query=youtube_query)

        log_user_interaction(timestamp, overall_mood)

        st.write(uplifting_message)

        st.subheader("Recommendations")
        for result in results:
            st.write(result["title"])
            st.image(result["thumbnail"])
            st.write(f"[Watch it on YouTube]({result['url']})")

