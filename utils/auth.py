# utils/auth.py

import streamlit as st
from utils.db import db

def handle_auth():
    st.sidebar.subheader("🔐 Login or Register")

    mode = st.sidebar.radio("Choose action", ["Login", "Register"])

    username = st.sidebar.text_input("Username", key="auth_username")
    password = st.sidebar.text_input("Password", type="password", key="auth_password")

    if mode == "Register":
        emergency = st.sidebar.text_input("Emergency Contact (Optional)", key="emergency")
        if st.sidebar.button("Register"):
            if db.users.find_one({"username": username}):
                st.sidebar.error("Username already exists!")
            else:
                db.users.insert_one({
                    "username": username,
                    "password": password,
                    "emergencyContact": emergency or "None"
                })
                st.sidebar.success("Registered! Please login now.")
    else:
        if st.sidebar.button("Login"):
            user = db.users.find_one({"username": username, "password": password})
            if user:
                st.session_state["user"] = {
                    "username": user["username"],
                    "emergencyContact": user.get("emergencyContact", "None")
                }
                st.sidebar.success(f"Welcome back, {username}!")
                return st.session_state["user"]
            else:
                st.sidebar.error("Invalid credentials.")

    return st.session_state.get("user")
