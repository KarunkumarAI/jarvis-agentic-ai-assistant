from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/contacts.readonly"
]

TOKEN_FILE = "contacts_token.json"


def get_contacts_service():
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
        "people",
        "v1",
        credentials=credentials,
    )
def get_contacts(limit: int = 10) -> list[dict]:
    service = get_contacts_service()

    result = (
        service.people()
        .connections()
        .list(
            resourceName="people/me",
            pageSize=limit,
            personFields="names,emailAddresses,phoneNumbers",
        )
        .execute()
    )

    contacts = []

    for person in result.get("connections", []):
        names = person.get("names", [])
        emails = person.get("emailAddresses", [])
        phones = person.get("phoneNumbers", [])

        contacts.append(
            {
                "name": (
                    names[0].get("displayName", "")
                    if names else ""
                ),
                "email": (
                    emails[0].get("value", "")
                    if emails else ""
                ),
                "phone": (
                    phones[0].get("value", "")
                    if phones else ""
                ),
            }
        )

    return contacts

def search_contacts(name: str) -> list[dict]:
    contacts = get_contacts(100)

    keyword = name.lower().strip()

    return [
        contact
        for contact in contacts
        if keyword in contact["name"].lower()
    ]