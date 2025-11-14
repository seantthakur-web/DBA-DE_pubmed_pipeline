import streamlit as st
from ui.components.sidebar import render_sidebar

st.set_page_config(
    page_title="PubMed RAG Pipeline",
    page_icon="🧬",
    layout="wide"
)

# Render the sidebar navigation
render_sidebar()

st.title("PubMed + OrderPipeline — RAG & Agents UI")
st.write("Welcome to the unified UI for your RAG pipeline, LangGraph agents, and PGVector search.")

st.divider()

st.subheader("How to use this UI")

st.write("""
Use the sidebar to navigate:
- **RAG Chat** — Ask questions and get answers powered by PGVector + GPT
- **Document Search** — Query PubMed embeddings directly
- **Agent Trace** — View LangGraph multi-step reasoning traces
""")

st.info("This UI is deployment-ready for Azure App Service.")
