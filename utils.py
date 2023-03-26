import uuid
from datetime import datetime

def create_id():
    time_id = datetime.now().strftime(format='%y%m%d-%H%M%S')
    raw_id = str(uuid.uuid1().int)
    return f'{time_id}-{raw_id[:4]}-{raw_id[4:8]}-{raw_id[8:12]}-{raw_id[12:16]}'