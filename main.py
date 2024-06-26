import streamlit as st
import os
from llm import (setup_groq_client, groq_chat_completion,
                 LLAMA3_70B, LLAMA3_8B, GEMMA_7B_IT)
import time


st.set_page_config(
        page_title="RAG Chatbot",
)


# Streamlit app title
st.title("Project 4 RAG-based Chatbot")

backend_LLM = LLAMA3_70B
file_filter = None
GROQ_API_KEY = None


def setup_groq_with_backend():
    if not GROQ_API_KEY or not GROQ_API_KEY.startswith('gsk_'):
        st.warning('Please enter your Groq API key!', icon='⚠')
    else:
        setup_groq_client(GROQ_API_KEY, backend_LLM)


# GROQ_API_KEY = st.sidebar.text_input('Groq API Key', type='password')
GROQ_API_KEY = "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"

backend_LLM = st.sidebar.selectbox("LLM", 
                                   options=(LLAMA3_70B, LLAMA3_8B, GEMMA_7B_IT),
                                   on_change=setup_groq_with_backend())
# doc_type = st.sidebar.selectbox("Doc Type", options=("general", "git"))
# external_url_source = st.sidebar.text_input('Enter External Source URL:',
#                                             placeholder='<URL>')


# Streamed response emulator
def response_generator(urls, session_messages):
    response = groq_chat_completion(urls, session_messages)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# def response_generator(urls, session_messages):
#     response = groq_chat_completion(urls, session_messages)
    
#     for line in response.split("\n\n\n"):
#         for word in line.split():
#             yield word + " "
#             time.sleep(0.05)
#         yield "\n"


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    if GROQ_API_KEY and GROQ_API_KEY.startswith('gsk_'):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", 
                                        "content": prompt})

        urls = []
        # if external_url_source:
        #     urls = external_url_source.split(",")
        assistant_message = st.chat_message("assistant")
        with st.spinner("Thinking..."):
            llm_response = response_generator(
                urls=urls,
                # doc_type=doc_type,
                session_messages=st.session_state.messages,
                # file_filter=file_filter
            )
            response = assistant_message.write_stream(llm_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant",
                                        "content": response})
        external_url_source = ""
    else:
        st.toast("Please enter your Groq API key!", icon='❗')
