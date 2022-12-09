import os
from dotenv import load_dotenv

def get_webhook() -> str:
    load_dotenv()
    WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
    if not WEBHOOK_URL:
        return "DISCORD WEBHOOK NOT FOUND"
    else:
        return WEBHOOK_URL