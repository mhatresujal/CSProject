from flask import Flask, render_template, request, redirect, url_for, session
import time

from auth import register_user, verify_login, account_status, get_attempt_info, reset_password
from database import get_user, save_user, set_otp, get_otp, clear_otp, create_session, get_session, get_history, unlock_account, record_history
from otp import generate_otp, generate_totp_secret, verify_otp
from security import hash_md5, hash_sha256, hash_bcrypt, generate_totp
from utils import generate_session_token

app = Flask(__name__)
app.secret_key = "your-secret-key-change-in-production"

@app.template_filter('datetimeformat')
def datetimeformat(value):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(value))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    message = None
    result = None

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        success, payload = register_user(username, password)

        if success:
            message = "Registration successful ? Redirecting to login..."
            result = payload
        else:
            message = payload

    return render_template("register.html", message=message, result=result)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = None
    delay = 0
    attempts = 0
    remaining = 3

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        success, message, delay = verify_login(username, password)

        attempts, remaining = get_attempt_info(username)

        if success:
            session["username"] = username
            session["authenticated"] = False
            return redirect(url_for("otp"))

    return render_template("login.html", message=message, delay=delay, attempts=attempts, remaining=remaining, is_locked=False)

@app.route("/otp", methods=["GET", "POST"])
def otp():
    username = session.get("username")
    if not username:
        return redirect(url_for("home"))

    user = get_user(username)
    if not user:
        return redirect(url_for("home"))

    if not user.get("totp_secret"):
        user["totp_secret"] = generate_totp_secret()
        save_user(username, user)

    otp_code = None
    message = None
    otp_ttl = 0

    if request.method == "POST":
        action = request.form.get("action")
        if action == "send":
            otp_code = generate_otp()
            set_otp(username, otp_code)
            message = "OTP generated and displayed for demo purposes."
            otp_ttl = 45
        elif action == "verify":
            code = request.form.get("otp_code", "").strip()
            otp_entry = get_otp(username)
            if verify_otp(otp_entry, code):
                token = generate_session_token()
                create_session(username, token)
                session["authenticated"] = True
                session["session_token"] = token
                clear_otp(username)
                return redirect(url_for("dashboard"))
            message = "Invalid or expired OTP. Please try again."

    live_totp = generate_totp(user["totp_secret"])
    return render_template(
        "otp.html",
        username=username,
        account_status=account_status(username),
        totp_secret=user["totp_secret"],
        otp_code=otp_code,
        otp_ttl=otp_ttl,
        live_totp=live_totp,
        message=message
    )

@app.route("/dashboard")
def dashboard():
    username = session.get("username")
    authenticated = session.get("authenticated", False)
    if not username or not authenticated:
        return redirect(url_for("login"))

    user = get_user(username)
    if not user:
        return redirect(url_for("home"))

    session_info = get_session(username) or {}
    status_text = account_status(username)
    attempts, remaining = get_attempt_info(username)

    # Find last login time
    history = get_history(username)
    last_login = None
    for event in reversed(history):
        if event["event"] == "login_success":
            last_login = event["time"]
            break

    return render_template(
        "dashboard.html",
        username=username,
        message="Login successful. Welcome to the security dashboard.",
        account_status=status_text,
        attempts=attempts,
        remaining_attempts=remaining,
        history=history,
        last_login=last_login,
        session_status="Normal" if status_text == "Normal" else "Locked",
        session_token=session_info.get("token", "N/A")
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password_route():
    message = None
    username = None
    
    if request.method == "POST":
        username = request.form["username"].strip()
        new_password = request.form["new_password"].strip()
        confirm_password = request.form["confirm_password"].strip()
        
        # Check if passwords match
        if new_password != confirm_password:
            message = "Passwords do not match"
        else:
            # Reset the password
            success, msg = reset_password(username, new_password)
            if success:
                # Unlock the account
                unlock_account(username)
                message = "Password reset successful! You can now login with your new password."
                username = None  # Clear username to show success message
            else:
                message = msg
    
    return render_template("reset_password.html", message=message, username=username)

if __name__ == "__main__":
    app.run(debug=True)
