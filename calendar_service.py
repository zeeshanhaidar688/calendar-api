import json
import os
import secrets

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, "credentials.json")
TOKEN_FILE = os.path.join(BASE_DIR, "token.json")
REDIRECT_URI = "http://127.0.0.1:5000/auth/callback"


def create_oauth_flow(state=None, code_verifier=None):
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI,
        code_verifier=code_verifier,
    )
    return flow


def generate_code_verifier():
    # PKCE verifier must be 43-128 chars
    return secrets.token_urlsafe(64)[:100]


def save_credentials(creds: Credentials):
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        f.write(creds.to_json())


def load_credentials():
    if not os.path.exists(TOKEN_FILE):
        return None

    try:
        if os.path.getsize(TOKEN_FILE) == 0:
            os.remove(TOKEN_FILE)
            return None

        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            save_credentials(creds)

        return creds
    except Exception:
        try:
            os.remove(TOKEN_FILE)
        except Exception:
            pass
        return None


def get_calendar_service():
    creds = load_credentials()
    if not creds or not creds.valid:
        return None

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