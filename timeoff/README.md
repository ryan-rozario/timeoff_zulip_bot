# Timeoff Bot 

This bot allows you to request, review and approve time off.

Any Employee can send a leave request to his manager.
The manager can then approve of the leave request.

Zulip provides a great platform where people can interact and plan in an effective way. The zulip bot acts as a ready interface so that people can discuss and analyse the information from the comfort of zulip, all from one single app, no need to switch between apps. Also, the bot's reply provides context for others.

## Commands

In a private message we can use the following:

```text
create_request type:<vacation/sick leave/work from home>, details:<details>, start :DD/MM/YY, end:DD/MM/YY, manager:<manager email related to zulip account>

approve_request <application number>

view_requests sent

view_requests received

list_commands
```

## How to run this bot

If you want to deploy your own clone this repo, obtain a zuliprc from zulipchat.com and put it here. Now, type in these commands to deploy to heroku:

- `heroku create` - creates an app instance on heroku
- commit the zuliprc file, `git add .; git commit -m 'zuliprc added'`
-  `git push heroku master`
- `heroku dyno:scale worker=1` assign a worker dyno so that the app is online 24/7