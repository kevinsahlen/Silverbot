from datetime import datetime, timedelta
from re import match
from utils.db import getTimezone
import discord
import pytz

# returns a discord timestamp with the timezone adjusted to the user's timezone
def discordTimestamp(user: discord.User, input_HHMM: str,input_day: str, input_month: str,input_year: str) -> str:
    if input_day is None: input_day = datetime.now().day
    if input_month is None: input_month = datetime.now().month
    if input_year is None: input_year = datetime.now().year
    if input_HHMM is None: input_HHMM = datetime.now().strftime('%H:%M')
    if not validateTime(input_HHMM):
        raise ValueError('Invalid time format. Please use HH:MM')
    input_hour, input_minute, input_day, input_month, input_year = extractTime(input_HHMM, input_day, input_month, input_year)
    parsed_datetime = datetime.now().replace(hour=input_hour,minute=input_minute,day=input_day,month=input_month,year=input_year)
    cest_adjusted = adjustTimezone(parsed_datetime, user)
    return f'<t:{int(cest_adjusted.timestamp())}:R>'

# returns a discord timestamp with with a timedelta restriction and adjust past time, only for use in key command
def discordTimestampKey(user: discord.User, input_HHMM: str,input_day: str, input_month: str,input_year: str) -> str:
    if input_day is None: input_day = datetime.now().day
    if input_month is None: input_month = datetime.now().month
    if input_year is None: input_year = datetime.now().year
    if input_HHMM is None: input_HHMM = datetime.now().strftime('%H:%M')
    if not validateTime(input_HHMM):
        raise ValueError('Invalid time format. Please use HH:MM')
    input_hour, input_minute, input_day, input_month, input_year = extractTime(input_HHMM, input_day, input_month, input_year)
    parsed_dateTime = datetime.now().replace(hour=input_hour,minute=input_minute,day=input_day,month=input_month,year=input_year)
    cest_adjusted = adjustTimezone(parsed_dateTime, user)
    cest_adjusted = addDayIfPast(cest_adjusted)
    if abs(datetime.now(pytz.utc) - cest_adjusted) > timedelta(days=1):
        raise ValueError('set time cannot exceed 24 hours from now')
    return f'<t:{int(cest_adjusted.timestamp())}:R>'

# returns a datetime object with the timezone adjusted to the user's timezone
def adjustTimezone(input_time, user: discord.User) -> datetime:
    user_timezone = pytz.timezone(getTimezone(user))
    input_time_aware = user_timezone.localize(input_time)
    input_cest = input_time_aware.astimezone(pytz.timezone('Europe/Stockholm'))
    return input_cest

# returns a tuple with the values converted to integers for use in datetime objects
def extractTime(time: str, day: str, month: str, year: str) -> tuple:
    h = int(time.split(':')[0])
    m = int(time.split(':')[1])
    day = int(day)
    month = int(month)
    year = int(year)
    return h, m, day, month, year

# checks if time is in HH:MM format
def validateTime(time: str):
    regex = r'^\s*[0-2][0-9]:[0-5][0-9]\s*$'
    if not match(regex, time.strip()):
        print('regex failed')
        return False
    return True

# If the time is in the past, add a day
def addDayIfPast(time: datetime):
    if time < datetime.now(pytz.utc) and time - datetime.now(pytz.utc) < timedelta(minutes=1):
        time = time + timedelta(days=1)
    return time