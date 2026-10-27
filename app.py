import streamlit as st

from core.config import APP_NAME
from core.logger import setup_logger
from memory.sqlite_memory import initialize_memory
from ui.chat import show_chat
from ui.sidebar import show_sidebar
from ui.vision import show_vision
from ui.rag import show_rag

logger = setup_logger()
initialize_memory()

st.set_page_config(
    page_title=APP_NAME,
    page_icon="🤖",
    layout="wide",
)

show_sidebar()

st.title(f"🤖 {APP_NAME}")
st.caption("Multimodal Agentic Desktop AI Assistant")

chat_tab, rag_tab, vision_tab = st.tabs(
    ["💬 Chat", "📄 Documents", "👁️ Vision"]
)

with chat_tab:
    show_chat()
    
with rag_tab:
    show_rag()

with vision_tab:
    show_vision()

logger.info("JARVIS application running")