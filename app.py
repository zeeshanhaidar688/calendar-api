from datetime import datetime, timedelta, timezone

from flask import Flask, jsonify, redirect, request, session, url_for

from calendar_service import create_oauth_flow, get_calendar_service, save_credentials

app = Flask(__name__)
app.secret_key = "replace-this-with-a-random-secret-key"


@app.route("/", methods=["GET"])
def home():
    return """
    <h2>Google Calendar API</h2>
    <p><a href="/auth/start">Connect Google Calendar</a></p>
    <p><a href="/calendar_test_list">List Events</a></p>
    <p>Use POST /calendar_test_create to create a test event.</p>
    """


@app.route("/auth/start", methods=["GET"])
def auth_start():
    flow = create_oauth_flow()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )

    session["oauth_state"] = state
    return redirect(authorization_url)


@app.route("/auth/callback", methods=["GET"])
def auth_callback():
    state = session.get("oauth_state")
    if not state:
        return "Missing OAuth state in session.", 400

    flow = create_oauth_flow()
    flow.state = state

    flow.fetch_token(authorization_response=request.url)

    creds = flow.credentials
    save_credentials(creds)

    return """
    <h3>Authentication successful</h3>
    <p>Your Google Calendar is now connected.</p>
    <p><a href="/calendar_test_list">Test list events</a></p>
    """


@app.route("/calendar_test_list", methods=["GET"])
def calendar_test_list():
    service = get_calendar_service()
    if service is None:
        return jsonify({
            "ok": False,
            "error": "Not authenticated. Open /auth/start first."
        }), 401

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
        "count": len(formatted_events),
        "events": formatted_events
    })


@app.route("/calendar_test_create", methods=["POST"])
def calendar_test_create():
    service = get_calendar_service()
    if service is None:
        return jsonify({
            "ok": False,
            "error": "Not authenticated. Open /auth/start first."
        }), 401

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
        "event": {
            "id": created_event.get("id"),
            "summary": created_event.get("summary"),
            "htmlLink": created_event.get("htmlLink"),
            "start": created_event.get("start")
        }
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)