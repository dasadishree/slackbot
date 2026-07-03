# slackbot
Bot tracking my tabs open and publicly humiliating me in my Slack channel if I am on a tab I'm not supposed to be on!!!!

Sends a message in my personal channel every time ur on a new site that is not productive (ie social media)

See #a-dish-ree (private, dm to join) or #publichumiliation on slack to see it working

https://hackclub.enterprise.slack.com/archives/D0BEX62PVJ6

# HOW TO USE
TO START (RUNS IN THE BACKGROUND): cd to the right folder, nohup python3 tracker.py > /dev/null 2>&1 &
TO PAUSE: touch .paused
TO RESUME: rm .paused
TO END: pkill -f tracker.py