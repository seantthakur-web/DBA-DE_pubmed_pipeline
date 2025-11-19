import streamlit as st
from ui.utils.api_client import query_rag

# -------------------------------------------------------------------
# Safe wrapper to prevent UI crashes
# -------------------------------------------------------------------
def safe_search(question: str, top_k: int):
    try:
        return query_rag(question, top_k)
    except Exception as exc:
        st.error(f"API Error: {exc}")
        return None


# -------------------------------------------------------------------
# Page Renderer
# -------------------------------------------------------------------
def render():
    st.title("Document Search")

    st.markdown(
        "Use this tool to search PubMed-derived biomedical literature indexed in "
        "your PGVector database. This runs only the retrieval component (no full "
        "LangGraph pipeline)."
    )

    # Search input
    query_text = st.text_input(
        "Search query",
        placeholder="e.g., gastric cancer immunotherapy mechanisms"
    )

    top_k = st.number_input(
        "Top K Results",
        min_value=1,
        max_value=20,
        value=10,
        step=1,
    )

    run_button = st.button(
        "Search Documents",
        disabled=not query_text.strip()
    )

    if run_button:
        with st.spinner("Retrieving documents..."):
            response = safe_search(query_text, top_k)

        if response is None:
            return

        st.success("Documents retrieved.")

        # Retrieved documents
        st.subheader("Retrieved Documents")

        docs = response.get("retrieved_docs")
        if not docs:
            st.write("No documents returned.")
            return

        # Display each doc cleanly
        for idx, doc in enumerate(docs):
            st.markdown(f"### Document {idx + 1}")
            st.write(f"**PMID:** {doc.get('pmid', 'N/A')}")
            st.write(f"**Chunk ID:** {doc.get('chunk_id', 'N/A')}")

            text = doc.get("text", "")
            if text:
                st.markdown("**Text:**")
                st.write(text)

            score = doc.get("score")
            if score is not None:
                st.write(f"**Score:** {score:.6f}")

            st.markdown("---")
