from datetime import datetime, timedelta, timezone
from calendar_service import get_calendar_service

if __name__ == "__main__":
    service = get_calendar_service()

    start = datetime.now(timezone.utc) + timedelta(hours=1)
    end = start + timedelta(minutes=30)

    event_body = {
        "summary": "Calendar API Test Event",
        "description": "Created for testing from Python",
        "start": {
            "dateTime": start.isoformat(),
            "timeZone": "UTC"
        },
        "end": {
            "dateTime": end.isoformat(),
            "timeZone": "UTC"
        }
    }

    created_event = service.events().insert(
        calendarId="primary",
        body=event_body
    ).execute()

    print("Event created successfully")
    print("Event ID:", created_event.get("id"))
    print("Event Link:", created_event.get("htmlLink"))