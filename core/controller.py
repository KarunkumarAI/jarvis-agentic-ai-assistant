from core.llm import (
    ask_jarvis,
    extract_email_request,
)

from agent.graph import run_agent

from integrations.gmail_summary import summarize_emails
from integrations.gmail_service import send_email
from integrations.calendar_service import get_upcoming_events
from integrations.contacts_service import search_contacts

from memory.sqlite_memory import (
    get_memories,
    save_memory,
)

from rag.rag_chain import ask_documents

from core.pending_email import (
    clear_pending_email,
    get_pending_email,
    set_pending_email,
)


def handle_request(
    user_input: str,
    history: list[dict] | None = None,
) -> str:

    text = user_input.lower().strip()

    # --------------------------------------------------
    # EMAIL - CONFIRM SEND
    # --------------------------------------------------
    if text == "confirm email":
        email = get_pending_email()

        if email is None:
            return "There is no email waiting for confirmation."

        try:
            result = send_email(
                to_email=email.to_email,
                subject=email.subject,
                body=email.body,
            )

            clear_pending_email()

            return result

        except Exception as error:
            return f"Email sending failed: {error}"

    # --------------------------------------------------
    # EMAIL - CANCEL
    # --------------------------------------------------
    if text == "cancel email":
        clear_pending_email()
        return "Email cancelled."

    # --------------------------------------------------
    # EMAIL - SEND REQUEST
    # --------------------------------------------------
    if text.startswith("send email"):
        try:
            email = extract_email_request(user_input)

            set_pending_email(email)

            return (
                "Please confirm this email:\n\n"
                f"To: {email.to_email}\n"
                f"Subject: {email.subject}\n\n"
                f"{email.body}\n\n"
                "Type 'confirm email' to send it.\n"
                "Type 'cancel email' to cancel."
            )

        except Exception as error:
            return f"Could not prepare email: {error}"

    # --------------------------------------------------
    # GMAIL - READ / SUMMARIZE
    # --------------------------------------------------
    if (
        "inbox" in text
        or "summarize emails" in text
        or "summarise emails" in text
    ):
        return summarize_emails(
            query="in:inbox",
            limit=5,
        )

    # --------------------------------------------------
    # CALENDAR
    # --------------------------------------------------
    if (
        "calendar" in text
        or "upcoming events" in text
    ):
        return format_calendar_events()

    # --------------------------------------------------
    # CONTACTS
    # --------------------------------------------------
    if text.startswith("find contact"):
        name = user_input[
            len("find contact"):
        ].strip()

        if not name:
            return "Please provide a contact name."

        return format_contacts(name)

    # --------------------------------------------------
    # MEMORY - SAVE
    # --------------------------------------------------
    if text.startswith("remember:"):
        content = user_input.split(
            ":",
            1,
        )[1].strip()

        if not content:
            return "Tell me what you want me to remember."

        return save_memory(
            category="user_note",
            content=content,
        )

    # --------------------------------------------------
    # MEMORY - READ
    # --------------------------------------------------
    if text in {
        "show memories",
        "what do you remember",
    }:
        return format_memories()

    # --------------------------------------------------
    # RAG
    # --------------------------------------------------
    if text.startswith("ask document:"):
        question = user_input.split(
            ":",
            1,
        )[1].strip()

        if not question:
            return "Please enter a question about the document."

        return ask_documents(
            question,
            history=history,
        )

    # --------------------------------------------------
    # DESKTOP / BROWSER AGENT
    # --------------------------------------------------
    action_words = (
        "open ",
        "search google",
        "search youtube",
        "scroll down",
        "go back",
        "close browser",
    )

    if text.startswith(action_words):
        return run_agent(user_input)

    # --------------------------------------------------
    # NORMAL GEMINI CHAT
    # --------------------------------------------------
    return ask_jarvis(
        user_input,
        history=history,
    )


def format_calendar_events() -> str:
    events = get_upcoming_events(5)

    if not events:
        return "You have no upcoming events."

    return "\n".join(
        f"- {event['title']} - {event['start']}"
        for event in events
    )


def format_contacts(name: str) -> str:
    contacts = search_contacts(name)

    if not contacts:
        return f"I couldn't find a contact named {name}."

    return "\n".join(
        (
            f"- {contact['name']} | "
            f"{contact['email']} | "
            f"{contact['phone']}"
        )
        for contact in contacts
    )


def format_memories() -> str:
    memories = get_memories(10)

    if not memories:
        return "I don't have any saved memories."

    return "\n".join(
        f"- {memory[2]}"
        for memory in memories
    )