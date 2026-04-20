from logger_config import setup_logging
setup_logging()

import logging
logger = logging.getLogger(__name__)

from agent.llm_config import get_llm_with_tools
from agent.agent_state import AgentState

def model_node(state: AgentState):
    logger.info(f"Entering model Node with state-->{state}")
    llm_with_tools = get_llm_with_tools()
    return {
        'messages': llm_with_tools.invoke(state['messages'])
    }