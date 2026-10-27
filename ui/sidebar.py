import streamlit as st


def show_sidebar() -> None:
    with st.sidebar:
        st.header("JARVIS Status")

        st.success("System Online")
        st.success("LLM Online")
        st.success("Voice Online")

        st.success("Vision Online")
        st.info("Agent: Not configured")
        st.info("Qdrant: Not configured")

        st.divider()

        st.toggle(
            "Voice Response",
            value=False,
            key="voice_enabled",
        )

        if st.button("Clear Chat"):
            st.session_state.messages = []
            st.session_state.pop("last_audio", None)
            st.rerun()