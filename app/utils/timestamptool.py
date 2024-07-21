from datetime import datetime, timedelta
import re
import discord
import pytz
from utils.db import getTimezone


def discordTimestamp(user: discord.Interaction.user, time: str,day: str, month: str,year: str) -> str:
    
    if day is None: day = datetime.now().day
    if month is None: month = datetime.now().month
    if year is None: year = datetime.now().year
    if time is None:
        time = datetime.now().strftime('%H:%M')
    if not validateTime(time):
        raise ValueError('Invalid time format. Please use HH:MM')
    h, m, day, month, year = extractTime(time, day, month, year)
    input_time = datetime.now().replace(hour=h,minute=m,day=day,month=month,year=year)
    input_cest = adjustTimezone(input_time, user)
    return f'<t:{int(input_cest.timestamp())}:R>'

def discordTimestampKey(user: discord.Interaction.user, time: str,day: str, month: str,year: str) -> str:
    
    if day is None: day = datetime.now().day
    if month is None: month = datetime.now().month
    if year is None: year = datetime.now().year
    if time is None:
        time = datetime.now().strftime('%H:%M')
    if not validateTime(time):
        raise ValueError('Invalid time format. Please use HH:MM')
    h, m, day, month, year = extractTime(time, day, month, year)
    input_time = datetime.now().replace(hour=h,minute=m,day=day,month=month,year=year)
    input_cest = adjustTimezone(input_time, user)
    input_cest = addDayIfPast(input_cest)
    if abs(datetime.now(pytz.utc) - input_cest) > timedelta(days=1):
        raise ValueError('set time cannot exceed 24 hours from now')
    
    return f'<t:{int(input_cest.timestamp())}:R>'

def adjustTimezone(input_time, user: discord.User) -> datetime:
    user_timezone = pytz.timezone(getTimezone(user))
    input_time_aware = user_timezone.localize(input_time)
    input_cest = input_time_aware.astimezone(pytz.timezone('Europe/Stockholm'))
    return input_cest

def extractTime(time: str, day: str, month: str, year: str) -> tuple:
    h = int(time.split(':')[0])
    m = int(time.split(':')[1])
    day = int(day)
    month = int(month)
    year = int(year)
    return h, m, day, month, year

def validateTime(time: str):
    regex = r'^\s*[0-2][0-9]:[0-5][0-9]\s*$'
    if not re.match(regex, time.strip()):
        print('regex failed')
        return False
    return True

def addDayIfPast(time: datetime):
    if time < datetime.now(pytz.utc) and time - datetime.now(pytz.utc) < timedelta(minutes=1):
        time = time + timedelta(days=1)
    return time