import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")
    DEFAULT_CATEGORY_ID = 1
    DEFAULT_CATEGORY_NAME = "Uncategorized"
