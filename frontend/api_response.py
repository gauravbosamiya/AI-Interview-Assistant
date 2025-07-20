from api.app import generate_question
import requests
import streamlit as st

def get_question(file):
    print("preparing questions for you...")
    try:
        files = {"file":(file.name, file, file.type)}
        response = requests.post("http://localhost:8000/generate-question", files=files)
        if response.status_code==200:
            return response.json()
        else:
            st.error(f"Failed to upload file. Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occured while uploading file: {str(e)}")
        return None
