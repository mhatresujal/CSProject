from flask import Flask, render_template, request
import hashlib
import os

app = Flask(__name__)

# In-memory storage
users = {}
attempts = {}
locked_accounts = {}
lock_until = {}

# -------- FUNCTIONS --------
def generate_salt():
    return os.urandom(16).hex()

def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()

# -------- ROUTES --------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    message = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            message = "Username already exists ❌"

        else:
            salt = generate_salt()
            hashed = hash_password(password, salt)

            users[username] = {
                "salt": salt,
                "password": hashed
            }

            message = f"Registered successfully ✅ | Salt: {salt[:8]}... | Hash: {hashed[:10]}..."

    return render_template("register.html", message=message)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = None
    delay = 0

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username not in users:
            message = "User not found ❌"

        elif username in locked_accounts:
            message = "Account locked 🔒"

        else:
            if username not in attempts:
                attempts[username] = 0

            salt = users[username]["salt"]
            stored_hash = users[username]["password"]

            entered_hash = hash_password(password, salt)

            if entered_hash == stored_hash:
                attempts[username] = 0
                message = "Login successful ✅"

            else:
                attempts[username] += 1

                if attempts[username] >= 3:
                    locked_accounts[username] = True
                    message = "Account locked 🔒"
                else:
                    delay = 2 ** (attempts[username] - 1)
                    message = f"Incorrect password ❌ (Attempt {attempts[username]}/3)"

    return render_template("login.html", message=message, delay=delay)

if __name__ == "__main__":
    app.run(debug=True)