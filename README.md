# Production-Ready LangGraph AI Assistant | FastAPI | Streamlit | PII Guardrails | Human-in-the-Loop | Docker | AWS
![LangGraph](https://img.shields.io/badge/LangGraph-Stateful%20Agent-green)
![HITL](https://img.shields.io/badge/HITL-Human--in--the--Loop-blue)
![PII Guardrails](https://img.shields.io/badge/Guardrails-PII%20Protection-red)
![Tool Calling](https://img.shields.io/badge/Tool%20Calling-Tavily-orange)

This project demonstrates a production-style Generative AI assistant built using LangGraph, FastAPI, and Streamlit. The application supports conversational AI with stateful memory, PII masking, Human-in-the-Loop (HITL) approval, persistent chat history, and tool integration using Tavily Search. The entire application is containerized using Docker and can be deployed on AWS.

## Features

- LangGraph StateGraph workflow
- Human-in-the-Loop (HITL) approval using LangGraph Interrupts
- PII Detection & Masking
- Tavily Web Search Tool Integration
- Persistent Conversation Memory
- SQLite Checkpointer
- Chat History Management
- FastAPI Backend
- Streamlit Chat Interface
- Dockerized Deployment
- AWS Ready
- Modular Project Structure
- Structured Logging

## Architecture
```mermaid
flowchart TD

A[User] --> B[Streamlit Chat UI]

B --> C[FastAPI Backend]

C --> D[LangGraph Workflow]

D --> E[PII Guard Node]

E --> F[HITL Approval]

F --> G[LLM Node]

G --> H{Tool Required?}

H -->|Yes| I[Tavily Search]

I --> G

H -->|No| J[Response]

J --> K[SQLite Checkpointer]

K --> B
```

## Langgraph Workflow
```mermaid
flowchart TD

START --> PII

PII --> HITL

HITL -->|Approved| MODEL

HITL -->|Rejected| END

MODEL --> TOOLCHECK

TOOLCHECK -->|Tool Needed| TOOL

TOOL --> MODEL

TOOLCHECK -->|Done| END
```

## Tech Stack
| Component        | Technology             |
| ---------------- | ---------------------- |
| LLM Framework    | LangGraph              |
| LLM              | Google Gemma 4         |
| Tool Calling     | Tavily Search          |
| Backend          | FastAPI                |
| Frontend         | Streamlit              |
| Database         | SQLite                 |
| Memory           | LangGraph Checkpointer |
| Containerization | Docker                 |
| Deployment       | AWS EC2 + ECR          |
| Language         | Python                 |


## To run locally
uv sync

uv run uvicorn api.chat_api:app --reload

uv run streamlit run ui/chat_ui.py

## Docker commands
docker compose build

docker compose up

## AWS Deployment
Docker Images
EC2
Docker Compose

## API Endpoints
| Endpoint                      | Description          |
| ----------------------------- | -------------------- |
| POST /chat                    | Chat with assistant  |
| POST /approve                 | Resume after HITL    |
| GET /chats/{user_id}          | Recent Chats         |
| GET /chat_history/{thread_id} | Conversation History |


# Application Screenshots

## Home Page

![Chat UI](screenshots/Chat_UI.png)

---
### Recent Chats

![Recent Chats](screenshots/Recent_Chats.png)

---
### PII Masking

![PII Masking](screenshots/PII_Masking.png)

---

---
### HITL Approval

![HITL Approval](screenshots/HITL_Approval.png)

---

---
### HITL Rejection

![HITL Rejection](screenshots/HITL_Rejection.png)

---

---
### Docker Containers

![Docker Container](screenshots/Docker_Containers.png)

---