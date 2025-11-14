import streamlit as st

def render_sidebar():
    st.sidebar.title("Navigation")

    # Entrypoint file is main.py inside /app/ui
    st.sidebar.page_link(
        "main.py",
        label="Home"
    )

    st.sidebar.page_link(
        "pages/RAG_Chat.py",
        label="RAG Chat"
    )

    st.sidebar.page_link(
        "pages/DocumentSearch.py",
        label="Document Search"
    )

    st.sidebar.page_link(
        "pages/AgentTrace.py",
        label="Agent Trace"
    )

