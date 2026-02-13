# daylight_hours.py

from datetime import date
import calendar
from astral import LocationInfo
from astral.sun import sun
import pytz

def get_average_daylight_hours(city: str, country: str, timezone: str, month: int, year: int = 2025) -> float:
    """Calculate the average daylight hours for a given city, timezone, and month."""

    # Setup location
    loc = LocationInfo(city, country, timezone)

    # Get total days in month
    days_in_month = calendar.monthrange(year, month)[1]

    daylight_hours = []

    for day in range(1, days_in_month + 1):
        current_date = date(year, month, day)
        s = sun(loc.observer, date=current_date, tzinfo=pytz.timezone(timezone))

        sunrise = s["sunrise"]
        sunset = s["sunset"]
        duration = sunset - sunrise
        daylight_hours.append(duration.total_seconds() / 3600)  # convert to hours

    # Return average daylight hours
    return sum(daylight_hours) / len(daylight_hours)


if __name__ == "__main__":
    city = input("Enter your city: ").strip()
    country = input("Enter your country: ").strip()
    timezone = input("Enter timezone (e.g., Asia/Kolkata, Europe/London): ").strip()

    month_input = input("Enter month (1-12): ").strip()
    month = int(month_input)

    avg_hours = get_average_daylight_hours(city, country, timezone, month)
    print(f"\n🌞 Average daylight hours in {city}, {country} for month {calendar.month_name[month]}: {avg_hours:.2f} hrs")
