import streamlit as st

# -------------------------------------------------------------------
# Page registry
# -------------------------------------------------------------------
def load_page(page_name: str):
    if page_name == "RAG Chat":
        from ui.pages.RAG_Chat import render
    elif page_name == "Document Search":
        from ui.pages.DocumentSearch import render
    elif page_name == "Agent Trace":
        from ui.pages.AgentTrace import render
    else:
        st.error(f"Unknown page: {page_name}")
        return
    render()


# -------------------------------------------------------------------
# Main Application
# -------------------------------------------------------------------
def main():
    st.set_page_config(
        page_title="PubMed RAG System",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.sidebar.title("Navigation")

    pages = [
        "RAG Chat",
        "Document Search",
        "Agent Trace",
    ]

    selected_page = st.sidebar.radio("Select a page", pages)

    # Display selected page content
    load_page(selected_page)

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "**PubMed RAG System**  
        Multi-agent retrieval and biomedical question-answering interface."
    )


# -------------------------------------------------------------------
# Entry Point
# -------------------------------------------------------------------
if __name__ == "__main__":
    main()
