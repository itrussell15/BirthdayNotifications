import os
import requests
import urllib.parse
from typing import Iterable

from .models import Birthday

PUSHOVER_APP_TOKEN = os.getenv("PUSHOVER_APP_TOKEN")
PUSHOVER_USER_KEY = os.getenv("PUSHOVER_USER_KEY")


def send_notification(title: str, message: str, url: str | None = None, url_title: str | None = None) -> bool:
    """Send a Pushover notification. Returns True if successful."""
    if not PUSHOVER_APP_TOKEN or not PUSHOVER_USER_KEY:
        print("Pushover not configured; skipping send")
        print(f"APP_TOKEN set: {'yes' if PUSHOVER_APP_TOKEN else 'no'}")
        print(f"USER_KEY set: {'yes' if PUSHOVER_USER_KEY else 'no'}")
        return False
        
    payload = {
        "token": PUSHOVER_APP_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "title": title,
        "message": message,
    }
    
    if url and url_title:
        payload["url"] = url
        payload["url_title"] = url_title
        
    try:
        print(f"Sending Pushover notification with payload: {payload}")
        r = requests.post('https://api.pushover.net/1/messages.json', json=payload, timeout=10)
        print(f"Pushover response status: {r.status_code}")
        print(f"Pushover response body: {r.text}")
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"Failed to send pushover notification: {str(e)}")
        if hasattr(e, 'response'):
            print(f"Error response: {e.response.text}")
        return False

def notify_birthdays(birthdays: Iterable["Birthday"], birthday_timeline: str) -> bool:
    """Notify about birthdays on a specific date."""
    if not birthdays:
        return False
        
    title = "Birthday Alert! 🎂🎉"
    
    successes = []
    for birthday in list(birthdays):
        title_message = f"Your {birthday.relation} {birthday.name} has a birthday {birthday_timeline}!"
        if birthday.custom_message:
            text_message = birthday.custom_message
            url = f"shortcuts://run-shortcut?name=BirthdayText&input={urllib.parse.quote(text_message)}"
            success = send_notification(title, title_message, url=url, url_title="Send them a text!")
        else:
            success = send_notification(title, title_message)
        successes.append(success)
    return all(successes)

