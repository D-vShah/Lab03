import google.generativeai as genai
import streamlit as st
import requests as re


response = re.get("https://api.sportsdata.io/v4/soccer/scores/json/Players?key=YOUR_API_KEY")
players = response.json()

st.header('Learn About Your Favorite Footballer!')
st.info("Type the name of a player to learn about their career.")

player_name = st.text_input("Enter the footballer's name:")

if player_name:
    found_players = [p for p in players if player_name.lower() in p['Name'].lower()]

    if found_players:
        player = st.selectbox("Select a player:", [p['Name'] for p in found_players])

        try:
            genai.configure(api_key="AIzaSyCyT-q7icEuQen3rZOC6Grs1MzpTO8w0Go")
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(
                f"Write a detailed description of the career of football player {player}."
            )
            st.write(response.text)

            if 'messages' not in st.session_state:
                st.session_state.messages = []

            st.chat_message("assistant").markdown(response.text)

            talk = st.chat_input("Ask or say something about this player!")
            if talk:
                st.chat_message("user").markdown(talk)
                st.session_state.messages.append({'role': 'user', 'content': talk})
                response = model.generate_content(f"{talk}.")
                st.chat_message('assistant').markdown(response.text)
                st.session_state.messages.append({'role': 'assistant', 'content': response.text})

        except Exception as e:
            st.error("Error connecting to Google Gemini API. Please try again later.")
    else:
        st.warning("Player not found. Please check the spelling.")
