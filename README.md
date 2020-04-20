# Timeoff Bot

Zulip Bot of managers to organize and manage requests for work-from-home, sick leave, vacations and other holidays from zulip

[timeoff](./timeoff) contains the code for the zulip bot

[timeoff_api] contains an api that acts as a backend for the bot which is built on flask.

## Things to do

- [x] Create an API
- [x] Create a bot that interacts with api
- [ ] Add more functionality to determine who can access what data
- [ ] Add functionality so people can view_requests more easily (filter by sender or dates)

## How to run this bot

If you want to deploy your own clone this repo, obtain a zuliprc from zulipchat.com and put it into the timeoff folder. Now, type in these commands to deploy to heroku:

- `heroku create` - creates an app instance on heroku
- commit the zuliprc file, `git add .; git commit -m 'zuliprc added'`
-  `git push heroku master`
- `heroku dyno:scale worker=1` assign a worker dyno so that the app is online 24/7

## Contributors

[Ryan Rozario](https://github.com/ryan-rozario)
[Ankit Raut](https://github.com/ankitraut12379)