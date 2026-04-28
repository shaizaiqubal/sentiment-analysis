import streamlit as st
import plotly.express as px
import requests
import streamlit.components.v1 as components
from yt_fetcher import get_data

st.set_page_config(page_title="YT Sentiment Lens", page_icon="🎬", layout="centered")

st.title("🎬 YT Sentiment Lens")
st.caption("Paste a YouTube URL to analyse the comment sentiment.")
st.divider()

url = st.text_input("YouTube URL", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Analyse", type="primary", use_container_width=True):
    if not url.strip():
        st.error("Please enter a YouTube URL.")
    else:
        with st.spinner("Fetching comments…"):
            vid, vid_title, comments = get_data(url)

        if not vid_title:
            st.error("Video not found — double-check the URL and try again.")
        else:
            st.subheader(vid_title)
            st.divider()

            try:
                with st.spinner("Running sentiment analysis…"):
                    response = requests.post("http://127.0.0.1:8000/predict", json={"lists": comments})

                if response.status_code == 400:
                    st.warning(response.json()["detail"])
                else:
                    result     = response.json()
                    sentiments = result["sentiments"]

                    cont = len(sentiments)
                    pos  = sentiments.count("positive")
                    neg  = sentiments.count("negative")
                    neu  = sentiments.count("neutral")

                    # Metrics
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Total",    cont)
                    c2.metric("Positive", pos)
                    c3.metric("Negative", neg)
                    c4.metric("Neutral",  neu)

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
                        st.plotly_chart(fig, use_container_width=True)

                    with vid_col:
                        components.html(
                            f'<iframe width="100%" height="280" src="https://www.youtube.com/embed/{vid}" '
                            f'frameborder="0" allowfullscreen></iframe>',
                            height=280,
                        )

                    st.divider()

                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the prediction server.")