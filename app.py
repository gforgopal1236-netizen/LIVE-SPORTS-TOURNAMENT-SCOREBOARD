
import streamlit as st
import sqlite3
import pandas as pd

# Initialize database
conn = sqlite3.connect('scoreboard.db', check_same_thread=False)
c = conn.cursor()

# Create table if not exists
c.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sport TEXT,
        team1 TEXT,
        team2 TEXT,
        score1 INTEGER,
        score2 INTEGER,
        status TEXT
    )
''')
conn.commit()

st.title("🏆 Live Sports Scoreboard App")

# Admin section to update scores
st.sidebar.header("⚡ Admin: Update Match Scores")
with st.sidebar.form(key='update_form'):
    sport = st.text_input("Sport (e.g., Cricket, Football)")
    team1 = st.text_input("Team 1 Name")
    team2 = st.text_input("Team 2 Name")
    score1 = st.number_input("Team 1 Score", min_value=0, value=0)
    score2 = st.number_input("Team 2 Score", min_value=0, value=0)
    status = st.selectbox("Match Status", ["Live", "Finished"])
    submit = st.form_submit_button("Update Score")

    if submit:
        c.execute('''
            INSERT INTO matches (sport, team1, team2, score1, score2, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (sport, team1, team2, score1, score2, status))
        conn.commit()
        st.success("✅ Score Updated Successfully!")

# Display live scoreboard
st.header("📊 Live Scoreboard")
query = "SELECT sport, team1, score1, team2, score2, status FROM matches ORDER BY id DESC"
matches_df = pd.read_sql_query(query, conn)

if not matches_df.empty:
    st.dataframe(matches_df)
else:
    st.write("No matches available yet.")

# Close DB connection on exit
def close_conn():
    conn.close()

st.button("🔄 Refresh Scores", on_click=close_conn)
