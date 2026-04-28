from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import re
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),  # writes to file
        logging.StreamHandler()           # also prints to console
    ]
)

logger = logging.getLogger(__name__)

try:
    model = joblib.load("models/sentiment_model.pkl")
    vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
    logger.info("Model and vectorizer loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise

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
        logger.error("Comment field empty")
        raise HTTPException(status_code=400, detail="Comment field empty")
    try:
        logger.info(f"Batch prediction request received: {len(input.lists)} comments")
        cleaned_text = [clean_text(t) for t in input.lists]
        vec_text = vectorizer.transform(cleaned_text)
        pred = model.predict(vec_text)
        logger.info(f"Predictions complete")
        return {"sentiments": pred.tolist()}
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=500, detail="Prediction error")


