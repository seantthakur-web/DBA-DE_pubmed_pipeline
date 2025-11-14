import streamlit as st
from ui.utils.api_client import rag_chat

st.title("RAG Chat")

query = st.text_input("Enter your biomedical question:")

if st.button("Ask"):
    with st.spinner("Running RAG pipeline..."):
        result = rag_chat(query)
        st.json(result)

