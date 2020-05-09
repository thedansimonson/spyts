from datetime import datetime, timedelta

def wait(until):
    """
    Waits for the specified duration.
    Arg: until = a datetime object specifying the time to quit waiting.
    """
    while datetime.now() < until:
        "do nothing"

def one_hour():
    return datetime.now() + timedelta(1.0/24,0,0)

def one_minute():
    "For test purposes"
    return datetime.now() + timedelta(1.0/24/60,0,0)
	
def in_minutes(length):
    "For test purposes"
    return datetime.now() + timedelta(float(length)/24/60,0,0)
