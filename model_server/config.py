import os
import logging

logging_level = logging.DEBUG

cfg = {
    "USE_OPENAI_ENDPOINT": os.getenv("USE_OPENAI_ENDPOINT", 1),
    "ENABLE_DEBUG_LOGGING": os.getenv("ENABLE_DEBUG_LOGGING", 1),
    "FIREWORKS_API_KEY": os.getenv("FIREWORKS_API_KEY"),
    "DB_URL": os.getenv("DB_URL"),
    "DEV": os.getenv("DEV", 0)
}

# , "sqlite:///./sql_app.db"
