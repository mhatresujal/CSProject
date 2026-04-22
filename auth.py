from database import get_user, save_user, record_history, get_attempts, increment_attempts, reset_attempts, lock_account, is_locked
from security import generate_salt, hash_password, verify_password
import re


def check_password_strength(password):
    """Check if password meets requirements: alphanumeric + special char + number"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    if not re.search(r'[^A-Za-z0-9]', password):
        return False, "Password must contain at least one special character"
    return True, "Strong password"


def register_user(username, password):
    if get_user(username):
        return False, "Username already exists"
    
    # Check password strength during registration
    is_strong, strength_msg = check_password_strength(password)
    if not is_strong:
        return False, f"Registration failed: {strength_msg}"

    salt = generate_salt()
    hashed = hash_password(password, salt)
    save_user(username, {
        "salt": salt,
        "password": hashed,
        "totp_secret": None,
        "status": "normal"
    })
    # Record registration event
    record_history(username, "registered")
    return True, {
        "salt": salt,
        "hash": hashed
    }


def verify_login(username, password):
    user = get_user(username)
    if not user:
        return False, "User not found", 0
    if is_locked(username):
        return False, "Account locked", 0

    if verify_password(password, user["salt"], user["password"]):
        reset_attempts(username)
        record_history(username, "login_success")
        return True, "Login verified", 0

    attempts = increment_attempts(username)
    record_history(username, f"login_failed_{attempts}")
    if attempts >= 3:
        lock_account(username)
        record_history(username, "account_locked")
        return False, "Account locked after 3 failed attempts", 0

    delay = 2 ** (attempts - 1)
    return False, f"Incorrect password (Attempt {attempts}/3)", delay


def reset_password(username, new_password):
    """Reset the password for a locked account"""
    user = get_user(username)
    if not user:
        return False, "User not found"
    
    # Check password strength
    is_strong, strength_msg = check_password_strength(new_password)
    if not is_strong:
        return False, f"Reset failed: {strength_msg}"
    
    # Update password with new salt
    salt = generate_salt()
    hashed = hash_password(new_password, salt)
    user["salt"] = salt
    user["password"] = hashed
    save_user(username, user)
    record_history(username, "password_reset")
    
    return True, "Password reset successfully"


def account_status(username):
    if is_locked(username):
        return "Locked"
    return "Normal"


def get_attempt_info(username):
    attempts = get_attempts(username)
    return attempts, max(0, 3 - attempts)
