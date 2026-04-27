import streamlit as st
import requests

text = st.text_input("enter")

if st.button("predict"):
    if not text.strip():
        st.error('Text field empty!')
    else:
        try:
            response = requests.post("http://127.0.0.1:8000/predict", json={'text':text},)
            if response.status_code == 400:
                st.warning(response.json()['detail'])
            else:
                result = response.json()
                st.text(result['sentiment'])
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to predicton server")