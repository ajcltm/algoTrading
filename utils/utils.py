import uuid
from datetime import datetime

def create_id():
    time_id = datetime.now().strftime(format='%y%m%d-%H%M%S')
    raw_id = str(uuid.uuid1().int)
    return f'{time_id}-{raw_id[:4]}-{raw_id[4:8]}-{raw_id[8:12]}-{raw_id[12:16]}'

def create_datetime_periods(start_date, end_date): # date format -> "1923-08-29"
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    date_generated = [start_date + datetime.timedelta(days=x) for x in range(0, (end_date-start_date).days)+1]
    return date_generated
