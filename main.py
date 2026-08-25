import requests
import os
import json
from datetime import date, timedelta

BASE_URL = "https://adminbooking.gopichandacademy.com/API/Get/Calender"
HEADERS = {"User-Agent": "Mozilla/5.0"}
VENUE_IDS = [1, 2, 3]
STATE_FILE = "state.json"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]


def get_weekend_dates_this_week():
    """Return Saturday & Sunday of the current week, skipping any already past."""
    today = date.today()
    monday = today - timedelta(days=today.weekday())  # Monday of this week
    saturday = monday + timedelta(days=5)
    sunday = monday + timedelta(days=6)
    return [d.strftime("%Y-%m-%d") for d in (saturday, sunday) if d >= today]


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def get_calendar(venue_id, date_str):
    params = {"venue_id": venue_id, "date": date_str}
    resp = requests.get(BASE_URL, headers=HEADERS, params=params)
    resp.raise_for_status()
    return resp.json()


def parse_available_slots(court_data):
    """
    court_available_slots entries look like: "13:00-14:00|1|405"
    Format: time|available_flag|price   (available_flag: 1 = open, 0 = booked)
    Returns a list of open time slots, e.g. ["13:00-14:00", "14:00-15:00"]
    """
    open_slots = []
    for entry in court_data.get("court_available_slots", []):
        if not entry:  # handles the [""] "not opened yet" case
            continue
        parts = entry.split("|")
        if len(parts) != 3:
            continue
        time_range, available_flag, _price = parts
        if available_flag == "1":
            open_slots.append(time_range)
    return open_slots


def main():
    state = load_state()
    dates_to_check = get_weekend_dates_this_week()

    if not dates_to_check:
        print("No upcoming weekend days left this week. Nothing to check.")
        return

    for venue_id in VENUE_IDS:
        for date_str in dates_to_check:
            try:
                data = get_calendar(venue_id, date_str)
            except Exception as e:
                print(f"Failed to fetch venue {venue_id} on {date_str}: {e}")
                continue

            if data.get("Status") != "Success":
                print(f"API returned non-success for venue {venue_id} on {date_str}: {data}")
                continue

            result = data.get("Result", {})

            for court_id, court_data in result.items():
                court_name = court_data.get("court_name", court_id)
                open_slots = parse_available_slots(court_data)

                state_key = f"v{venue_id}_d{date_str}_c{court_id}"
                previously_seen = set(state.get(state_key, []))
                currently_open = set(open_slots)

                new_slots = currently_open - previously_seen

                if new_slots:
                    message = (
                        f"🏸 New slot(s) opened!\n"
                        f"Venue: {venue_id} | Court: {court_name}\n"
                        f"Date: {date_str}\n"
                        f"Time(s): {', '.join(sorted(new_slots))}"
                    )
                    print(message)
                    send_telegram(message)
                else:
                    print(f"Venue {venue_id}, Court {court_name}, {date_str}: no new slots.")

                # Update state with whatever is currently open (so next run compares correctly)
                state[state_key] = sorted(currently_open)

    save_state(state)


if __name__ == "__main__":
    main()
