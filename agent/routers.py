from agent.agent_state import AgentState
from logger_config import setup_logging
setup_logging()

import logging

logger = logging.getLogger(__name__)


def hitl_router(state: AgentState):
    logger.info("Entering hitl router and state is->.",state)
    if state.get("status") == "ok":
        return "model_node"
    elif state.get("status") == "blocked":
        return "end"


def tools_router(state):
    last_message = state["messages"][-1]

    if getattr(last_message, "tool_calls", None):
        return "tool_node"
    return "end"