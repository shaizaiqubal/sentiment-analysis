# YT Sentiment Lens

> Sentiment analysis dashboard that scrapes youtube comments, classifies sentiment, and displays overall mood

## Overview
YT Sentiment Lens analyses the sentiment of a video's top 500
comments and weights them by likes; so the opinions the crowd endorses carry more 
signal than random noise.
Paste any YouTube URL, get a sentiment breakdown in seconds.

## Features

- Supports both youtube.com and youtu.be URL formats
- Sentiment breakdown — Positive, Negative, Neutral
- Like-weighted sentiment — crowd-endorsed opinions carry more weight
- Overall verdict card — at a glance summary of audience reception
- Embedded video player alongside analysis

## How It Works

### Data Pipeline
- Scraped and cleaned 108,000 comments from Indian subreddits (r/india, 
  r/bollywood, r/Cricket and more)
- Auto-labeled using VADER sentiment analyzer
- Trained a Logistic Regression classifier on TF-IDF vectors
- Selected Logistic Regression after comparing against Naive Bayes and 
  Random Forest — LR consistently outperforms on sparse high-dimensional 
  text data

## Domain Adaptation

The model was deliberately trained on Reddit data and deployed on YouTube comments, two different domains with different writing styles. Reddit comments tend to be 
longer and more structured; YouTube comments are shorter and more reactive.
Observing real-world domain shift was more valuable than training and testing on the same distribution.

## Model Performance

| Model | Weighted F1 |
| --- | --- |
| Logistic Regression | **0.84** |
| Random Forest | 0.71 |
| Naive Bayes | 0.52 |

5-fold cross validation: **0.825 ± 0.002** — stable across splits.


## Tech Stack

| Layer | Tools |
|---|---|
| Frontend | Streamlit, Plotly |
| Backend | FastAPI, Uvicorn |
| ML | Scikit-learn, VADER, TF-IDF |
| Data | Pandas, Reddit dataset (Kaggle) |
| API | YouTube Data API v3 |

## Run Locally

### Prerequisites
- Python 3.9+
- YouTube Data API v3 key

### Installation
```bash
git clone https://github.com/shaizaiqubal/sentiment-analysis
cd sentiment-analysis
pip install -r requirements.txt
```

### Setup
Create a `.env` file in the root:
```
YOUTUBE_API_KEY=your_key_here
```

### Run
```bash
# Terminal 1 — FastAPI backend
uvicorn app:app --reload

# Terminal 2 — Streamlit frontend
streamlit run streamlit_app.py
```

## Project Structure
```
sentiment-analysis/
│
├── notebooks/
│   └── model_training.ipynb
│   └── preprocessing.ipynb
├── models/
│   ├── sentiment_model.pkl
│   └── tfidf_vectorizer.pkl
├── app.py                  ← FastAPI backend
├── streamlit_app.py        ← Streamlit frontend
├── youtube_fetcher.py      ← YouTube API integration
├── .env
├── requirements.txt
└── README.md
```