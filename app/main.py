from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim

# ANSI escape codes for colors
COLORS = {
    "Morning": "\033[92m",   # Green
    "Noon": "\033[93m",      # Yellow
    "Evening": "\033[94m",   #Light Blue
    "Night": "\033[34m",     # Blue 
    "HeaderNA": "\033[96m",  # Cyan for North America
    "HeaderEU": "\033[94m",  # Blue for Europe
    "HeaderAS": "\033[91m",  # Red for Asia/Oceania
    "Reset": "\033[0m"
}

city_timezones = {
    "New York": "America/New_York",
    "California": "America/Los_Angeles",
    "Chicago": "America/Chicago",
    "India": "Asia/Kolkata",
    "London": "Europe/London",
    "Sydney": "Australia/Sydney",
    "Melbourne": "Australia/Melbourne",
    "Victoria": "Australia/Victoria",
    "Dublin": "Europe/Dublin",
    "Dubai": "Asia/Dubai",
    "Tokyo": "Asia/Tokyo",
    "Paris": "Europe/Paris",
    "Berlin": "Europe/Berlin",
    "Rome": "Europe/Rome",
    "Cape Town": "Africa/Johannesburg",
    "Toronto": "America/Toronto",
    "Vancouver": "America/Vancouver",
    "Seoul": "Asia/Seoul",
    "Bangkok": "Asia/Bangkok",
    "Moscow": "Europe/Moscow"
}

def get_timezone_from_city(city_name):
    geolocator = Nominatim(user_agent="timezone_finder")
    location = geolocator.geocode(city_name)
    if location:
        tf = TimezoneFinder()
        return tf.timezone_at(lng=location.longitude, lat=location.latitude)
    return None

def get_time_of_day(time_obj):
    hour = time_obj.hour
    if 5 <= hour < 12:
        return "Morning", "🌅"
    elif 12 <= hour < 17:
        return "Noon", "☀️"
    elif 17 <= hour < 21:
        return "Evening", "🌇"
    else:
        return "Night", "🌙"

def print_colored(city, time_str, tod_label, emoji):
    color = COLORS.get(tod_label, "")
    reset = COLORS["Reset"]
    print(f"{color} 📌 {city}: {time_str} ➠ { tod_label} {emoji}{reset}")

def print_times(user_city):
    user_timezone_str = get_timezone_from_city(user_city)
    if user_timezone_str is None:
        print(f"Could not find timezone for city: {user_city}")
        return

    now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    user_timezone = pytz.timezone(user_timezone_str)
    user_time_obj = now_utc.astimezone(user_timezone)
    user_time_str = user_time_obj.strftime('%Y-%m-%d %H:%M:%S')
    tod_label, emoji = get_time_of_day(user_time_obj)

    print(f"\n\033[1mYour City: {user_city}\033[0m")
    print_colored(user_city, user_time_str, tod_label, emoji)

    print(f"\n{COLORS['HeaderNA']}\033[1mNorth America:\033[0m{COLORS['Reset']}")
    for city in ["New York", "California", "Chicago"]:
        tz = city_timezones[city]
        time_obj = now_utc.astimezone(pytz.timezone(tz))
        tod_label, emoji = get_time_of_day(time_obj)
        time_str = time_obj.strftime('%Y-%m-%d %H:%M:%S')
        print_colored(city, time_str, tod_label, emoji)

    print(f"\n{COLORS['HeaderEU']}\033[1mEurope:\033[0m{COLORS['Reset']}")
    for city in ["London", "Dublin"]:
        tz = city_timezones[city]
        time_obj = now_utc.astimezone(pytz.timezone(tz))
        tod_label, emoji = get_time_of_day(time_obj)
        time_str = time_obj.strftime('%Y-%m-%d %H:%M:%S')
        print_colored(city, time_str, tod_label, emoji)

    print(f"\n{COLORS['HeaderAS']}\033[1mAsia & Oceania:\033[0m{COLORS['Reset']}")
    for city in ["India", "Sydney", "Melbourne", "Victoria", "Dubai"]:
        tz = city_timezones[city]
        time_obj = now_utc.astimezone(pytz.timezone(tz))
        tod_label, emoji = get_time_of_day(time_obj)
        time_str = time_obj.strftime('%Y-%m-%d %H:%M:%S')
        print_colored(city, time_str, tod_label, emoji)

if __name__ == "__main__":
    user_input = input("Enter your city: ")
    print_times(user_input.strip())
