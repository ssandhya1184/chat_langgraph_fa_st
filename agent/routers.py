from agent.agent_state import AgentState

def hitl_router(state: AgentState):
    logger.info("Entering hitl router and state is->.",state)
    if state.get("status") == "ok":
        return "model_node"
    elif state.get("status") == "blocked":
        return "end"