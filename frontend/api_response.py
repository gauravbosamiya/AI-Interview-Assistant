import requests
import streamlit as st

def generate_questions(file,username):
    print("preparing questions for you...")
    try:
        files = {"file":(file.name, file, file.type)}
        data = {"username":username}
        response = requests.post("http://localhost:8000/generate-question", files=files, data=data)
        if response.status_code==200:
            return response.json()
        else:
            st.error(f"Failed to upload file. Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"An error occured while uploading file: {str(e)}")
        return None
    
def get_questions_from_db(file_id, username):
    response = requests.get(
        "http://localhost:8000/get-questions",
        params={"file_id": file_id, "username": username}
    )
    if response.status_code == 200:
        return response.json()["questions"]
    else:
        st.error(f"Failed to fetch questions: {response.status_code} - {response.text}")
        return []
