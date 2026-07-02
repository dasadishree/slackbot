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