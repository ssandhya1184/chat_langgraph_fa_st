import re
import os
import sys
#print("sys path-.",sys.path)
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

from agent.nodes import model_node
from agent.agent_state import AgentState


logger = logging.getLogger(__name__)
logger.info("In Agent File")






def run_agent():
    logger.info("Successful Agent!!")
    



#Graph Builder
graph_builder = StateGraph(AgentState)

#Add nodes to graph builder
graph_builder.add_node('model_node',model_node)

graph_builder.add_edge(START,'model_node')
graph_builder.add_edge('model_node',END)

graph = graph_builder.compile()







