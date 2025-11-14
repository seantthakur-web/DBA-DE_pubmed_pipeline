import streamlit as st
from ui.utils.api_client import agent_trace

st.title("Agent Trace Viewer")

trace_id = st.text_input("Enter a Trace ID:")

if st.button("Load Trace"):
    with st.spinner("Retrieving agent trace..."):
        result = agent_trace(trace_id)
        st.json(result)

