# Birthday Notification System

Alert system before I forget to tell people that I care about Happy Birthday!

## The Problem.

I am notoriously known for only remembering my families birthday and even then, I get too caught up in my own life that I don't realize what day it is and don't remember to  reach out to them. I also try to stay as far away from social media as possible, which has saved me in the past from missing out on reaching out to them. Facebook would send notifications to remind me when peoples birthdays were, but I no longer have the app.

## The Solution.

I wanted a similar notification system to Facebooks birthday notifications, but without Facebook. So I created my own.

## How it works.

Its a really simple system, that is made up of a SQLite database with peoples important dates saved in it. This database gets queried every morning and if there is something today, in 7 days, or 30 days then it will send me a notification to let me know. That way I still have a chance to get them a gift or do whatever preparations are necessary. I have a cron job running on my computer everyday pointing to the shell script to run the programs in this repo.

## Notifications.

I sadly don't know how to write mobile apps, otherwise I would likely build it that way, so I used what I knew which was REST apis and python. I use the [Pushover API](https://pushover.net/api) to send out my phone notification. You simply send a basic API request and it sends out a notification on your phone. My database has a column to preload a custom message that I would like to send if it is the day of their birthday. On the day of their birthday the pushover app will have a link to this message as a shortcut that I have preloaded on my phone. I select the contact associated with that birthday notification and press send!

## Auto Updating

I wanted to be able to modify my database somewhat easily as I find out when their birthdays. I have stored all the birthdays in a csv file and can modify this csv to reflect what is in my SQL file. Every time the program runs, it checks for changes in the csv and updates the SQL database to reflect these changes. We also store a backup instance of the DB file every time we modify it so that I can roll back if something bad happens and my database is in a bad spot. This just makes it easier for me to manage all the dates and make sure I don't forget people that I want to reach out to. You can see the example csv file that I store information in.

## Future plans.

I have a feeling that the messages may get a bit spammy with 3 messages per date especially as my DB continues to grow. I want to add another column in the DB that will just allow me to send a single message when it is a person I want to simply say happy birthday to and don't need a warning for a gift or time to prepare something for them. For example, I want to have a heads up that my mom's birthday is in a month, but I don't really need to know that about my coworker. I just don't want to work with them and find out it is their birthday at the end of the day.

I have also thought about adding special dates that aren't necessarily birthdays. Maybe anniversaries or other special dates that I would want reminders for just as a personal reminder or to reach out to people that are celebrating something. The logic would be similar, but I would want another database these dates would live in.
