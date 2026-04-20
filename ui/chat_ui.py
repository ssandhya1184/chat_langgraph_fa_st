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
            chat_response = requests.post(
                f"{API_URL}/chat",
                json = {
                    'message':user_input,
                    'thread_id':st.session_state.thread_id
                }).json()

            print("chat_response---",chat_response)
            st.markdown(chat_response["response"])
           # st.session_state.messages.append({"role":"assistant","content":chat_response["response"]})
