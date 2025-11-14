import streamlit as st
from ui.utils.api_client import run_agent_trace

st.title("🧠 LangGraph Agent Trace")

query = st.text_input("Enter a query to inspect agent reasoning:")

if st.button("Run Agents"):
    if query.strip():
        with st.spinner("Executing LangGraph pipeline..."):
            trace = run_agent_trace(query)
        st.json(trace)
    else:
        st.warning("Please enter a query.")
