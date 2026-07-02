from agent.agent_tools import search_tool
from langchain_google_genai import ChatGoogleGenerativeAI
from logger_config import setup_logging
from  utils import LLM_MODEL
setup_logging()

import logging

logger = logging.getLogger(__name__)

def get_llm_with_tools():

    #Get list of tools
    tools = [search_tool]
    logger.info(f"Creating llm_with_tools with the tools-->{tools}")

    #Set up LLM
    llm = ChatGoogleGenerativeAI(model=LLM_MODEL)

    #bind Tools
    llm_with_tools = llm.bind_tools(tools=tools)

    return llm_with_tools