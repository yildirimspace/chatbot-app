# frontend/app.py

try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass


import sys
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import streamlit as st
from crew.main import kickoff_query                     # expects: kickoff_query(query: str, domain_directive: str)
from crew.tasks import DOMAIN_DIRECTIVES                # dict of domain -> directive text


# Page config
st.set_page_config(
    page_title="The Maple Protocol – Canada AI Strategy Assistant",
    layout="wide",
)

# Header with logo
logo_path = os.path.join(CURRENT_DIR, "assets", "maple_protocol_logo.png")

# Make the logo column narrow and reduce the gap between columns
header_col1, header_col2 = st.columns([1, 6], gap="medium")

with header_col1:
    st.write("") 
    if os.path.exists(logo_path):
        st.image(logo_path, width=160)
    else:
        st.write("The Maple Protocol")

with header_col2:
    st.title("The Maple Protocol – Canada AI Strategy Assistant")
    st.caption(
        "MIE 1624 Course Project – Interactive chatbot grounded in our analysis and supporting evidence."
    )

# Sidebar
with st.sidebar:
    st.subheader("How to use this assistant")
    st.markdown(
        "- Ask questions about Canada’s AI strategy, competitiveness, policy, talent, compute, and adoption.\n"
        "- Answers are grounded in our project report and embedded reference material, with citations where available.\n"
        "- If you update the underlying PDFs or data, re-run: `python -m rag.ingest`."
    )

    selected_domain = st.selectbox(
        "Answer focus",
        ["general", "policy", "research", "product", "manufacturing"],
        index=0,
        help="Tailor the answer style and focus to this aspect of AI competitiveness.",
    )

    if st.button("Clear chat", width="stretch"):
        st.session_state.history = []


# Chat state
if "history" not in st.session_state:
    # list[dict]: {"role": "user"|"assistant", "content": str}
    st.session_state.history = []


#  Chat input
prompt = st.chat_input("Ask about Canada’s AI strategy and competitiveness...")
if prompt:
    # Show user message immediately
    st.session_state.history.append({"role": "user", "content": prompt})

    directive = DOMAIN_DIRECTIVES[selected_domain]
    with st.spinner("Thinking..."):
        try:
            answer = kickoff_query(query=prompt, domain_directive=directive)
        except Exception as e:
            answer = f"Sorry, something went wrong: `{e}`"

    st.session_state.history.append({"role": "assistant", "content": str(answer)})


# Render conversation
chatbot_icon_path = os.path.join(CURRENT_DIR, "assets", "chatbot_icon.png")

for msg in st.session_state.history:
    # Determine which icon to show
    if msg["role"] == "assistant":
        avatar_icon = chatbot_icon_path 
    else:
        avatar_icon = None 

    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])


# Quick starter questions
st.divider()
st.caption("Quick Maple Protocol questions:")
cols = st.columns(3)

examples = [
    "Summarize the key findings of this report.",
    "What are the primary goals and objectives?",
    "What is the roadmap for implementation?",
]

for i, ex in enumerate(examples):
    if cols[i % 3].button(ex):
        st.session_state.history.append({"role": "user", "content": ex})

        directive = DOMAIN_DIRECTIVES[selected_domain]
        with st.spinner("Thinking..."):
            try:
                answer = kickoff_query(query=ex, domain_directive=directive)
            except Exception as e:
                answer = f"Sorry, something went wrong: `{e}`"

        st.session_state.history.append({"role": "assistant", "content": str(answer)})
        st.rerun()
