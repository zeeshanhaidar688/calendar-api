import json
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ==============================
# CONFIG
# ==============================
USE_MOCK = False  # 🔥 Toggle this (True = mock, False = real)

SCOPES = ["https://www.googleapis.com/auth/calendar"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")


# ==============================
# REAL GOOGLE SERVICE
# ==============================
def get_calendar_service():
    if USE_MOCK:
        return None  # Not used in mock mode

    creds = None

    if not os.path.exists(CREDENTIALS_FILE):
        raise FileNotFoundError(
            f"credentials.json not found at: {CREDENTIALS_FILE}"
        )

    with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    if "installed" not in cfg and "web" not in cfg:
        raise ValueError(
            "credentials.json must be an OAuth client file."
        )

    if os.path.exists(TOKEN_FILE):
        try:
            if os.path.getsize(TOKEN_FILE) > 0:
                creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            else:
                os.remove(TOKEN_FILE)
        except Exception:
            try:
                os.remove(TOKEN_FILE)
            except Exception:
                pass

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


# ==============================
# MOCK DATA
# ==============================
def mock_list_events():
    return [
        {
            "id": "mock-1",
            "summary": "Mock Team Meeting",
            "start": "2026-03-25T10:00:00",
            "htmlLink": "https://calendar.google.com/mock1"
        },
        {
            "id": "mock-2",
            "summary": "Project Demo",
            "start": "2026-03-26T14:00:00",
            "htmlLink": "https://calendar.google.com/mock2"
        }
    ]


def mock_create_event():
    return {
        "id": "mock-created-123",
        "summary": "Mock Created Event",
        "htmlLink": "https://calendar.google.com/mock-created",
        "start": {
            "dateTime": "2026-03-27T12:00:00"
        }
    }