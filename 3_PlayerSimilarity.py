import requests as re
import streamlit as st

response = re.get("https://api.sportsdata.io/v4/soccer/scores/json/Players?key=YOUR_API_KEY")
players = response.json()

st.header('Which Footballer Matches Your Stats?')
st.info("Input your season stats to find a similar football player!")

goals = st.slider('Goals Scored', 0, 50, 5)
assists = st.slider('Assists', 0, 20, 3)
position = st.selectbox('Position', ['Forward', 'Midfielder', 'Defender', 'Goalkeeper'])

similar_players = []
for player in players:
    if (
        player.get('Position', '').lower() == position.lower() and
        abs(player.get('Goals', 0) - goals) <= 5 and
        abs(player.get('Assists', 0) - assists) <= 2
    ):
        similar_players.append(player)

if similar_players:
    st.success("We found players similar to you!")
    for p in similar_players:
        st.write(f"Name: {p['Name']}")
        st.write(f"Team: {p['Team']}")
        st.write(f"Position: {p['Position']}")
        st.image(p.get('PhotoUrl', ''))
        st.write('---')
else:
    st.warning("No players found with similar stats. You're one of a kind!")
