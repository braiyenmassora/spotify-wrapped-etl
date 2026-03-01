import os
from dotenv import load_dotenv

load_dotenv()

# config to load variable


class Config:
    # spotify
    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
    TIME_RANGE = os.getenv("TIME_RANGE", "medium_term")
    LIMIT = int(os.getenv("LIMIT", 50))
    DATA_FORMAT = os.getenv("DATA_FORMAT", "parquet")
    SCOPE = "user-top-read"

    # data
    RAW_DATA_PATH = os.getenv("RAW_DATA_PATH", "data/raw")
    PROCESSED_DATA_PATH = os.getenv("PROCESSED_DATA_PATH", "data/processed")
