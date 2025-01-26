from config_loader import load_env_from_file
import os

# Load environment variables from the file
load_env_from_file("env_vars.txt")

# Spotify API credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# Flask configuration
SECRET_KEY = os.getenv("APP_SECRET_KEY")

# File paths
SONGS_FILE = os.getenv("SONGS_FILE")
CARDS_FILE = os.getenv("CARDS_FILE")

# Spotify API URLs
REDIRECT_URI = os.getenv("REDIRECT_URI")
SPOTIFY_TOKEN_URL = os.getenv("SPOTIFY_TOKEN_URL")
SPOTIFY_CURRENT_TRACK_URL = os.getenv("SPOTIFY_CURRENT_TRACK_URL")

