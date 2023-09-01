from dotenv import load_dotenv
from datetime import datetime, timedelta

def getSnapshotTime():
    now = datetime.now()
    year = str(now.year)
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)
    hour = str(now.hour).zfill(2)
    minute = str(now.minute).zfill(2)
    second = str(now.second).zfill(2)

    return '{}_{}_{}_{}_{}_{}'.format(year, month, day, hour, minute, second)