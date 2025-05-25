from datetime import date, timedelta


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

