import streamlit as st
from components.sidebar import render_sidebar

st.set_page_config(
    page_title="PubMed RAG + Agents",
    layout="wide"
)

# Sidebar navigation
render_sidebar()

st.title("PubMed RAG + Agents Interface")
st.write("Use the sidebar to navigate between modules.")
