import time
import requests
from AppKit import NSWorkspace

DISTRACTING_SITES = ["tiktok", "instagram", "youtube", "netflix", "stream", "watch", "pinterest", "slack"]

SHAME_THRESHOLD = 10

def get_active_window_title():
    active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
    if active_app:
        return active_app.localizedName().lower()
    return ""

def send_shame_message(site, total_time):
    minutes = total_time // 60
    seconds = total_time % 60
    time_str = f"{minutes}m {seconds}s" if minutes>0 else f"{seconds}s"

    payload = {
        "text": (
            f"*PUBLIC HUMILIATION: ADISHREE IS SLACKING OFF* \n"
            f"Look who decidedto slack off and waste time\n"
            f"Adishree has been caught on *{site.capitalize()}* for *{time_str}* straight."
            f"Please drop some clown emojis in the thread to help them stay focused."
        )
    }
    try:
        request.post(WEBHOOK_URL, json=payload)
        print(f"Shame message sent for {site}")
    except Exception as e:
        print(f"Error sending to Slack: {e}")

def main():
    print("watching")
    tracked_time = 0
    current_distraction = None
    last_shame_time = 0

    while True:
        window_title = get_active_window_title()
        is_distracted = False
        for site in DISTRACTING_SITES:
            if site in window_title:
                is_distracted = True
                if current_distraction != site:
                    current_distraction = site
                    tracked_time=0
                break
