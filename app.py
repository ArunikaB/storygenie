# app.py (copy this)
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="StoryGenie", layout="wide")
st.title("📖 StoryGenie — Interactive Story Chatbot (Demo)")

if "history" not in st.session_state:
    st.session_state.history = []

with st.container():
    user_input = st.text_input("Type your action or message (e.g., 'Attack the dragon')", key="user_input")
    if st.button("Send"):
        text = user_input.strip()
        if text:
            text_l = text.lower()
            if any(k in text_l for k in ["attack", "fight", "hit", "strike"]):
                response = "You lash out bravely — smoke and sparks fill the cave."
                sentiment = "negative"
            elif any(k in text_l for k in ["talk", "negotiate", "speak", "reason", "ask"]):
                response = "You speak calmly; the creature seems curious and slows down."
                sentiment = "positive"
            elif any(k in text_l for k in ["run", "escape", "retreat"]):
                response = "You retreat carefully — the dragon watches you leave."
                sentiment = "neutral"
            else:
                response = "Interesting choice... the world reacts in mysterious ways."
                sentiment = "neutral"

            st.session_state.history.append({"input": text, "response": response, "sentiment": sentiment})
            st.session_state.user_input = ""
            st.experimental_rerun()

st.subheader("📜 Conversation")
for turn in reversed(st.session_state.history[-10:]):
    st.markdown(f"**You:** {turn['input']}")
    st.markdown(f"**Story:** {turn['response']}")
    st.markdown(f"*Sentiment:* {turn['sentiment']}")
    st.markdown("---")

st.sidebar.header("📊 Demo Analytics")
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
else:
    df = pd.DataFrame({
        "input": ["Attack the dragon","Negotiate","Attack the dragon","Offer gift","Run away"],
        "sentiment": ["negative","positive","negative","positive","neutral"]
    })

choice_counts = df["input"].value_counts().reset_index().rename(columns={"index":"choice", "input":"count"})
sent_counts = df["sentiment"].value_counts().reset_index().rename(columns={"index":"sentiment", "sentiment":"count"})

st.sidebar.subheader("Most recent choices")
fig1 = px.bar(choice_counts.head(10), x="choice", y="count", title="Choice frequency")
st.sidebar.plotly_chart(fig1, use_container_width=True)

st.sidebar.subheader("Sentiment split")
fig2 = px.pie(sent_counts, names="sentiment", values="count", title="Sentiment distribution")
st.sidebar.plotly_chart(fig2, use_container_width=True)
