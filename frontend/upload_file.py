import streamlit as st
from frontend.api_response import generate_questions, get_questions_from_db

def upload_document(username):
    try:
        st.sidebar.header("Upload Document")
        uploaded_file = st.sidebar.file_uploader("Choose a file", type=[".pdf", ".docx"])
        
        if uploaded_file is not None:
            if st.sidebar.button("Upload"):
                with st.spinner("Uploading..."):
                    response = generate_questions(uploaded_file, username)
                    if response:
                        file_id = response["file_id"]
                        st.session_state["file_id"] = file_id
                        st.session_state["username"] = username

                        questions = get_questions_from_db(file_id, username)
                        
                        st.session_state["questions"] = questions
                        st.session_state["question_index"] = 0
                        
                        st.sidebar.success(f"File '{uploaded_file.name}' uploaded successfully.")
                        st.success("Questions loaded. Ready to begin interview.")
                    else:
                        st.sidebar.error("Something went wrong!")
    except Exception as e:
        st.error(str(e))
