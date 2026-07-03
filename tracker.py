import time
import requests
from AppKit import NSWorkspace
import subprocess

DISTRACTING_SITES = ["tiktok", "instagram", "youtube", "netflix", "stream", "watch", "pinterest", "slack"]

SHAME_THRESHOLD = 10

def get_active_window_title():
    try:
        script = 'tell application "Google Chrome" to get title of active tab of front window'
        proc = subprocess.Popen(['osascript', '-e', script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if out:
            return f"chrome - {out.decode('utf-8').strip().lower()}"
    except Exception:
        pass
    active_app=NSWorkspace.sharedWorkspace().frontmostApplication()
    if active_app:
        return active_app.localizedName().lower()
    return ""

def send_shame_message(site, total_time):
    minutes = total_time // 60
    seconds = total_time % 60
    time_str = f"{minutes}m {seconds}s" if minutes>0 else f"{seconds}s"

    payload = {
        "text": (
            f"*:siren-real: PUBLIC HUMILIATION: ADISHREE IS SLACKING OFF :siren-real:* \n"
            f"Look who decided to slack off and waste time\n"
            f":caught: Adishree has been caught on *{site.capitalize()}* for *{time_str}* straight.\n"
            f":clown-face: Please drop some clown emojis in the thread to help them stay focused."
        )
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
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
        print(f"[DEBUG] Current Active Window Title: '{window_title}")
        is_distracted = False
        for site in DISTRACTING_SITES:
            if site in window_title:
                is_distracted = True
                if current_distraction != site:
                    current_distraction = site
                    tracked_time=0
                break
        if is_distracted:
            tracked_time += 2
            print(f"Caught on {current_distraction}! Time wasted: {tracked_time}s")

            if tracked_time>=SHAME_THRESHOLD and (time.time() - last_shame_time>30):
                send_shame_message(current_distraction, tracked_time)
                last_shame_time = time.time()
        else:
            if current_distraction:
                print("Back to work! Timer reset.")
            current_distraction = None 
            tracked_time = 0
        
        time.sleep(2)

if __name__ == "__main__":
    main()