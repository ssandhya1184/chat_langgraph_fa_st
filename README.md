# chat\_langgraph\_fa\_st

Simple Chat application using langgraph, Fast API and StreamLit

agent\_project/
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
│   │   ├── model\_node.py
│   │   ├── hitl\_node.py
│   │   ├── rejection\_node.py
│   │   └── **init**.py
│   │
│   ├── guards/                # 🛡️ guardrails
│   │   ├── pii\_guard.py
│   │   ├── input\_guard.py
│   │   ├── tool\_guard.py
│   │   ├── output\_guard.py
│   │   └── **init**.py
│   │
│   ├── routers/               # 🔀 routing logic
│   │   ├── input\_router.py
│   │   ├── hitl\_router.py
│   │   └── tool\_router.py
│   │
│   └── tools/                 # 🔎 tools (Tavily etc.)
│       ├── search\_tool.py
│       └── **init**.py
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
│   │   └── hitl\_controls.py
│   └── utils.py
│
├── config/                    # ⚙️ configs
│   ├── settings.py            # env vars, constants
│   └── prompts.py             # system prompts
│
├── tests/                     # 🧪 tests
│   ├── test\_graph.py
│   ├── test\_guards.py
│   └── test\_api.py
│
├── .env                       # 🔐 secrets
├── requirements.txt
├── README.md
└── main.py                    # optional entry point





Important Points:

\----------------

1. Schema Design
2. Structured Output from LLM
3. Validate LLM Response
4. Control LLM's Non Determinism
5. Prompt Injection
6. Prompt Versioning
7. Cost Calculation
8. PII Detection/Redaction
9. Fallback/Retry

