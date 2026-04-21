import logging
from fastapi import FastAPI
from logger_config import setup_logging
from pydantic import BaseModel
from agent.chat_agent import run_agent
from agent.chat_agent import graph
from agent.utils import format_response
from langchain_core.messages import HumanMessage
from langgraph.types import Command

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

# Store pending interrupts 
pending_interrupts = {}

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
         "messages": [HumanMessage(content=req.message)]},
            #"messages": [HumanMessage(content="What is 3+4")]}, # for testing purpose
            config=config
        )
        logger.info(f"Response received from graph agent -->{result}")

        #Check for any interrupts
        if "__interrupt__" in result:
            pending_interrupts[req.thread_id] = result["__interrupt__"]
            interrupt = result["__interrupt__"][0]
            logger.info(f"Interrupt info ->{interrupt}")
            data = interrupt.value
            question = data["question"]

            return{
                "status" : "needs_approval",
                "question" : question
            }

        #Return the response from agent if no interrupt. Format the AIMessage
        final_text = format_response(result)

        return {
            "status": "completed",
            "response": final_text
        }

    except:
        logger.error("Error in chat endpoint", exc_info=True)
        return {
            "response": "Something went wrong. Please try again."
        }

@app.post("/approve")
def approve_request(req: ApprovalRequest):
    logger.info(f"Entering approve_request. Decision -> {req.decision}")

    config = {'configurable': {'thread_id':req.thread_id}}
    
    #Invoke graph with the user's decision
    result = graph.invoke(
        Command(resume = req.decision),
        config=config
    )
    
    #Return the response from agent after resuming back with user's decision
    final_text = format_response(result)

    if req.decision == False:
        return {
            "status": "completed",
            "response": "Sorry. Please ask another question!"
        }
    else:      
        return {
            "status": "completed",
            "response": final_text
        }

