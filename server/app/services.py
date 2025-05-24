from datetime import datetime, timedelta


def get_current_week(date: datetime) -> dict:
    # Round down to the nearest Monday
    days_to_subtract = date.weekday()
    if days_to_subtract != 0:  # If it's not already Monday
        date -= timedelta(days=days_to_subtract)
 
    # Build the dictionary
    days_of_week = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    week_current = {}
    for i, day in enumerate(days_of_week):
        week_current[day] = date + timedelta(days=i)

    return week_current

