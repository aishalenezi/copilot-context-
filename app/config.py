import os


SECRET_KEY = os.getenv("APP_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Set APP_SECRET_KEY before using the application")
TOKEN_TTL_SECONDS = 3600
