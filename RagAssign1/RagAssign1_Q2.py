import os
import chromadb
import streamlit as st
from langchain.embeddings import init_embeddings
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.tools import tool
st.set_page_config(page_title="Agentic Resume RAG", layout="wide")
embed_model = init_embeddings(
    model="text-embedding-nomic-embed-text-v1.5",
    provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy",
    check_embedding_ctx_length=False
)
llm = init_chat_model(
    model="llama-3.1-8b-instruct",
    model_provider="openai",
    base_url="http://127.0.0.1:1234/v1",
    api_key="dummy"
)
db = chromadb.PersistentClient(path="./Resume_data")
collection = db.get_or_create_collection("resumes")
def load_pdf_resume(path):
    loader = PyPDFLoader(path)
    docs = loader.load()
    return " ".join([d.page_content for d in docs])
@tool
def retrieve_resumes(query: str) -> str:
    """Retrieve relevant resume content based on query"""
    q_embed = embed_model.embed_query(query)
    result = collection.query(
        query_embeddings=[q_embed],
        n_results=2
    )
    if not result["documents"] or not result["documents"][0]:
        return "No relevant resumes found."
    return "\n\n".join(result["documents"][0])
def agentic_rag_answer(query):
    retrieved_text = retrieve_resumes(query)
    prompt = f"""
You are an intelligent resume analysis agent.
You have access to a retrieval tool which has already been used.
Now reason over the retrieved resume information and answer clearly.
Retrieved Resume Content:
{retrieved_text}
User Question:
{query}
Final Answer:
"""
    return llm.invoke(prompt).content
if "loaded" not in st.session_state:
    if os.path.exists("fake-resumes"):
        for file in os.listdir("fake-resumes"):
            if file.endswith(".pdf") and file not in collection.get()["ids"]:
                path = os.path.abspath(os.path.join("fake-resumes", file))
                text = load_pdf_resume(path)
                emb = embed_model.embed_documents([text])
                collection.add(
                    ids=[file],
                    documents=[text],
                    embeddings=emb,
                    metadatas=[{"source": path}]
                )
    st.session_state.loaded = True
st.sidebar.title("Menu")
page = st.sidebar.radio(
    "Navigate",
    ["Home", "Add", "Delete", "Update", "All Resumes"]
)
all_ids = collection.get()["ids"]
if page == "Home":
    st.title("Agentic Resume Search")
    query = st.text_input("Ask about skills, experience, projects")
    if query:
        with st.spinner("Thinking..."):
            answer = agentic_rag_answer(query)
        st.subheader("Agent Answer")
        st.write(answer)
elif page == "Add":
    st.title("Add Resume")
    uploaded = st.file_uploader("Upload Resume PDF", type=["pdf"])
    if uploaded and st.button("Add Resume"):
        name = uploaded.name
        path = os.path.abspath(name)
        with open(path, "wb") as f:
            f.write(uploaded.read())
        text = load_pdf_resume(path)
        emb = embed_model.embed_documents([text])
        if name not in all_ids:
            collection.add(
                ids=[name],
                documents=[text],
                embeddings=emb,
                metadatas=[{"source": path}]
            )
            st.success("Resume added successfully")
        os.remove(path)
        st.rerun()
elif page == "Delete":
    st.title("Delete Resume")
    if all_ids:
        rid = st.selectbox("Select resume", all_ids)
        if st.button("Delete"):
            collection.delete(ids=[rid])
            st.success("Deleted successfully")
            st.rerun()
elif page == "Update":
    st.title("Update Resume")
    if all_ids:
        rid = st.selectbox("Select resume", all_ids)
        updated = st.file_uploader("Upload updated PDF", type=["pdf"])
        if updated and st.button("Update Resume"):
            path = os.path.abspath(updated.name)
            with open(path, "wb") as f:
                f.write(updated.read())
            text = load_pdf_resume(path)
            emb = embed_model.embed_documents([text])
            collection.delete(ids=[rid])
            collection.add(
                ids=[rid],
                documents=[text],
                embeddings=emb,
                metadatas=[{"source": path}]
            )
            os.remove(path)
            st.success("Updated successfully")
            st.rerun()
elif page == "All Resumes":
    st.title("All Resumes")
    if all_ids:
        for r in sorted(all_ids):
            st.write(r)
    else:
        st.info("No resumes found")