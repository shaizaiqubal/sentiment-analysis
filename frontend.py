import streamlit as st
import requests

text = st.text_input("enter")

if st.button("predict"):
    response = requests.post("http://127.0.0.1:8000/predict", json={'text':text},)
    result = response.json()
    st.text(result['sentiment'])