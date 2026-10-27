from datetime import datetime, timezone
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/calendar.events.readonly"
]

TOKEN_FILE = "calendar_token.json"


def get_calendar_service():
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
                "credentials.json",
                SCOPES,
            )
            credentials = flow.run_local_server(port=0)

        Path(TOKEN_FILE).write_text(
            credentials.to_json(),
            encoding="utf-8",
        )

    return build(
        "calendar",
        "v3",
        credentials=credentials,
    )


def get_upcoming_events(limit: int = 5) -> list[dict]:
    service = get_calendar_service()

    now = datetime.now(timezone.utc).isoformat()

    result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=limit,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = []

    for event in result.get("items", []):
        start = event["start"].get(
            "dateTime",
            event["start"].get("date"),
        )

        events.append(
            {
                "title": event.get("summary", "No title"),
                "start": start,
                "location": event.get("location", ""),
            }
        )

    return events