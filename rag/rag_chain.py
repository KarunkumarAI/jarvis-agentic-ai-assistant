from core.llm import get_llm
from rag.retriever import retrieve_documents


def ask_documents(
    question: str,
    history: list[dict] | None = None,
) -> str:

    documents = retrieve_documents(question)

    if not documents:
        return "I could not find relevant information in the document."

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    conversation = ""

    if history:
        conversation = "\n".join(
            f"{message['role']}: {message['content']}"
            for message in history[-6:]
        )

    prompt = f"""
    You are JARVIS, a document assistant.

    Answer using the document context below.

    Use the recent conversation when the user's question
    refers to something discussed previously.

    If the answer cannot be found in the document,
    say that clearly.

    Recent conversation:
    {conversation}

    Document context:
    {context}

    Current question:
    {question}
    """

    response = get_llm().invoke(prompt)

    return response.text