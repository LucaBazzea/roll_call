import secrets
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from django.conf import settings

from mailersend import MailerSendClient, EmailBuilder




def get_week(date: date) -> dict:
    # Round down to the nearest Monday
    days_to_subtract = date.weekday()
    if days_to_subtract != 0:  # If it's not already Monday
        date -= timedelta(days=days_to_subtract)

    # Build the dictionary
    days_of_week = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")
    week_current = {}
    for item, day in enumerate(days_of_week):
        week_current[day] = date + timedelta(days=item)

    return week_current

def get_next_7_days(timezone: str) -> dict: # e.g. "Africa/Windhoek"
    tz = ZoneInfo(timezone)
    now_local = datetime.now(tz)

    days = {}
    for item in range(7):
        day = now_local + timedelta(days=item)

        day_name = day.strftime("%A")[:3].lower()
        date = day.date()

        days[day_name] = date

    return days

def generate_pin():
    return secrets.randbelow(900000) + 100000

def send_otp_email(email, pin):
    ms = MailerSendClient()

    email = (
        EmailBuilder()
            .from_email("no-reply@rollcall.cc", "RollCall Team")
            .to_many([{"email": "recipient@domain.com", "name": "Recipient"}])
            .template("o65qngkm50jlwr12")
            .personalize_many([{
                "email": "recipient@domain.com",
                "data": {},
                "otp": pin
            }])
            .build()
    )

    response = ms.emails.send(email)
