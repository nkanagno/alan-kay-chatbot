
import streamlit as st
import time
import requests
import os


API_URL = "http://127.0.0.1:8000/ask/alan_kay"

def API_response(API_URL,question):
    try:
        response = requests.post(API_URL, json={"question": question})
        if response.status_code == 200:
            response = response.json()["answer"]
        else:
            response = "I'm sorry, but I couldn't process your request."
    except requests.exceptions.RequestException:
        response = "Error: Unable to reach the backend API."
    return response


st.chat_message("assistant", avatar='./assets/alan_kay_profile.jpg')
st.title("Alan Kays Chatbot")
st.write("#### Ask Alan Kay anything...")
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    if message["role"] == 'assistant':
        with st.chat_message("assistant", avatar='./assets/alan_kay_profile.jpg'):
            st.write(message['message'])
    else:
        with st.chat_message("user"):
            st.write(message['message'])


if user_input := st.chat_input("You:", key="user_input"):
    user_message = {"role": "user", "message": user_input}
    st.session_state.chat_history.append(user_message)
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant", avatar='./assets/alan_kay_profile.jpg'):
        status_text = st.empty()
        status_text.markdown("Alan Kay is typing...")
        assistant_response = API_response(API_URL,user_input)
        message_placeholder = st.empty()
        status_text.empty()
        full_response = ""
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response,unsafe_allow_html=True)
        
    chatbot_message = {"role": "assistant", "message": assistant_response}
    st.session_state.chat_history.append(chatbot_message)
    