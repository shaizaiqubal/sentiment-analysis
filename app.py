from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import re

model = joblib.load("models/sentiment_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

class textinput(BaseModel):
    text : str

class listinput(BaseModel):
    lists : list[str]

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
def accept_text(input : listinput):
    if not input.lists:
        raise HTTPException(status_code=400, detail="Comment field empty")
    cleaned_text = [clean_text(t) for t in input.lists]
    vec_text = vectorizer.transform(cleaned_text)
    pred = model.predict(vec_text)
    return {"sentiments": pred.tolist()}


# @app.post('/predict')
# def accept_text(input : textinput):
#     cleaned_text = clean_text(input.text)
#     if not input.text.strip():   
#         raise HTTPException(status_code=400, detail="Text cannot be empty")

#     vec_text = vectorizer.transform([cleaned_text])
#     pred = model.predict(vec_text)
#     sentiment = pred[0]
#     return {"sentiment" : sentiment}