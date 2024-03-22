"""
A basic streamlit chatbot
"""
import streamlit as st
import config
from openai_utils import ChatClient

st.title("Chatbot Template")

# Initialize chat history
if "client" not in st.session_state:
    st.session_state.client = ChatClient(
        azure_endpoint=config.openai.API_BASE,
        api_key=config.openai.API_KEY,
        api_version=config.openai.API_VERSION,
        deployment=config.openai.DEPLOYMENT_NAME,
    )

# Display chat messages from history on app rerun
# Note: The client will omit system messages by default
for message in st.session_state.client.messages:
    with st.chat_message(message.role.value):
        st.markdown(message.content)

# React to user input
if prompt := st.chat_input():
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to chat history
    st.session_state.client.user(prompt)

    # Stream assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(
            st.session_state.client.stream_response()
        )
        st.session_state.client.assistant(response)
