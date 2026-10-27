import os

from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "JARVIS")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")