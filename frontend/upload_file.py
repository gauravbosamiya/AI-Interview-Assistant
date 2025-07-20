import streamlit as st 
from frontend.api_response import get_question


def upload_document():
    try:
        st.sidebar.header("Upload Document")
        uploaded_file = st.sidebar.file_uploader("Choose a file",type=[".pdf",".docx"])
        
        
        if uploaded_file is not None:
            if st.sidebar.button("Upload"):
                with st.spinner("Uploading..."):
                    get_response = get_question(uploaded_file)
                    if get_response:
                        st.sidebar.success(f"File '{uploaded_file.name}' uploaded successfully with ID {get_response['file_id']}.")
                    else:
                        st.sidebar.error("Something went wrong!!")
                    st.write(get_response["questions"])
    except Exception as e:
        st.error(str(e)) 
    
                
    