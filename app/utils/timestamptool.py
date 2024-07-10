from datetime import datetime, timedelta
import re

class TimestampTool:
    @staticmethod
    def discordTimestamp(time: str) -> str:
        regex = r'^\d{1,2}:\d{1,2}$'
        if not re.match(regex, time.strip()):
            raise ValueError('Invalid time format. Please use HH:MM')
        
        h = int(time.split(':')[0])
        m = int(time.split(':')[1])

        if h > 23 or m > 59:
            raise ValueError('time value out of range. HH:MM cant exceed 23:59')
        
        if abs(datetime.now() - datetime.now().replace(hour=h, minute=m)) > timedelta(days=1):
            raise ValueError('set time cannot exceed 24 hours from now')
        
        future_time:datetime = datetime.now().replace(hour=h,minute=m)

        if future_time < datetime.now():
            future_time = future_time + timedelta(days=1)

        return f'<t:{int(future_time.timestamp())}:R>'