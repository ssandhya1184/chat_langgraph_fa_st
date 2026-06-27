from typing import TypedDict, Annotated, Literal
from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from logger_config import setup_logging
setup_logging()

import logging

logger = logging.getLogger(__name__)


# Defining State
class AgentState(TypedDict,total=False):
    messages: Annotated[list[BaseMessage],add_messages]
    pii_metadata: dict | None
    status: Literal["ok", "blocked", "needs_approval"]
    requires_approval: bool 

