import streamlit as st
from langchain_community.chat_message_histories import (
    StreamlitChatMessageHistory
)
from Planners import MasterChat

msgs = StreamlitChatMessageHistory(key = "langchain_messages")
st.set_page_config(page_title="Gmail Manager", page_icon="📖")
st.title('Assistant to the Gmail Manager')

if 'history' not in st.session_state:
    st.session_state.history = []

if 'master_chat' not in st.session_state:
    st.session_state.master_chat = MasterChat()

for msg in st.session_state.history:
    if msg["role"] == "user":
        with st.chat_message("user", avatar='🧑🏻'):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar='🤖'):
            st.markdown(msg["content"])

if prompt := st.chat_input(placeholder='Ask me your data driven questions...'):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar='🧑🏻'):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar='🤖'):
        message_placeholder = st.empty()
        response = st.session_state.master_chat.chat(prompt)

        with message_placeholder.container():
            st.markdown(response)

        st.session_state.history.append(
            {
                "role": "assistant",
                "content": response,
            }
        )