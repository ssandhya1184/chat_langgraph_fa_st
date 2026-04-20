import os
import sys
from langchain_tavily.tavily_search import TavilySearch

from logger_config import setup_logging
setup_logging()

import logging

logger = logging.getLogger(__name__)
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

# WEb Search Tool
search_tool = TavilySearch(
   max_results=3,
   search_depth="basic", # "basic" or "advanced"
   api_key = os.getenv("TAVILY_API_KEY")
)