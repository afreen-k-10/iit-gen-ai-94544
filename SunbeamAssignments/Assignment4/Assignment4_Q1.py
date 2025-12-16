import streamlit as st
import time
if 'messages' not in st.session_state:
    st.session_state.messages = []
st.title(" Afreen's Chatbot~~")
def stream_text(text):
    for word in text.split():
        yield word+ " "
        time.sleep(0.1)
for chat in st.session_state.messages:
    with st.chat_message(chat["role"]):
        st.write(chat["content"])
msg = st.chat_input("Say something....")
if msg:
    with st.chat_message("User"):
        st.write(msg)
    st.session_state.messages.append({"role" : "user","content": msg})
    response = f"{msg}"
    with st.chat_message("assistant"):
        st.write_stream(stream_text(response))
    st.session_state.messages.append({"role" : "assistant","content": response})