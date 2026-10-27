from langchain_google_genai import ChatGoogleGenerativeAI

from models.schemas import AssistantResponse
from core.config import GOOGLE_API_KEY
from models.schemas import AssistantResponse, EmailRequest


def get_llm() -> ChatGoogleGenerativeAI:
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=GOOGLE_API_KEY,
    )


def ask_jarvis(
    question: str,
    history: list[dict] | None = None,
) -> str:

    messages = []

    if history:
        for message in history[-10:]:
            role = (
                "human"
                if message["role"] == "user"
                else "ai"
            )

            messages.append(
                (role, message["content"])
            )

    messages.append(
        ("human", question)
    )

    response = get_llm().invoke(messages)

    return response.text


def understand_command(command: str) -> AssistantResponse:
    llm = get_llm()

    structured_llm = llm.with_structured_output(
        AssistantResponse
    )

    return structured_llm.invoke(
        f"""
        Understand this JARVIS command.

        Command: {command}

        Return the user's intent, target,
        and a short response.
        """
    )

def extract_email_request(command: str) -> EmailRequest:
    structured_llm = get_llm().with_structured_output(
        EmailRequest
    )

    return structured_llm.invoke(
        f"""
        Extract an email from this user request.

        User request:
        {command}

        Return:
        - to_email
        - subject
        - body

        Do not add placeholders.
        Keep the email natural and concise.
        """
    )