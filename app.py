import streamlit as st
from agent import run_query
from db import get_db

st.set_page_config(
    page_title="Text-to-SQL Bot",
    page_icon="🗄️",
    layout="wide"
)

st.title("Text-to-SQL Bot")
st.markdown("Powered by **Hugging Face (Qwen 2.5 Coder)** — Ask questions in plain English.")

# Sidebar
with st.sidebar:
    st.header("Database Info")
    @st.cache_resource
    def _cached_get_db():
        return get_db()

    try:
        db = _cached_get_db()
        tables = db.get_table_names()
        st.success("Connected: chinook.db")
        st.markdown("**Tables available:**")
        for t in tables:
            st.markdown(f"- `{t}`")
    except Exception as e:
        st.error(f"DB connection failed: {e}")

    st.divider()
    st.markdown("**Example questions:**")
    examples = [
        "Show top 5 customers by total spending",
        "Which genre has the most tracks?",
        "How many albums per artist?",
        "List all invoices above $15",
        "Which country has the most customers?",
        "Show all tracks longer than 5 minutes",
        "Top 3 selling artists by invoice total",
    ]
    for ex in examples:
        if st.button(ex, key=ex):
            st.session_state["prefill"] = ex

    st.divider()
    st.caption("Model: Qwen/Qwen2.5-Coder-32B-Instruct")
    st.caption("DB: Chinook SQLite")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prefill = st.session_state.pop("prefill", None)
user_input = st.chat_input("Ask a question about your data...") or prefill

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Hugging Face is generating SQL..."):
            response = run_query(user_input)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})