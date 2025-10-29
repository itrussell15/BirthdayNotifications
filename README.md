# Birthday Notifier

Dockerized FastAPI service to store birthdays and send daily notifications (via Telegram) when it's someone's birthday.

Features
- REST API to create, read, update, delete birthdays
- SQLite database (file) inside container
- Daily scheduler that checks for today's birthdays and sends Telegram messages

Environment
- See `.env.example` for required variables. You need a Pushover application token and user key.

Run (Docker Compose)
1. Copy `.env.example` to `.env` and fill in your Pushover tokens.
2. Build and run:

```bash
docker compose up --build -d
```

API
- GET /health
- GET /birthdays
- POST /birthdays
- GET /birthdays/{id}
- PUT /birthdays/{id}
- DELETE /birthdays/{id}

Testing notifications
- POST /notify — triggers the birthday check immediately (handy for testing)

Setup Pushover
1. Create an account at pushover.net if you haven't already
2. Create a new application at https://pushover.net/apps/build
3. Get your user key from your dashboard
4. Add both tokens to your .env file:
   - PUSHOVER_APP_TOKEN: Your application's API token
   - PUSHOVER_USER_KEY: Your user keyExample requests (replace host/port accordingly):

# Web Interface

## Add birthdays via a form
![add_birthday](https://github.com/itrussell15/BirthdayNotifications/blob/master/images/add_birthday.png)

## View current birthdays that have been entered
![show_birthdays](https://github.com/itrussell15/BirthdayNotifications/blob/master/images/birthday_list.png)

Create a birthday:

```bash
curl -X POST http://localhost:8000/birthdays \
	-H 'Content-Type: application/json' \
	-d '{"name": "Alice", "date": "1990-10-22"}'
```

Trigger notification now (test):

```bash
curl -X POST http://localhost:8000/notify
```

Data persistence
- The SQLite DB is stored in `./data/birthdays.db` on the host (via a Docker volume mapping). Keep backups as needed.

Next steps / improvements
- Add authentication for the API
- Support other notification channels (email, SMS)
- Add timezone-aware birthday checks or per-user preferences


Notes
- The scheduler runs once per day at 08:00 UTC by default. You can change schedule in `app/scheduler.py`.
