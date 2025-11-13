from agents.base.shared import AgentState, logger, build_azure_llm

def reporter_node(state: AgentState) -> AgentState:
    logger.info(f"Reporter node invoked | trace_id={state.trace_id}")

    if not state.summary:
        state.insights = "No summary available. Reporter skipped."
        return state

    prompt = (
        "Extract the 3 most important biomedical insights from the summary.\n\n"
        f"Summary:\n{state.summary}\n"
    )

    try:
        model = build_azure_llm("insight")
        result = model.invoke(prompt)
        state.insights = result.strip()
    except Exception as e:
        logger.error(f"Reporter fallback due to Azure LLM error: {e}")
        state.insights = "Fallback: No insights available."

    return state
