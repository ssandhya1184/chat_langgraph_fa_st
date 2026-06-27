import logging
from fastapi import FastAPI
from logger_config import setup_logging
from pydantic import BaseModel
from agent.chat_agent import graph
from agent.utils import format_response
from langchain_core.messages import HumanMessage
from langgraph.types import Command
from agent.sqlite_utils import init_db,upsert_chat
import sqlite3

#Setup Logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

#Chat Request Schema
class ChatRequest(BaseModel):
    message: str
    thread_id: str
    user_id : str

#Approval Request Schema
class ApprovalRequest(BaseModel):
    thread_id: str
    decision: bool
    user_id : str

# Store pending interrupts 
pending_interrupts = {}


@app.on_event('startup')
def on_start():
    init_db()

#Health Check URL
@app.get("/")
def health_check():
    return {'status':'ok'}

@app.post("/chat")
def chat_request(req: ChatRequest):
    logger.info(f"Entering chat request in chat_api with request data--> {req}")
    config = {
        "configurable": {
            "thread_id": req.thread_id, 
            "checkpoint_ns": req.user_id}
        }
    try:
        result = graph.invoke(
        {
         "messages": [HumanMessage(content=req.message)]},            
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

        #Update Chat details to sqlite db
        upsert_chat(req.thread_id, req.user_id, req.message)

        return {
            "status": "completed",
            "response": final_text
        }

    except:
        logger.error("Error in chat endpoint", exc_info=True)
        return {
            "status": "completed",
            "response": "Something went wrong. Please try again."
        }

@app.post("/approve")
def approve_request(req: ApprovalRequest):
    logger.info(f"Entering approve_request. Decision -> {req.decision}")

    config = {'configurable': {'thread_id':req.thread_id,"checkpoint_ns": req.user_id}}
    
    #Invoke graph with the user's decision
    result = graph.invoke(
        Command(resume = req.decision),
        config=config
    )
    
    #Return the response from agent after resuming back with user's decision
    final_text = format_response(result)

    if req.decision:
        upsert_chat(req.thread_id, req.user_id, final_text)

    return {
        "status": "completed",
        "response": final_text if req.decision else "Sorry. Please ask another question!"
    }

@app.get("/chats/{user_id}")
def get_chats(user_id: str):
    logger.info(f"Entering get_chats-> user_id: {user_id}")
    conn = sqlite3.connect("db\\chats.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT thread_id, title, updated_at
        FROM chats
        WHERE user_id = ?
        ORDER BY updated_at DESC
    """, (user_id,))

    rows = cursor.fetchall()
    
    return [
        {
            "thread_id": r[0],
            "title": r[1],
            "updated_at": r[2]
        }
        for r in rows
    ]


@app.get("/chat_history/{thread_id}")
def get_chat_history(thread_id: str):
    logger.info("Entering get_chat_history->thread_id: {thread_id}")
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    
    state = graph.get_state(config)
    logger.info(f"Current State from graph --> {state}")
    messages = state.values.get("messages", []) if state else []
    
    return_msg = []
    
    role = ""
    content = ""
    return_msg = []

    for msg in messages:
        if msg.type == "human":
            return_msg.append({
                "role": "user",
                "content": msg.content
            })

        elif msg.type == "ai":
            content = ""

            # AI content can be list OR string
            if isinstance(msg.content, list):
                for block in msg.content:
                    if block.get("type") == "text":
                        content = block.get("text", "")
                        break
            else:
                content = msg.content

            return_msg.append({
                "role": "assistant",
                "content": content
            })
    logger.info(f"Return message back to UI is-->{return_msg}")
    return return_msg

