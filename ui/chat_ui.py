import streamlit as st
import requests
import uuid
import json

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Agent UI", page_icon="🤖")
st.title("🤖 LangGraph Agent with Guardrails + HITL")

#Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

##Thread ID
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

#Approval Status
if "pending_approval" not in st.session_state:
    st.session_state.pending_approval = None


#Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


#Get input from user
user_input = st.chat_input("Hello! How can I help you?....")

if user_input:
    st.session_state.messages.append({"role":"user", "content":user_input})
    st.chat_message("user").markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            res = requests.post(
                f"{API_URL}/chat",
                json = {
                    'message':user_input,
                    'thread_id':st.session_state.thread_id
                }).json()

            # check if any approval required
            if res["status"] == "needs_approval":
                st.session_state.pending_approval = True
                st.session_state.messages.append(
                    {
                        'role' : 'assistant',
                        'content' : res['question']
                    }
                )
                st.markdown(res['question'])
            else:
                st.markdown(res["response"])
                st.session_state.messages.append(
                    {
                        'role' : 'assistant',
                        'content' : res['response']
                    }
                )


#Approve/Reject 
approval_box = st.empty()
if st.session_state.pending_approval:
    with approval_box.container():
        col1, col2 = st.columns(2)
        if col1.button("✅ Approve"):
            with st.chat_message('assistant'):
                with st.spinner("Loading.."):
                    # Invoke approve api 
                    res = requests.post(
                        f"{API_URL}/approve",
                        json = {
                            'thread_id' : st.session_state.thread_id,
                            'decision' : True
                        }
                    ).json()

                    #Add approval message to session state
                    st.session_state.messages.append({
                        'role' : 'assistant',
                        'content' : "✅ Approved! " + res["response"]
                    })

                    st.session_state.pending_approval = None
                    st.markdown("✅ Approved")
                    st.markdown(res["response"])
            

        if col2.button("❌ Reject"):
            with st.chat_message("assistant"):
                with st.spinner("Loading..."):

                    # Invoke approve api 
                    res = requests.post(
                        f"{API_URL}/approve",
                        json = {
                            'thread_id' : st.session_state.thread_id,
                            'decision' : False
                        }
                    ).json()

                    #Add Rejection message to session state
                    st.session_state.messages.append({
                        'role' : 'assistant',
                        'content' : "❌ Rejected! " + res["response"]
                    })
                    st.session_state.pending_approval = None
                    st.markdown("❌ Rejected!")
                    st.markdown(res["response"])
                
                











           
