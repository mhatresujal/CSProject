import random
import string
import time


def generate_session_token(length=12):
    charset = string.ascii_uppercase + string.digits
    return ''.join(random.choice(charset) for _ in range(length))


def format_duration(seconds):
    return f"{int(seconds)}s"


def safe_timestamp(ts):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(ts))
