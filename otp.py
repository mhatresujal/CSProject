import base64
import os
import random
import time
from security import generate_totp


def generate_otp():
    return ''.join(str(random.randint(0, 9)) for _ in range(6))


def generate_totp_secret():
    return base64.b32encode(os.urandom(10)).decode('utf-8')


def verify_otp(otp_entry, code):
    if not otp_entry:
        return False
    if time.time() > otp_entry.get("expires_at", 0):
        return False
    return otp_entry.get("otp") == code
