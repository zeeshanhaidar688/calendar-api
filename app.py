from flask import Flask, jsonify
from calendar_service import list_upcoming_events, create_test_event

app = Flask(__name__)


@app.route("/calendar/test-list", methods=["GET"])
def calendar_test_list():
    try:
        events = list_upcoming_events(max_results=10)

        formatted = []
        for event in events:
            start = event.get("start", {}).get("dateTime") or event.get("start", {}).get("date")
            formatted.append({
                "id": event.get("id"),
                "summary": event.get("summary"),
                "start": start,
                "htmlLink": event.get("htmlLink")
            })

        return jsonify({
            "ok": True,
            "count": len(formatted),
            "events": formatted
        })
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500


@app.route("/calendar/test-create", methods=["POST"])
def calendar_test_create():
    try:
        event = create_test_event()
        return jsonify({
            "ok": True,
            "event": {
                "id": event.get("id"),
                "summary": event.get("summary"),
                "htmlLink": event.get("htmlLink"),
                "start": event.get("start")
            }
        })
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)