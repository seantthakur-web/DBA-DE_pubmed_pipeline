from agents.base.shared import AgentState, logger, build_azure_llm

def summarizer_node(state: AgentState) -> AgentState:
    logger.info(f"Summarizer node invoked | trace_id={state.trace_id}")

    # documents list
    docs = state.documents or []

    if not docs:
        state.summary = "No documents provided. Summary skipped."
        return state

    prompt = (
        "Summarize the following biomedical literature into 3–5 sentences.\n\n"
        f"Documents:\n{docs}\n"
    )

    try:
        model = build_azure_llm("summary")
        result = model.invoke(prompt)
        state.summary = result.strip()
    except Exception as e:
        logger.error(f"Summarizer fallback due to Azure LLM error: {e}")
        state.summary = "Fallback: Summary unavailable."

    return state
