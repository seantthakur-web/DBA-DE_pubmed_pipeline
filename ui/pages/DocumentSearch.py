import streamlit as st
from utils.api_client import search_documents

st.title("Document Search")

term = st.text_input("Search PubMed Abstracts:")

if st.button("Search"):
    with st.spinner("Searching..."):
        results = search_documents(term)

    st.subheader("Results")
    st.write(results)

