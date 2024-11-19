import streamlit as st
import json

# Function to load users from the JSON file
def load_users():
    with open("users.json") as file:
        return json.load(file)

def login():
    st.title("Welcome to MoodCure!")
    st.write("Please log in to access the app.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    user_data = load_users()

    if st.button("Login"):
        if username == user_data["username"] and password == user_data["password"]:

            st.session_state.logged_in = True
            st.session_state.username = username
            # st.session_state.page = "main"
            # st.experimental_rerun() 
            st.success("Login Successful, redirecting to MoodCure app")
        else:
            st.error("Invalid credentials. Please try again.")

login()