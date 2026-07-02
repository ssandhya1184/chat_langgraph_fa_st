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
from utils import STATUS_BLOCKED, STATUS_OK, RISK_WORDS_LIST

# Model_Node - Invoke LLM with tools
def model_node(state: AgentState):
    logger.info(f"Entering model Node with state-->{state['messages']}")
    llm_with_tools = get_llm_with_tools().bind_tools([]) # Tentatively disabling tool binding
    #llm_with_tools = get_llm_with_tools()
    result = llm_with_tools.invoke(state['messages'])
    logger.info(f"##### Model Node with result -->{result} \n and type --> {type(result)}")
    return {
        'messages': [result]
    }


def tool_node(state: AgentState):
    logger.info(f"Entering get_tool_node with state-->{state['messages']}")
    tool_node = ToolNode(tools=[search_tool])
    return tool_node


#PII Guard Node
def pii_guard_node(state):
    logger.info(f"Entering pii_guard_node with state->{state['messages']}")
    last_message = state["messages"][-1]
    logger.info(f"Message ID of the last mesage is {last_message.id}")
    
    clean_text, pii_metadata = sanitize_text(last_message.content)
    logger.info(f"Cleantext-->{clean_text}")

    #Logging the redacted PII info
    logger.warning(f"PII Data detected -> {pii_metadata}")

    return {
        "messages": [HumanMessage(content=clean_text,id = last_message.id)],   
        "pii_metadata": pii_metadata
    }


""" Input Guard Node - To check if any unsafe words like hacking are prompted and if noted
    verify with the user if we can still proceed with the request
"""
def guard_input_with_hitl(state):
    logger.info(f"Entering hitl_niode with state-->{state['messages']}")
    risk_words = RISK_WORDS_LIST

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
                     "status": STATUS_OK,
                     "requires_approval": False
                }
        else:
            return {
            "messages": [AIMessage(content="Request blocked! Please try with other input.")],
            "status": STATUS_BLOCKED,
            "requires_approval": False
        }
    else:
        return {
            "status": STATUS_OK,
            "requires_approval": False
        }