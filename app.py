from flask import Flask, jsonify
from datetime import datetime, timedelta, timezone

from calendar_service import (
    get_calendar_service,
    USE_MOCK,
    mock_list_events,
    mock_create_event
)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    mode = "MOCK MODE" if USE_MOCK else "REAL MODE"
    return f"Google Calendar API is running ({mode})"


# ==============================
# LIST EVENTS
# ==============================
@app.route("/calendar_test_list", methods=["GET"])
def calendar_test_list():
    try:
        if USE_MOCK:
            events = mock_list_events()
            return jsonify({
                "ok": True,
                "mode": "mock",
                "count": len(events),
                "events": events
            })

        # REAL MODE
        service = get_calendar_service()
        now = datetime.now(timezone.utc).isoformat()

        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        events = events_result.get("items", [])

        formatted_events = []
        for event in events:
            start = event.get("start", {}).get("dateTime") or event.get("start", {}).get("date")
            formatted_events.append({
                "id": event.get("id"),
                "summary": event.get("summary", "(No title)"),
                "start": start,
                "htmlLink": event.get("htmlLink")
            })

        return jsonify({
            "ok": True,
            "mode": "real",
            "count": len(formatted_events),
            "events": formatted_events
        })

    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500


# ==============================
# CREATE EVENT
# ==============================
@app.route("/calendar_test_create", methods=["POST"])
def calendar_test_create():
    try:
        if USE_MOCK:
            event = mock_create_event()
            return jsonify({
                "ok": True,
                "mode": "mock",
                "event": event
            })

        # REAL MODE
        service = get_calendar_service()

        start = datetime.now(timezone.utc) + timedelta(hours=1)
        end = start + timedelta(minutes=30)

        event_body = {
            "summary": "Calendar API Test Event",
            "description": "Created from Flask endpoint",
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

        return jsonify({
            "ok": True,
            "mode": "real",
            "event": created_event
        })

    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)