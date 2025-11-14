import streamlit as st

def render_sidebar():
    st.sidebar.title("Navigation")

    # Main entry file (relative to ui/)
    st.sidebar.page_link("main.py", label="Home")

    # Pages inside ui/pages/
    st.sidebar.page_link("pages/RAG_Chat.py", label="RAG Chat")
    st.sidebar.page_link("pages/DocumentSearch.py", label="Document Search")
    st.sidebar.page_link("pages/AgentTrace.py", label="Agent Trace")
