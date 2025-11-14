import streamlit as st

def render_sidebar():
    st.sidebar.title("Navigation")

    # Entry point
    st.sidebar.page_link("main.py", label="Home")

    # Pages from pages_custom
    st.sidebar.page_link("pages_custom/RAG_Chat.py", label="RAG Chat")
    st.sidebar.page_link("pages_custom/DocumentSearch.py", label="Document Search")
    st.sidebar.page_link("pages_custom/AgentTrace.py", label="Agent Trace")
