from typing import TypedDict, Annotated, Literal
from langgraph.graph import add_messages


# Defining State
class AgentState(TypedDict,total=False):
    messages: Annotated[list,add_messages]
    pii_metadata: dict | None
    status: Literal["ok", "blocked", "needs_approval"]
    requires_approval: bool 