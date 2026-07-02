import os
import re

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

FRONTEND_URL = os.getenv("FRONTEND_URL")
if not FRONTEND_URL:
    raise RuntimeError("FRONTEND_URL is not set")

CORS_ORIGINS = [origin.strip() for origin in FRONTEND_URL.split(",")]

JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError("JWT_SECRET is not set")

JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60 * 24 * 7

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID") or None
if GOOGLE_CLIENT_ID and not re.fullmatch(r"\d+-[a-zA-Z0-9]+\.apps\.googleusercontent\.com", GOOGLE_CLIENT_ID):
    print(f"WARNING: GOOGLE_CLIENT_ID '{GOOGLE_CLIENT_ID}' doesn't look valid, disabling Google auth")
    GOOGLE_CLIENT_ID = None

# rate limits for "dangerous" endpoints
RATE_LIMIT_SENSITIVE = "3/second"
# rate limits for everything else
RATE_LIMIT_DEFAULT = "5/second"

class Errors:
    """error messages shown to the client"""

    TOO_MANY_REQUESTS = "too many requests, please slow down"
    INVALID_INPUT = "invalid input"
    EMAIL_ALREADY_REGISTERED = "email already registered"
    INVALID_CREDENTIALS = "invalid email or password"
    GOOGLE_NOT_CONFIGURED = "google auth is not configured"
    INVALID_GOOGLE_CREDENTIAL = "invalid Google credential"
    GOOGLE_EMAIL_NOT_VERIFIED = "google email is not verified"
    INVALID_TOKEN = "invalid or expired token"
    USER_NOT_FOUND = "user not found"
    INVALID_EMAIL = "please enter a valid email address"
    PASSWORD_TOO_SHORT = "password must be at least 8 characters"
