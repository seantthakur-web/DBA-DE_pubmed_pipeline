import streamlit as st
from utils.api_client import query_rag

st.title("RAG Chat")

query = st.text_input("Enter your biomedical question:")

if st.button("Ask"):
    with st.spinner("Retrieving answer..."):
        result = query_rag(query)

    st.subheader("Answer")
    st.write(result)

