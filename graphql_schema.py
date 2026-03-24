from datetime import datetime, timedelta, timezone
from typing import Optional

import strawberry

from calendar_service import get_calendar_service


@strawberry.type
class CalendarEvent:
    id: str
    summary: str
    start: Optional[str]
    html_link: Optional[str]


@strawberry.type
class AuthStatus:
    authenticated: bool
    message: str


@strawberry.type
class CreateEventResponse:
    ok: bool
    message: str
    event: Optional[CalendarEvent]


def _get_service():
    service = get_calendar_service()
    if service is None:
        raise Exception("Not authenticated. Open /auth/start first.")
    return service


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        return "GraphQL is running"

    @strawberry.field
    def auth_status(self) -> AuthStatus:
        service = get_calendar_service()
        if service is None:
            return AuthStatus(
                authenticated=False,
                message="Not authenticated. Open /auth/start first."
            )
        return AuthStatus(
            authenticated=True,
            message="Authenticated successfully."
        )

    @strawberry.field
    def upcoming_events(self, limit: int = 10) -> list[CalendarEvent]:
        service = _get_service()
        now = datetime.now(timezone.utc).isoformat()

        events_result = service.events().list(
            calendarId="primary",
            timeMin=now,
            maxResults=limit,
            singleEvents=True,
            orderBy="startTime",
        ).execute()

        items = events_result.get("items", [])
        results: list[CalendarEvent] = []

        for event in items:
            start = event.get("start", {}).get("dateTime") or event.get("start", {}).get("date")
            results.append(
                CalendarEvent(
                    id=event.get("id", ""),
                    summary=event.get("summary", "(No title)"),
                    start=start,
                    html_link=event.get("htmlLink"),
                )
            )

        return results


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_test_event(self) -> CreateEventResponse:
        service = _get_service()

        start = datetime.now(timezone.utc) + timedelta(hours=1)
        end = start + timedelta(minutes=30)

        event_body = {
            "summary": "Calendar API GraphQL Test Event",
            "description": "Created from GraphQL mutation",
            "start": {
                "dateTime": start.isoformat(),
                "timeZone": "UTC",
            },
            "end": {
                "dateTime": end.isoformat(),
                "timeZone": "UTC",
            },
        }

        created_event = service.events().insert(
            calendarId="primary",
            body=event_body
        ).execute()

        event = CalendarEvent(
            id=created_event.get("id", ""),
            summary=created_event.get("summary", "(No title)"),
            start=created_event.get("start", {}).get("dateTime"),
            html_link=created_event.get("htmlLink"),
        )

        return CreateEventResponse(
            ok=True,
            message="Event created successfully.",
            event=event,
        )


schema = strawberry.Schema(query=Query, mutation=Mutation)