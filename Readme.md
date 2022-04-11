# Birthday Notification System

Alert system for when I forget to tell people that I care about Happy Birthday!

## The Problem.

I am notoriously known for only remembering my families birthday and even then, I get too caught up in my own life that I don't realize what day it is and don't remember to  reach out to them. I also try to stay as far away from social media as possible, which has saved me in the past from missing out on reaching out to them. Facebook would send notifications to remind me when peoples birthdays were, but I no longer have the app.

## The Solution.

I wanted a similar notification system to Facebooks birthday notifications, but without Facebook. So I created my own.

## How it works.

Its a really simple system, that is made up of a SQLite database with peoples important dates saved in it. This database gets queried every morning and if there is something today, in 7 days, or 30 days then it will send me a notification to let me know. That way I still have a chance to get them a gift or do whatever preparations are necessary. I have this set up in a docker container on my home server and runs daily via cron.

## Notifications.

I sadly don't know how to write mobile apps, otherwise I would likely build it that way, so I used what I knew which was REST apis and python. I use the  [Pushover API](https://pushover.net/api) to send out my phone notification. You simply send a basic API request and it sends out a notification on your phone.

## Future plans.

Don't tell anyone, but I am hoping to build a messaging system that will actually send people a happy birthday message if I have some parameter that deems them worthy of an auto or pre-generated message. I would still get a notification that my the message was sent, but just would save myself a step if I didn't think I should call or do something that wasn't possible non-programmaticly. Feels a bit not personal, but I think that I would rather send a message than not remember and not do anything.
