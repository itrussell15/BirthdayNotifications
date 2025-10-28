import os
import datetime
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from . import crud, notifier

SCHED_HOUR = int(os.getenv("SCHEDULER_HOUR", "8"))
SCHED_MINUTE = int(os.getenv("SCHEDULER_MINUTE", "0"))
TIMEZONE = os.getenv("TIMEZONE", "UTC")

try:
    tz = pytz.timezone(TIMEZONE)
except pytz.exceptions.UnknownTimeZoneError:
    print(f"Warning: Unknown timezone {TIMEZONE}, falling back to UTC")
    tz = pytz.UTC


def check_upcoming_birthday(birthday_date: datetime.date, today: datetime.date) -> tuple[bool, int]:
    """Check if a birthday is coming up and return (is_upcoming, days_until)."""
    # Get this year's birthday
    this_year_birthday = datetime.date(today.year, birthday_date.month, birthday_date.day)
    
    # If the birthday has passed this year, look at next year's date
    if this_year_birthday < today:
        this_year_birthday = datetime.date(today.year + 1, birthday_date.month, birthday_date.day)
    
    days_until = (this_year_birthday - today).days
    return days_until in (7, 30), days_until

def check_and_notify(for_date: datetime.date | None = None) -> bool:
    """Check for birthdays using the configured timezone."""
    if for_date is None:
        # Get current time in configured timezone
        now = datetime.datetime.now(tz)
        today = now.date()
    else:
        today = for_date
    
    print(f"Checking birthdays for date: {today} ({TIMEZONE})")
    
    birthdays = crud.get_birthdays()
    today_matches = []
    upcoming_7_days = []
    upcoming_30_days = []
    
    for b in birthdays:
        print(f"Checking birthday: {b.name} on {b.date} (type: {type(b.date)})")
        if isinstance(b.date, str):
            # Parse string date if needed
            b_date = datetime.datetime.strptime(b.date, "%Y-%m-%d").date()
        else:
            b_date = b.date
        
        if b_date.month == today.month and b_date.day == today.day:
            today_matches.append(b)
            print(f"Match found today: {b.name}")
            continue
            
        is_upcoming, days_until = check_upcoming_birthday(b_date, today)
        if is_upcoming:
            if days_until == 7 and b.notify_7_days:
                upcoming_7_days.append(b)
                print(f"Match found 7 days ahead: {b.name}")
            elif days_until == 30 and b.notify_30_days:
                upcoming_30_days.append(b)
                print(f"Match found 30 days ahead: {b.name}")
    
    success = True
    
    # Send notifications for today's birthdays
    if today_matches:
        ok = notifier.notify_birthdays(today_matches, "today")
        print(f"Today's notifications sent: {ok} -> [" + ", ".join(b.name for b in today_matches) + "]")
        success = success and ok
        
    # Send notifications for upcoming birthdays
    for days, matches in [(7, upcoming_7_days), (30, upcoming_30_days)]:
        if matches:
            print(vars(matches[0]))
            ok = notifier.notify_birthdays(matches, f"in {days} days")
            success = success and ok
            
    if not (today_matches or upcoming_7_days or upcoming_30_days):
        print(f"No birthdays today or upcoming (checked {len(birthdays)} entries)")
        
    return success


def start():
    scheduler = BackgroundScheduler(timezone=tz)
    # run once daily at configured hour/minute in local timezone
    scheduler.add_job(check_and_notify, 'cron', hour=SCHED_HOUR, minute=SCHED_MINUTE)
    scheduler.start()
    print(f"Scheduler started ({TIMEZONE}) at {SCHED_HOUR:02d}:{SCHED_MINUTE:02d}")
