import datetime

def nano_to_s(t):
    # convert to second.us
    return int(t)/1e9

def now_readable():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")