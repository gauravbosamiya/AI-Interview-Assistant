import streamlit as st 
from frontend.upload_file import upload_document

st.set_page_config(page_title="AI Interview Assistant", layout="wide")
st.title("AI Interview Assistant")


upload_document()