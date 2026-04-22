import time

users = {}
login_attempts = {}
lock_until = {}
otp_store = {}
sessions = {}
user_history = {}

ATTEMPT_LIMIT = 3
LOCK_DURATION = 120


def get_user(username):
    return users.get(username)


def save_user(username, data):
    users[username] = data


def record_history(username, event):
    user_history.setdefault(username, []).append({
        "event": event,
        "time": time.time()
    })


def get_history(username):
    return user_history.get(username, [])


def get_attempts(username):
    return login_attempts.get(username, 0)


def increment_attempts(username):
    login_attempts[username] = get_attempts(username) + 1
    return login_attempts[username]


def reset_attempts(username):
    login_attempts[username] = 0


def lock_account(username):
    lock_until[username] = time.time() + LOCK_DURATION


def is_locked(username):
    unlock_time = lock_until.get(username)
    if unlock_time and time.time() < unlock_time:
        return True
    if unlock_time and time.time() >= unlock_time:
        lock_until.pop(username, None)
        login_attempts[username] = 0
        return False
    return False


def set_otp(username, otp_code, expires_in=45):
    otp_store[username] = {
        "otp": otp_code,
        "expires_at": time.time() + expires_in,
        "sent_at": time.time()
    }


def get_otp(username):
    return otp_store.get(username)


def clear_otp(username):
    otp_store.pop(username, None)


def create_session(username, token):
    sessions[username] = {
        "token": token,
        "created_at": time.time(),
        "status": "authenticated"
    }


def get_session(username):
    return sessions.get(username)


def unlock_account(username):
    """Unlock account and reset login attempts"""
    lock_until.pop(username, None)
    login_attempts[username] = 0
