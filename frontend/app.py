import streamlit as st
import requests

st.title("ChatBot Frontend")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input and backend communication
if prompt := st.chat_input("Message"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = requests.post(
                "http://localhost:5000/chat",
                json={"messages": st.session_state.messages},
                timeout=15  # Optional: prevent hanging
            )
            response.raise_for_status()  # Raise an error for bad HTTP status
            data = response.json()
            reply = data.get("reply", "No reply received from backend.")
        except requests.exceptions.RequestException as e:
            reply = f"API Error: {str(e)}"
        except Exception as e:
            reply = f"Unexpected Error: {str(e)}"
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
