from logger_config import setup_logging
setup_logging()

import logging
logger = logging.getLogger(__name__)

from agent.llm_config import get_llm_with_tools
from agent.agent_state import AgentState
from agent.utils import sanitize_text
from langchain_core.messages import HumanMessage,AIMessage
from langgraph.types import interrupt
from agent.agent_tools import search_tool
from langgraph.prebuilt import ToolNode


# Model_Node - Invoke LLM with tools
def model_node(state: AgentState):
    logger.info(f"Entering model Node with state-->{state}")
    llm_with_tools = get_llm_with_tools().bind_tools([]) # Tentatively disabling tool binding
    #llm_with_tools = get_llm_with_tools()
    return {
        'messages': llm_with_tools.invoke(state['messages'])
    }


def tool_node(state: AgentState):
    logger.info(f"Entering get_tool_node with state-->{state}")
    tool_node = ToolNode(tools=[search_tool])
    return ""


#PII Guard Node
def pii_guard_node(state):
    logger.info(f"Entering pii_guard_node with state->{state}")
    last_message = state["messages"][-1]
    logger.info(f"Message from UI -> {last_message.content}")
    clean_text, pii_metadata = sanitize_text(last_message.content)

    #Logging the redacted PII info
    logger.warning(f"PII Data detected -> {pii_metadata}")

    return {
        "messages": [
            HumanMessage(content=clean_text)
        ],
        "overwrite_messages": True,   # ✅ important
        "pii_metadata": pii_metadata
    }


""" Input Guard Node - To check if any unsafe words like hacking are prompted and if noted
    verify with the user if we can still proceed with the request
"""
def guard_input_with_hitl(state):
    risk_words = ["hacking", "violence", "SSN", "jailbreak", "credit card number"]

    user_input = state['messages'][-1].content
    if any(word in user_input.lower() for word in risk_words):
        #Trigger an interrupt for Human Approval
        logger.warning(f"⚠️ Unsafe input detected {state['messages']}")

        decision = interrupt(
            {
                "type": "approval",
                "question": "This request may be unsafe! Please approve if you wish to continue!",
                "data": state["messages"][-1].content
            }
        )
        if decision:
            return {                
                     "status": "ok",
                     "requires_approval": False
                }
        else:
            return {
            "messages": [AIMessage(content="Request blocked! Please try with other input.")],
            "status": "blocked",
            "requires_approval": False
        }
    else:
        return {
            "status": "ok",
            "requires_approval": False
        }