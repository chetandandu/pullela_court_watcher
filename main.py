import requests
import os
import json

URL = "https://adminbooking.gopichandacademy.com/API/Get/Calender?venue_id=3&date=2026-07-18"
HEADERS = {"User-Agent": "Mozilla/5.0"}
PARAMS = {"date": "2026-07-20"}

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def get_availability():
    resp = requests.get(URL, headers=HEADERS, params=PARAMS)
    resp.raise_for_status()
    return resp.json()

def main():
    data = get_availability()
    open_slots = [s for s in data.get("slots", []) if s.get("available")]
    if open_slots:
        send_telegram(f"Open slots found: {open_slots}")
    else:
        print("No slots available right now.")

if __name__ == "__main__":
    main()
