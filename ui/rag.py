from pathlib import Path

import streamlit as st

from rag.document_loader import load_document
from rag.rag_chain import ask_documents
from rag.vector_store import create_vector_store


def show_rag() -> None:
    st.subheader("📄 Chat with your PDF")

    if "rag_messages" not in st.session_state:
        st.session_state.rag_messages = []

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
    )

    if uploaded_file:
        Path("data/documents").mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = (
            Path("data/documents")
            / uploaded_file.name
        )

        file_path.write_bytes(
            uploaded_file.getvalue()
        )

        if st.button("Process PDF"):
            try:
                with st.spinner("Processing PDF..."):
                    documents = load_document(
                        str(file_path)
                    )

                    create_vector_store(documents)

                st.session_state.pdf_ready = True

                st.success(
                    f"PDF ready — "
                    f"{len(documents)} chunks indexed."
                )

            except Exception as error:
                st.error(
                    f"PDF processing failed: {error}"
                )

    if not st.session_state.get(
        "pdf_ready",
        False,
    ):
        return

    st.divider()

    for message in st.session_state.rag_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input(
        "Ask something about the PDF...",
        key="rag_chat",
    )

    if question:
        history = st.session_state.rag_messages[-6:]

        st.session_state.rag_messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.write(question)

        try:
            with st.spinner("Searching document..."):
                answer = ask_documents(
                    question,
                    history=history,
                )

        except Exception as error:
            answer = f"RAG failed: {error}"

        st.session_state.rag_messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        with st.chat_message("assistant"):
            st.write(answer)