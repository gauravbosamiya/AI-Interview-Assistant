from langchain_community.document_loaders import PyMuPDFLoader, Docx2txtLoader
import tempfile
import os

def extract_text_from_file(content:str, file_extension:str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name
        
    try:
        if file_extension == ".pdf":
            loader = PyMuPDFLoader(temp_file_path)
        elif file_extension == ".docx":
            loader = Docx2txtLoader(temp_file_path)
        else:
            raise ValueError("Unsupported file type")

        docs = loader.load()
        return "\n".join([doc.page_content for doc in docs])
    finally:
        os.remove(temp_file_path)