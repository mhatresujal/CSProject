# Secure Authentication System

## Overview

A Flask-based authentication system with support for multi-factor authentication, password hashing, and security analytics. This application provides a complete authentication flow with built-in protection mechanisms including rate limiting, account lockout, and cryptographic password hashing.

## Features

- User registration with password strength validation
- Secure login with attempt tracking and account lockout
- Two-factor authentication (OTP and TOTP support)
- Password hashing with salting using SHA-256
- Hash algorithm comparison (MD5, SHA-256, bcrypt)
- Session token generation
- Activity logging
- Rate limiting with exponential backoff
- Responsive light-themed user interface

## Technology Stack

- **Backend:** Flask 2.0+
- **Frontend:** HTML5, CSS3
- **Cryptography:** hashlib, bcrypt
- **Database:** In-memory storage (for demo purposes)
- **Python Version:** 3.8+

## Project Structure

```
project/
├── app.py              # Main Flask application and routing
├── auth.py             # Authentication logic (registration, login verification)
├── database.py         # In-memory data storage and management
├── otp.py              # OTP and TOTP generation
├── security.py         # Cryptographic functions and hashing algorithms
├── utils.py            # Utility functions
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── home.html
│   ├── register.html
│   ├── login.html
│   ├── otp.html
│   └── dashboard.html
└── static/
    └── style.css       # Stylesheet
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Open a terminal and navigate to the project directory:
```bash
cd D:\Users\Desktop\CS_Project\CSProject
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the Flask server:
```bash
python app.py
```

The application will be accessible at:
```
http://127.0.0.1:5000/
```

## User Flow

### 1. Home Page
Entry point with navigation options to register or login.

### 2. Registration
- Create a new account with username and password
- Real-time password strength indicator
- Displays generated salt and hash values
- Auto-redirects to login upon success

### 3. Login
- Enter credentials
- Attempt counter tracks failed attempts
- Rate limiting: 3 failed attempts lock the account for 120 seconds
- Exponential backoff delays between attempts (1s, 2s, 4s)

### 4. Two-Factor Authentication
- OTP verification screen
- Request a one-time password
- Live TOTP code display (updates every 30 seconds)
- OTP expiration: 45 seconds

### 5. Dashboard
- Account verification confirmation
- Session token display
- Three tabs:
  - **Overview:** Account status and activity log
  - **Benchmark:** Hash algorithm performance comparison
  - **Salt Demo:** Demonstrates salt impact on hashing

## Security Features

### Password Hashing
- Algorithm: SHA-256 with random salt
- Salt length: 16 bytes (hexadecimal encoded)
- Each password is hashed uniquely due to random salt generation

### Rate Limiting
- Failed login attempts tracked per user
- Exponential backoff: delay = 2^(attempts-1) seconds
- Account lockout after 3 failed attempts
- Lockout duration: 120 seconds

### OTP/TOTP Implementation
- **OTP:** Random 6-character alphanumeric codes
- **TOTP:** Time-based One-Time Password using HMAC-SHA1
- Time interval: 30 seconds
- Expiration: 45 seconds for demo OTP

### Session Management
- Random alphanumeric session tokens (12 characters)
- Session tokens generated after successful OTP verification
- In-memory session storage

## Algorithm Details

### Hashing Algorithms

#### MD5
- Speed: Very fast
- Security: Weak (vulnerable to collisions)
- Not recommended for new applications

#### SHA-256
- Speed: Fast
- Security: Strong
- Widely used standard
- Used as primary hashing algorithm in this application

#### bcrypt
- Speed: Slow (intentional)
- Security: Very strong
- Resistant to brute-force attacks
- Includes built-in salting

### TOTP (Time-Based One-Time Password)
- Based on RFC 6238 standard
- Algorithm: HMAC-SHA1
- Time step: 30 seconds
- Code length: 6 digits
- Derived from base32-encoded secret

## API Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page |
| `/register` | GET, POST | Registration page and handler |
| `/login` | GET, POST | Login page and handler |
| `/otp` | GET, POST | Two-factor authentication |
| `/dashboard` | GET | Authenticated dashboard |
| `/logout` | GET | Clear session and logout |

## Configuration

### Secret Key
Change the Flask secret key in `app.py` for production:
```python
app.secret_key = "your-strong-secret-key-here"
```

### Account Lockout
Edit these constants in `database.py`:
- `ATTEMPT_LIMIT = 3` - Number of failed attempts before lockout
- `LOCK_DURATION = 120` - Lockout duration in seconds

## Important Notes

- **Data Storage:** All user data is stored in memory and will be lost on server restart
- **Production Use:** For production deployment, integrate with a persistent database
- **HTTPS:** Always use HTTPS in production
- **OTP Delivery:** Currently displays OTP on-screen for demo purposes; integrate email/SMS service for production

## Security Recommendations for Production

1. Use a persistent database (PostgreSQL, MongoDB, etc.)
2. Implement HTTPS/SSL encryption
3. Add rate limiting at network level
4. Use stronger session token generation
5. Implement account recovery mechanisms
6. Add email verification for registration
7. Store audit logs securely
8. Implement CSRF protection
9. Add input validation and sanitization
10. Regular security audits and penetration testing

## Troubleshooting

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, port=5001)
```

### Module Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### CSS Not Loading
Clear browser cache or use Ctrl+Shift+R to force refresh

## License

This project is provided as-is for educational and demonstration purposes.

## Support

For issues or questions, please refer to the inline code documentation or review the Flask documentation at https://flask.palletsprojects.com/
