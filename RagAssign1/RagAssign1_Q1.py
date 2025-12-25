import chromadb
import os
from langchain.embeddings import init_embeddings
from langchain_community.document_loaders import PyPDFLoader
import streamlit as st
st.title("Resume Details")
embed_model = init_embeddings(
    model="text-embedding-all-minilm-l6-v2-embedding",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="not-needed",
    check_embedding_ctx_length=False
)
db = chromadb.PersistentClient(path="./Resume_data")
collection = db.get_or_create_collection("resumes")
def load_pdf_resume(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    text = ""
    for page in docs:
        text += page.page_content
    return text, {"source": pdf_path}
for file in os.listdir("fake-resumes"):
    if file.endswith(".pdf"):
        resume_path = os.path.join("fake-resumes", file)
        resume_text, resume_info = load_pdf_resume(resume_path)
        resume_embeddings = embed_model.embed_documents([resume_text])
        collection.add(ids=[resume_path], embeddings=resume_embeddings, metadatas=[resume_info], documents=[resume_text])
query = st.text_input("Ask Anything.....")
query_embedding = embed_model.embed_query(query)
results = collection.query(query_embeddings=[query_embedding], n_results=1)
st.write("\nMetadata:")
st.write(results["metadatas"][0][0])
st.write("\nMatched Resume Text:")
st.write(results["documents"][0][0])