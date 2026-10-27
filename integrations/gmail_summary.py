from core.llm import get_llm
from integrations.gmail_service import search_emails


def summarize_emails(
    query: str = "in:inbox",
    limit: int = 5,
) -> str:

    emails = search_emails(
        query=query,
        limit=limit,
    )

    if not emails:
        return "No matching emails found."

    email_text = "\n\n".join(
        (
            f"From: {email['from']}\n"
            f"Subject: {email['subject']}\n"
            f"Date: {email['date']}\n"
            f"Preview: {email['snippet']}"
        )
        for email in emails
    )

    prompt = f"""
    Summarize these emails briefly.

    Highlight:
    - important messages
    - anything requiring action
    - deadlines if mentioned

    Emails:

    {email_text}
    """

    response = get_llm().invoke(prompt)

    return response.text