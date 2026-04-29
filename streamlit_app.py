import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from yt_fetcher import get_data

st.set_page_config(page_title="YT Sentiment Lens", page_icon="🎬", layout="centered")

st.title("🎬 YT Sentiment Lens")
st.caption("Paste a YouTube URL to analyse the comment sentiment.")
st.divider()

url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Analyse", type="primary", width="stretch"):
    if not url.strip():
        st.error("Please enter a YouTube URL.")
    else:
        with st.spinner("Fetching comments…"):
            vid, vid_title, comments, likes = get_data(url)

        if not vid_title:
            st.error("Video not found — double-check the URL and try again.")
        else:
            st.header(vid_title)
            st.divider()

            try:
                with st.spinner("Running sentiment analysis…"):
                    response = requests.post("http://127.0.0.1:8000/predict", json={"lists": comments})

                if response.status_code == 400:
                    st.warning(response.json()["detail"])
                else:
                    result     = response.json()
                    sentiments = result["sentiments"]

                    df = pd.DataFrame({
                        'comments' : comments,
                        "likes" : likes,
                        "sentiment" : sentiments
                    })

                    
                    cont = len(df)

                    total_likes = df['likes'].sum()

                    if total_likes > 0:
                        
                        pos = df.query("sentiment == 'positive'")['likes'].sum()/total_likes
                        neg = df.query("sentiment == 'negative'")['likes'].sum()/total_likes
                        neu = df.query("sentiment == 'neutral'")['likes'].sum()/total_likes

                    else:
                        pos  = sentiments.count("positive") / cont
                        neg  = sentiments.count("negative") / cont
                        neu  = sentiments.count("neutral") / cont

                    if pos > 0.7:
                        st.success(" ↑ Overwhelmingly Positive")
                    elif neg > 0.4:
                        st.error(" ↓ Mostly Negative")
                    elif neu >= pos and neu >= neg:
                        st.info(" → Neutral Reception")
                    else:
                        st.warning(" → Mixed Reactions")

                    # Metrics
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Total",    cont)
                    c2.metric("Positive", f"{pos*100 : .1f}%")
                    c3.metric("Negative", f"{neg*100 : .1f}%")
                    c4.metric("Neutral",  f"{neu*100 : .1f}%")

                    st.divider()

                    # Chart + Video
                    chart_col, vid_col = st.columns(2, gap="large")

                    with chart_col:

                        fig = px.pie(
                            names=["Positive", "Negative", "Neutral"],
                            values=[pos, neg, neu],
                            color=["Positive", "Negative", "Neutral"],
                            color_discrete_map={
                                "Positive": "#2ecc71",
                                "Negative": "#e74c3c",
                                "Neutral":  "#95a5a6",
                            },
                            hole=0.4,
                        )
                        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=280)
                        st.plotly_chart(fig, width="stretch")

                    with vid_col:
                        st.iframe(f"https://www.youtube.com/embed/{vid}", height=280, width="stretch")

                    st.divider()
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the prediction server.")
