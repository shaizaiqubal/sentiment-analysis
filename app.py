from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import re

model = joblib.load("models/sentiment_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

class textinput(BaseModel):
    text : str

def clean_text(text):
    pattern=r'\n|\t|\r|http\S+|[^\w\s]'
    cleaned_text = re.sub(pattern,'',text)
    cleaned_text = cleaned_text.strip().lower()
    return cleaned_text

app = FastAPI()

@app.get('/')
def home():
    return {"hello" :"world!"}

@app.post('/predict')
def accept_text(input : textinput):
    cleaned_text = clean_text(input.text)

    vec_text = vectorizer.transform([cleaned_text])
    pred = model.predict(vec_text)
    sentiment = pred[0]
    return {"sentiment" : sentiment}