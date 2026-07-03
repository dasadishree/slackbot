import os
import time
import requests
import subprocess
from AppKit import NSWorkspace
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

DISTRACTING_SITES = ["tiktok", "instagram", "youtube", "netflix", "stream", "watch", "pinterest", "slack"]

def get_active_window_title():
    try:
        script = 'tell application "Google Chrome" to get title of active tab of front window'
        proc = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if out:
            return f"chrome - {out.decode('utf-8').strip()}"
    except Exception:
        pass

    try:
        active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        if active_app:
            return active_app.localizedName()
    except Exception:
        pass
    return ""

def send_shame_message(full_title, strike_count):
    if not WEBHOOK_URL:
        print("Error: SLACK_WEBHOOK_URL is not set!")
        return
    
    display_title = full_title.replace("Chrome -", "")

    payload = {
        "text": (
            f":siren-real: *PUBLIC HUMILIATION: ADISHREE IS SLACKING OFF* :siren-real: \n"
            f":caught: Adishree has been caught on *{display_title}*\n"
            f"This is distraction #*{strike_count}* today. :caught:\n"
        )
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
        print(f"Shame message sent for {display_title} (Strike #{strike_count})")
    except Exception as e:
        print(f"Error sending to Slack: {e}")

def main():
    print("watching")
    distraction_count = 0
    current_distraction = None

    while True:
        window_title = get_active_window_title()
        title_lower = window_title.lower()
        is_distracted = False
        matched_site = None

        for site in DISTRACTING_SITES:
            if site in title_lower:
                is_distracted = True
                matched_site = site
                break
        if is_distracted:
            if current_distraction != matched_site:
                distraction_count += 1
                current_distraction = matched_site
                send_shame_message(window_title, distraction_count)
        else:
            current_distraction = None
        
        time.sleep(2)

if __name__ == "__main__":
    main()