from datetime import datetime
import pytz
#print(pytz.all_timezones)
from timezonefinder import TimezoneFinder
from geopy.geocoders import Nominatim

# Predefined cities with respective timezones
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
    "Dubai": "Asia/Dubai"
}

def get_timezone_from_city(city_name):
    geolocator = Nominatim(user_agent="timezone_finder")
    location = geolocator.geocode(city_name)
    if location:
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        return timezone_str
    else:
        return None

def print_times(user_city):
    user_timezone_str = get_timezone_from_city(user_city)
    if user_timezone_str is None:
        print(f"Could not find timezone for city: {user_city}")
        return

    now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    user_timezone = pytz.timezone(user_timezone_str)
    print(f"\nTime in your city ({user_city}): {now_utc.astimezone(user_timezone).strftime('%Y-%m-%d %H:%M:%S')}")

    for city, tz in city_timezones.items():
        try:
            tz_clean = tz.strip()
            local_time = now_utc.astimezone(pytz.timezone(tz_clean))
            print(f"Time in {city}: {local_time.strftime('%Y-%m-%d %H:%M:%S')}")
        except pytz.UnknownTimeZoneError:
            print(f"Invalid timezone for {city}: {tz}")

if __name__ == "__main__":
    user_input = input("Enter your city: ")
    print_times(user_input.strip())
