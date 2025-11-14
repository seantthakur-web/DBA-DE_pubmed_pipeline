import streamlit as st
from ui.utils.api_client import ask_rag

st.title("💬 RAG Chat")

query = st.text_input("Ask a question:")

if st.button("Submit"):
    if query.strip():
        with st.spinner("Retrieving context and generating answer..."):
            result = ask_rag(query)

        st.subheader("Answer")
        st.write(result.get("answer", "No answer returned."))

        st.subheader("Contexts Used")
        st.json(result.get("contexts", []))
    else:
        st.warning("Please enter a question.")

