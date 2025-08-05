# app.py

import streamlit as st
from streamlit_lottie import st_lottie
import requests
from utils.auth import handle_auth
from utils.chat_engine import get_response

# Page configuration
st.set_page_config(
    page_title="MindMate 🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def load_lottie(url: str):
    """Load Lottie animation JSON from URL safely."""
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
        return None
    except Exception:
        return None


# Sidebar for branding
with st.sidebar:
    st.markdown(
        "<h1 style='color:#4e342e;'>🌼 <span style='color:#ff8a80;'>MindMate</span></h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='font-size: 16px; color: #5d4037;'>Your friendly companion for emotional support and wellness.</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")
    lottie_url = "https://assets3.lottiefiles.com/packages/lf20_lpgzixsb.json"
    animation = load_lottie(lottie_url)
    if animation:
        st_lottie(animation, height=200)
    else:
        st.warning("⚠️ Could not load animation.")


# Handle authentication (login/register is outside sidebar)
user = handle_auth()
if not user:
    st.stop()


# Chat UI logic
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("<h2 class='page-title'>🌸 Chat with MindMate</h2>", unsafe_allow_html=True)

# Chat message container
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for chat in st.session_state.chat_history:
    role = chat["role"]
    msg = chat["message"]
    bubble_class = "user-bubble" if role == "user" else "bot-bubble"
    st.markdown(f'<div class="chat-bubble {bubble_class}">{msg}</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Input and send
with st.container():
    user_input = st.text_input("Type your message…", placeholder="How are you feeling today?", key="input")
    send = st.button("Send", use_container_width=True)

if send and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "message": user_input})

    with st.spinner("MindMate is thinking..."):
        reply, score, emotion, suggestion = get_response(
            user_input, emergency_contact=user["emergencyContact"]
        )

    st.session_state.chat_history.append({"role": "assistant", "message": reply})

    if suggestion:
        st.warning(suggestion)

    st.markdown(
        f"<div class='status-bar'>🧠 <b>Stress Score:</b> {score}/100 &nbsp;&nbsp; 😶‍🌫️ <b>Emotion:</b> <i>{emotion}</i></div>",
        unsafe_allow_html=True
    )

    st.rerun()
