import streamlit as st
from ui.utils.api_client import document_search

st.title("Document Search")

query = st.text_input("Search PubMed documents:")

if st.button("Search"):
    with st.spinner("Retrieving documents..."):
        result = document_search(query)
        st.json(result)

