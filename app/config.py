import os


SECRET_KEY = os.getenv("APP_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Set APP_SECRET_KEY before using the application")
DEMO_USER_PASSWORD = os.getenv("DEMO_USER_PASSWORD")
TOKEN_TTL_SECONDS = 3600
