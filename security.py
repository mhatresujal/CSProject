import hashlib
import hmac
import os
import base64
import time

try:
    import bcrypt
    _has_bcrypt = True
except ImportError:
    _has_bcrypt = False



def generate_salt():
    return os.urandom(16).hex()


def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()


def verify_password(password, salt, stored_hash):
    return hash_password(password, salt) == stored_hash


def password_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()-_+=[]{}|;:'\",.<>/?`~" for c in password):
        score += 1

    if score <= 2:
        return "Weak", "#f87171"
    if score == 3:
        return "Medium", "#fbbf24"
    return "Strong", "#4ade80"


def hash_md5(text):
    return hashlib.md5(text.encode()).hexdigest()


def hash_sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()


def hash_bcrypt(text):
    if _has_bcrypt:
        return bcrypt.hashpw(text.encode(), bcrypt.gensalt()).decode()
    raw = hashlib.pbkdf2_hmac("sha256", text.encode(), b"bcrypt_demo_salt", 100000)
    return "bcrypt_demo$" + base64.b64encode(raw).decode()


def verify_bcrypt(text, hashed):
    if _has_bcrypt and hashed.startswith("$2b$"):
        return bcrypt.checkpw(text.encode(), hashed.encode())
    return hash_bcrypt(text) == hashed


def generate_totp(secret, interval=30):
    counter = int(time.time() // interval)
    key = base64.b32decode(secret, True)
    msg = counter.to_bytes(8, "big")
    hmac_hash = hmac.new(key, msg, hashlib.sha1).digest()
    offset = hmac_hash[-1] & 0x0F
    code = (int.from_bytes(hmac_hash[offset:offset + 4], "big") & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"
