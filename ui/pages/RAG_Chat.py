import streamlit as st
from ui.utils.api_client import query_rag

# -------------------------------------------------------------------
# Safe wrapper to prevent UI crashes
# -------------------------------------------------------------------
def safe_query_rag(question: str, top_k: int):
    try:
        return query_rag(question, top_k)
    except Exception as exc:
        st.error(f"API Error: {exc}")
        return None


# -------------------------------------------------------------------
# Page Renderer
# -------------------------------------------------------------------
def render():
    st.title("RAG Chat")

    st.markdown(
        "Ask a biomedical research question and run the full "
        "LangGraph-powered retrieval pipeline."
    )

    # User Input
    question = st.text_area(
        "Enter your question",
        height=120,
        placeholder="e.g., What is known about cisplatin resistance in gastric cancer?"
    )

    top_k = st.number_input(
        "Top K Documents",
        min_value=1,
        max_value=10,
        value=5,
        step=1,
    )

    run_button = st.button(
        "Run RAG Pipeline",
        disabled=not question.strip()
    )

    if run_button:
        with st.spinner("Running RAG pipeline..."):
            response = safe_query_rag(question, top_k)

        if response is None:
            return

        st.success("RAG query completed.")

        # -------------------------------------------------------------
        # Final Answer
        # -------------------------------------------------------------
        st.subheader("Final Answer")
        final_answer = response.get("final_answer")
        if final_answer:
            st.write(final_answer)
        else:
            st.write("(No final answer returned)")

        # -------------------------------------------------------------
        # Trace ID
        # -------------------------------------------------------------
        st.subheader("Trace ID")
        st.code(response.get("trace_id", "(none)"))

        # -------------------------------------------------------------
        # Insights
        # -------------------------------------------------------------
        insights = response.get("insights")
        if insights:
            st.subheader("Insights")
            for item in insights:
                st.write("- " + str(item))

        # -------------------------------------------------------------
        # Summaries
        # -------------------------------------------------------------
        summaries = response.get("summaries")
        if summaries:
            st.subheader("Summaries")
            for idx, item in enumerate(summaries):
                st.markdown(f"**Chunk {idx + 1}:** {item}")

        # -------------------------------------------------------------
        # Retrieved Documents
        # -------------------------------------------------------------
        retrieved_docs = response.get("retrieved_docs")
        if retrieved_docs:
            st.subheader("Retrieved Documents (Raw)")
            st.json(retrieved_docs)
