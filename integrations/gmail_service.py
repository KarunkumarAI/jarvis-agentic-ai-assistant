from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


def get_gmail_service():
    credentials = None

    if Path(TOKEN_FILE).exists():
        credentials = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES,
        )

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES,
            )

            credentials = flow.run_local_server(port=0)

        Path(TOKEN_FILE).write_text(
            credentials.to_json(),
            encoding="utf-8",
        )

    return build(
        "gmail",
        "v1",
        credentials=credentials,
    )
def search_emails(
    query: str = "in:inbox",
    limit: int = 5,
) -> list[dict]:

    service = get_gmail_service()

    result = (
        service.users()
        .messages()
        .list(
            userId="me",
            q=query,
            maxResults=limit,
        )
        .execute()
    )

    messages = result.get("messages", [])

    emails = []

    for message in messages:
        data = (
            service.users()
            .messages()
            .get(
                userId="me",
                id=message["id"],
                format="metadata",
                metadataHeaders=[
                    "From",
                    "Subject",
                    "Date",
                ],
            )
            .execute()
        )

        headers = {
            header["name"]: header["value"]
            for header in data["payload"]["headers"]
        }

        emails.append(
            {
                "id": message["id"],
                "from": headers.get("From", "Unknown"),
                "subject": headers.get(
                    "Subject",
                    "No Subject",
                ),
                "date": headers.get("Date", ""),
                "snippet": data.get("snippet", ""),
            }
        )

    return emails

import base64
from email.mime.text import MIMEText


def send_email(
    to_email: str,
    subject: str,
    body: str,
) -> str:
    service = get_gmail_service()

    message = MIMEText(body)
    message["to"] = to_email
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw_message},
    ).execute()

    return f"Email sent successfully to {to_email}."