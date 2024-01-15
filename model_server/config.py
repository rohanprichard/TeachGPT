import os
from dotenv import load_dotenv

load_dotenv(".env")

cfg = {
    "USE_OPENAI_ENDPOINT": os.getenv("USE_OPENAI_ENDPOINT", 1),
    "ENABLE_DEBUG_LOGGING": os.getenv("ENABLE_DEBUG_LOGGING", 1),
    "FIREWORKS_API_KEY": os.getenv("FIREWORKS_API_KEY"),
}

print(cfg)
