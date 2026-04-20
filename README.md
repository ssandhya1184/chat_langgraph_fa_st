# chat_langgraph_fa_st
Simple Chat application using langgraph, Fast API and StreamLit

agent_project/
│
├── app/                        # 🚀 FastAPI backend
│   ├── api.py                 # FastAPI routes (/chat, /approve)
│   ├── schemas.py             # Pydantic request/response models
│   └── dependencies.py        # shared configs (optional)
│
├── agent/                     # 🧠 LangGraph core
│   ├── graph.py               # graph builder + compile
│   ├── state.py               # AgentState schema
│   │
│   ├── nodes/                 # 🔧 all nodes (modular)
│   │   ├── model_node.py
│   │   ├── hitl_node.py
│   │   ├── rejection_node.py
│   │   └── __init__.py
│   │
│   ├── guards/                # 🛡️ guardrails
│   │   ├── pii_guard.py
│   │   ├── input_guard.py
│   │   ├── tool_guard.py
│   │   ├── output_guard.py
│   │   └── __init__.py
│   │
│   ├── routers/               # 🔀 routing logic
│   │   ├── input_router.py
│   │   ├── hitl_router.py
│   │   └── tool_router.py
│   │
│   └── tools/                 # 🔎 tools (Tavily etc.)
│       ├── search_tool.py
│       └── __init__.py
│
├── services/                  # ⚙️ external integrations
│   ├── llm.py                 # LLM setup (Gemini/OpenAI)
│   ├── memory.py              # MemorySaver config
│   └── logging.py             # logging / tracing
│
├── ui/                        # 🎨 Streamlit frontend
│   ├── app.py                 # main UI
│   ├── components/
│   │   ├── chat.py
│   │   ├── badges.py
│   │   └── hitl_controls.py
│   └── utils.py
│
├── config/                    # ⚙️ configs
│   ├── settings.py            # env vars, constants
│   └── prompts.py             # system prompts
│
├── tests/                     # 🧪 tests
│   ├── test_graph.py
│   ├── test_guards.py
│   └── test_api.py
│
├── .env                       # 🔐 secrets
├── requirements.txt
├── README.md
└── main.py                    # optional entry point
