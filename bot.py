import os 
import re
from datetime import datetime
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from apscheduler.schedulers.background import BackgroundScheduler

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

daily_tracker = {}
MY_USER_ID = "U07DBE2RUL"

# aura command
@app.command("/aura")
def handle_aura(ack, respond, command):
    ack()
    user_id=command['user_id']
    text=command['text'].strip()
    match=re.match(r"^([+-]?\d+)\s+(.*)$", text)
    if not match:
        respond("Oops! Please use the format: `/aura +50 text` or `/aura -50 text`")
        return
    points = int(match.group(1))
    reason = match.group(2)
    if user_id not in daily_tracker:
        daily_tracker[user_id] = {"score":0, "history":[]}
    
    daily_tracker[user_id]["score"] += points
    daily_tracker[user_id]["history"].append(f"{'+' if points > 0 else ''}{points}: {reason}")

    current_total = daily_tracker[user_id]["score"]

    respond(f"Aura logged! Total today: *{current_total}* points.")

# daily summary every night 9pm: ask u to rate ur day out of 10, summarize, share pic/video, and give daily/total aura point count
def send_nightly_checkin():
    user_id = MY_USER_ID
    score = 0
    history_text = "No events logged today."

    if user_id in daily_tracker:
        score = daily_tracker[user_id]["score"]
        if daily_tracker[user_id]["history"]:
            history_text = "\n".join(daily_tracker[user_id]["history"])
    
    if score>=200:
        tier = "GOAT"
    elif score>=50:
        tier = "Auramaxxer"
    elif score>=0:
        tier = "Mid"
    else:
        tier = "Clown"

    message=(
        f"Daily Aura Summary \n\n"
        f"*Today's Log:*\n{history_text}\n\n"
        f"Total Aura Points: *{score}*\n"
        f"Current Tier: *{tier}*\n\n"
        f"Rate today out of 10, share what you did and a photo/video if you want!"
    )

    try:
        app.client.chat_postMessage(channel=user_id, text=message)
    except Exception as e:
        print(f"Error sending message: {e}")
    if user_id in daily_tracker:
        daily_tracker[user_id] = {"score": 0, "history": []}

# schedule
scheduler = BackgroundScheduler()
scheduler.add_job(send_nightly_checkin, 'cron', hour=21,minute=0)
scheduler.start()

if __name__ == "__main__":
    print("bot is running")
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
    