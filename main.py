import streamlit as st
from chatbot import chatbot
from mood_quiz import mood_quiz
from suggestion import suggestions_page
from history import summary
from counsel import counsel_page

st.set_page_config(
    page_title="MoodCure",
    page_icon="🌈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
        .stButton>button {
            background-color: #f44336; /* Red color */
            color: white;
            font-size: 16px;
            border-radius: 5px;
            padding: 10px;
            width: 100%;
            margin-top: 20px;
        }
        
        .stButton>button:hover {
            color: white;
        }

        /* CSS for the 4-grid layout */
        .grid-container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 10px;
            max-width: 90%;
            margin: auto;
            background-color: #000; /* Set background color to black */
            padding: 20px;
            border-radius: 15px;
        }
        .grid-item {
            text-align: center;
            background-color: #1e1e1e; /* Dark background for each item */
            padding: 15px;
            border-radius: 12px;
            box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.3);
        }
        .grid-item h3 {
            font-size: 24px;
            margin-top: 10px;
            font-weight: bold; /* Make heading bold */
            color: #ffffff; /* Set text color to white */
        }
        .grid-item p {
            font-size: 14px;
            color: #cccccc; /* Light gray text for description */
            margin-top: 8px;
        }
    </style>
    """, unsafe_allow_html=True
)

def render_grid_layout():
    st.markdown(
        """
        <div class="grid-container">
            <div class="grid-item">
                <h2>Feelometer 🌟</h2>
                <p>Take this quiz to find out how you're feeling today!</p>
            </div>
            <div class="grid-item">
                <h2>LumiBot 🤖</h2>
                <p>A friendly companion awaits to listen and uplift your mood.</p>
            </div>
            <div class="grid-item">
                <h2>Cheerify 🎶</h2>
                <p>Get uplifting suggestions like quotes, music, or videos.</p>
            </div>
            <div class="grid-item">
                <h2>EmoWave 🌊</h2>
                <p>Track your mood journey and see your progress.</p>
            </div>
        </div>
        """, unsafe_allow_html=True
    )

def homepage():
    st.write("Welcome aasritha")
    st.sidebar.title("MoodCure Navigation")
    
    selected_option = st.sidebar.selectbox(
        "Choose a Service:",
        ["Home", "Feelometer", "LumiBot", "Cheerify", "EmoWave", "Professional Help"]
    )


    if st.sidebar.button("Logout", key="logout"):
        st.session_state.clear()
        st.write("You have been logged out. Please log in again to continue.")

    if selected_option == "Home":
        st.title("Welcome to MoodCure! 🌈")
        st.write(
            "Your personal companion for a brighter, happier day. Explore ways to uplift your mood and track your emotional journey. We’re here to help you feel your best 😊"
        )
        st.write("Explore MoodCure’s features")
        render_grid_layout()
    elif selected_option == "Feelometer":
        st.title("Feelometer 🌟")
        st.write("Quick check-in! Let's see how you're feeling today.")
        mood_quiz()
    elif selected_option == "LumiBot":
        st.title("LumiBot 🤖")
        st.write("Welcome to the LumiBot Section of MoodCure, where your friendly companion awaits to brighten your day! Our chatbot is here to listen, support, and uplift you whenever you need a virtual friend. Let's chat our way to a brighter mood together!")
        chatbot()
    elif selected_option == "Cheerify":
        st.title("Cheerify 🎶")
        st.write("Feeling like you need a little extra boost? 🎉")
        st.write("Sometimes all we need is a little nudge in the right direction. Whether you're looking for some motivational quotes, relaxing music, or fun ideas to cheer you up, I’ve got you covered.")
        suggestions_page()
    elif selected_option == "EmoWave":
        st.title("Your Emotional Journey 🌊")
        st.write("Track your mood journey and review your progress over time.")
        summary()
    elif selected_option == "Professional Help":
        counsel_page()

if __name__ == "__main__":
    homepage()
