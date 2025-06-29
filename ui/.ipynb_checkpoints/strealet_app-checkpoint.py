"""
Streamlit chat UI for local RAG backend
Run with:  streamlit run streamlit_app.py --server.port 7860
"""

import streamlit as st
import requests
from datetime import datetime

# ------------------ CONFIG ------------------
BACKEND_URL = "http://127.0.0.1:5000/ask"      # Flask route that returns {"answer": ...}
TIMEOUT     = 500                               # seconds
st.set_page_config(page_title="Quantum computing Assistant", page_icon="📑", layout="wide")
# --------------------------------------------

def query_rag_api(prompt: str) -> str:
    """POST the prompt to the RAG backend and return the answer string."""
    try:
        r = requests.post(BACKEND_URL, json={"prompt": prompt}, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json().get("answer", "❌ No 'answer' found in response")
    except Exception as e:
        return f"🚨 Error: {e}"

# Session‑state history ----------------------
if "history" not in st.session_state:
    st.session_state.history = []        # list of (role, msg)
# -------------------------------------------

st.title("Your Quantum computing Assistant")
st.caption("Chat with the Quantum computing assistant via your local LLM‑powered RAG pipeline.")

# Display chat history
for role, msg in st.session_state.history:
    with st.chat_message(role):
        st.markdown(msg, unsafe_allow_html=True)

# User input box (appear at bottom)
if prompt := st.chat_input("Type a question…"):
    # 1) Show user bubble immediately
    st.session_state.history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2) Call backend & stream answer
    placeholder = st.empty()
    with st.chat_message("assistant"):
        msg_container = st.empty()
    assistant_msg = ""

    # You can stream token‑by‑token if your API supports it; here we do one shot
    assistant_msg = query_rag_api(prompt)
    msg_container.markdown(assistant_msg, unsafe_allow_html=True)

    st.session_state.history.append(("assistant", assistant_msg))

st.sidebar.header("Settings")
st.sidebar.markdown(f"Backend URL: `{BACKEND_URL}`")
st.sidebar.markdown(f"Session started at **{datetime.now():%H:%M:%S}**")