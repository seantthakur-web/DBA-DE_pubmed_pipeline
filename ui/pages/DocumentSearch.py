import streamlit as st
from ui.utils.api_client import search_documents

st.title("🔍 Document Search (PGVector)")

query = st.text_input("Search for documents:")

if st.button("Search"):
    if query.strip():
        with st.spinner("Retrieving vector search results..."):
            results = search_documents(query)
        st.json(results)
    else:
        st.warning("Please enter a search query.")
