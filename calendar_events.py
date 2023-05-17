import datetime
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials


credentials_file = "credentials.json"
scopes = ["https://www.googleapis.com/auth/calendar.readonly"]
CALENDAR_ID = ""
DAYS = 15


def get_events(calendar_id, days):
    creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
    service = build("calendar", "v3", credentials=creds)
    
    start_date_str, end_date_str = get_start_end_date_str(days)

    events_result = service.events().list(calendarId=calendar_id, timeMin=start_date_str, timeMax=end_date_str,
                                          singleEvents=True, orderBy="startTime").execute()
    return events_result.get("items", [])


def get_start_end_date_str(days):
    today = datetime.date.today()
    start_date = today + datetime.timedelta(days=1)
    end_date = today + datetime.timedelta(days=days + 1)

    return (start_date.isoformat() + "T00:00:00Z", end_date.isoformat() + "T23:59:59Z")


def print_events(events):
    if not events:
        print("No se encontraron eventos en las próximas dos semanas.")
        return

    print(":palm_tree: :palm_tree: Holidays during the next two weeks :palm_tree: :palm_tree:")
    for event in events:
        start = event["start"].get("date")
        end = event["end"].get("date")
        end = date_str_minus_one_day(end)

        range_str = f"{start}"
        if start != end:
            range_str = f"{start} -> {end}"

        print(f"{range_str}: {event['summary']}")


def date_str_minus_one_day(date):
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    date = date - datetime.timedelta(days=1)
    return date.strftime("%Y-%m-%d")


if __name__ == "__main__":
    events = get_events(CALENDAR_ID, DAYS)
    print_events(events)
