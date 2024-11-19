import os
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import streamlit as st

score_to_mood = {
    3: "Happy",
    0: "Neutral",
    -3: "Sad",
    -6: "Anger",
    -9: "Anxiety"
}

def read_mood_data(file_path):
    data = []
    with open(file_path, "r") as f:
        try:
            entries = json.load(f) 
            for entry in entries:
                timestamp = entry.get("timestamp")
                mood = entry.get("overall_mood")

                if timestamp and mood:
                    mood_lower = mood.lower()
                    score = list(score_to_mood.keys())[list(map(str.lower, score_to_mood.values())).index(mood_lower)]
                    date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").date()
                    data.append({"date": date, "mood_score": score})
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file {file_path}")
        except ValueError:
            print(f"Mood '{mood}' in file {file_path} is not recognized in score_to_mood.")
    return data


def daily_mood_summary(json_folder=r'C:\Users\HP\Desktop\aasritha projects\IIP MoodCure\json_files'):
    file_paths = [os.path.join(json_folder, f) for f in os.listdir(json_folder) if f.endswith('.json')]
    all_data = []

    for file_path in file_paths:
        all_data.extend(read_mood_data(file_path))

    df = pd.DataFrame(all_data)
    daily_mood = df.groupby("date")["mood_score"].mean().reset_index()
    daily_mood["overall_mood"] = daily_mood["mood_score"].round().map(score_to_mood)

    return daily_mood

def mood_message(daily_mood):

    avg_score = daily_mood["mood_score"].mean()

    if avg_score >= 2:
        mood = "Happy"
        message = "Congarts! you’ve radiated positivity! 🌟 Your mood data shows a joyful and vibrant spirit, and it’s fantastic to see you in such a wonderful mindset. Keep enjoying the good moments and carrying that brightness into the week ahead! 😊 If you ever feel like diving deeper into what brings you happiness, a counselling session could offer unique insights and encouragement."
    elif avg_score >= 0:
        mood = "Neutral"
        message = "Your mood lately has been a mix of ups and downs, with a generally balanced mood. Some days brought a spark of happiness, while others may have felt a bit quieter. It’s completely normal to have varied experiences! Remember to celebrate the good moments and embrace any self-care you need. If you'd like a little more guidance on finding more consistency in your week, our counselling sessions are a great resource to explore.😊"
    elif avg_score >= -3:
        mood = "Sad"
        message = "It looks like this week had some challenging days. It’s okay to feel low or frustrated—it happens to everyone. Give yourself permission to rest and recharge and take things step-by-step. A fresh week is coming, and every day is a chance for new positivity. If you’d like someone to help you navigate through these feelings, consider booking a counselling session for added support and understanding.💙"
    elif avg_score >= -6:
        mood = "Anger"
        message = "You might be feeling frustrated. Take a deep breath and allow yourself some time to relax. Remember, you’re not alone, and taking time for yourself is important. Take it one day at a time and know that next week offers a fresh start. If you’d like, a counselling session could provide a safe space to talk things through and find new ways to manage these feelings🌿"
    else:
        mood = "Anxiety"
        message = "It seems like this past week has been especially tough, and that’s completely understandable. Life can get overwhelming, and handling everything on your own is no small feat. Remember, you’re not alone, and taking time for yourself is important. Take it one day at a time and know that next week offers a fresh start. If you’d like, a counselling session could provide a safe space to talk things through and find new ways to manage these feelings.🌱"
    
    return mood, message

def summary():
    daily_mood = daily_mood_summary()

    plt.style.use('dark_background')
    plt.figure(figsize=(5, 3))
    plt.plot(daily_mood["date"], daily_mood["mood_score"], marker="o", linestyle="-", color="cyan")
    plt.xticks(rotation=45)
    plt.xlabel("Date", color="white")
    plt.ylabel("Mood", color="white")
    plt.title("Daily Mood Over Time", color="white")
    plt.grid(True, color='white', linestyle='--', linewidth=0.5)

    mood_labels = list(score_to_mood.values())
    plt.yticks(ticks=list(score_to_mood.keys()), labels=mood_labels, color="white")

    st.pyplot(plt)

    mood, message = mood_message(daily_mood)
    st.write(f"Overall Mood: {mood}")
    st.write(message)
