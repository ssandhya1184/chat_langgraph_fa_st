import re
import os
import sys

from dotenv import load_dotenv
load_dotenv()

#root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(root_dir)

from logger_config import setup_logging
setup_logging()

import logging

from langgraph.types import interrupt
from langsmith import traceable
from langgraph.graph import add_messages, START, END, StateGraph
from langchain_core.messages import HumanMessage,AIMessage
from langgraph.checkpoint.memory import InMemorySaver

from agent.nodes import model_node, pii_guard_node, guard_input_with_hitl
from agent.agent_state import AgentState
from agent.routers import hitl_router


logger = logging.getLogger(__name__)
logger.info("In Agent File")






def run_agent():
    logger.info("Successful Agent!!")
    



#Graph Builder
graph_builder = StateGraph(AgentState)

#Add nodes to graph builder
graph_builder.add_node('model_node',model_node)
graph_builder.add_node('pii_node',pii_guard_node)
graph_builder.add_node('hitl_node',guard_input_with_hitl)

graph_builder.add_edge(START,'pii_node')
graph_builder.add_edge('pii_node','hitl_node')
graph_builder.add_conditional_edges(
    "hitl_node",
    hitl_router,
    {
        "model_node": "model_node",
        "end": END
    }
)

graph_builder.add_edge('model_node',END)


# Memory is required for HITL to save state during the interrupt
memory = InMemorySaver()
graph = graph_builder.compile(checkpointer=memory)







