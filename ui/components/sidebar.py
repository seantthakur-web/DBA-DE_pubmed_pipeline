import streamlit as st

def render_sidebar():
    st.sidebar.title("Navigation")
    st.sidebar.page_link("ui/main.py", label="🏠 Home")
    st.sidebar.page_link("ui/pages/RAG_Chat.py", label="💬 RAG Chat")
    st.sidebar.page_link("ui/pages/DocumentSearch.py", label="🔍 Document Search")
    st.sidebar.page_link("ui/pages/AgentTrace.py", label="🧠 Agent Trace")
    st.sidebar.divider()
    st.sidebar.caption("PubMed RAG Pipeline Streamlit UI")
