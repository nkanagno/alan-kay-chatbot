
import streamlit as st
import time
import requests
import os
import base64
from PIL import Image
from io import BytesIO

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

def get_circular_image_html(image_path, width=150):
    try:
        img = Image.open(image_path)
        
        # Convert to HTML
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        # HTML with CSS for circular image
        html = f'''
        <div style="display: flex; flex-direction: row; justify-content: flex-start; margin-bottom:20px;">
            <div style="width:100px;">
                <img src="data:image/png;base64,{img_str}" 
                    style="border-radius:50%; width:{width}px; height:{width}px; object-fit:cover;">
            </div>
            <div style="margin-left:30%;">
                <h1>Alan Kay</h1>
                <h5 style='color: grey;'>American computer scientist</h5>
            </div>
        </div>
        '''
        return html
    except Exception as e:
        return f"<div>Error loading image: {e}</div>"


with st.sidebar:
    st.markdown(get_circular_image_html('./assets/alan_kay_profile.jpg'), unsafe_allow_html=True)
    st.write("# Profile:")
    st.write("""I was born on May 17, 1940. Pioneer in object-oriented programming and windowing graphical user interfaces. Led the development of the first modern windowed computer desktop at Xerox PARC. Created the Smalltalk programming language and coined the term "object-oriented." Currently a computer scientist with decades of experience in software development. Recipient of the 2003 Turing Award and Fellow of the American Academy of Arts and Sciences, National Academy of Engineering, and Royal Society of Arts.""")




# Spacing to prevent overlap

st.markdown('<h1 class="chat-title">AI Chatbot</h1>', unsafe_allow_html=True)

# Scrollable chat messages container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)


if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    if message["role"] == 'assistant':
        with st.chat_message("assistant", avatar='./assets/alan_kay_profile.jpg'):
            st.write(message['message'])
    else:
        with st.chat_message("user"):
            st.write(message['message'])
st.markdown('</div>', unsafe_allow_html=True)

if user_input := st.chat_input("Ask me anything...", key="user_input"):
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
