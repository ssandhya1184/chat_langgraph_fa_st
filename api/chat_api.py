import logging
from fastapi import FastAPI
from logger_config import setup_logging
from pydantic import BaseModel
from agent.chat_agent import run_agent
from agent.chat_agent import graph
from langchain_core.messages import HumanMessage

#Setup Logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

#Chat Request Schema
class ChatRequest(BaseModel):
    message: str
    thread_id: str

#Approval Request Schema
class ApprovalRequest(BaseModel):
    thread_id: str
    decision: bool

#Health Check URL
@app.get("/")
def health_check():
    return {'status':'ok'}

@app.post("/chat")
def chat_request(req: ChatRequest):
    logger.info("Entering chat request in chat_api")
    config = {"configurable": {"thread_id": req.thread_id}}
    try:
        result = graph.invoke(
        {
        # "messages": [HumanMessage(content=req.message)]},
            "messages": [HumanMessage(content="What is 3+4")]}, # for testing purpose
            config=config
        )
        logger.info(f"Response received from graph agent -->{result}")

        return {"response": str(result)}
    except:
        logger.error("Error in chat endpoint", exc_info=True)
        return {
            "response": "Something went wrong. Please try again."
        }