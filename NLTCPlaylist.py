import requests
import csv
import os
import base64
import random 
from dotenv import load_dotenv # type: ignore

# Spotify API credentials
load_dotenv()  

# Access the environment variables as usual
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
PLAYLIST_ID = os.getenv("PLAYLIST_ID")
SPOTIFY_PLAYLIST_URL =  os.getenv("SPOTIFY_PLAYLIST_URL")
SPOTIFY_TOKEN_URL = os.getenv("SPOTIFY_TOKEN_URL")

print(CLIENT_ID)
print(CLIENT_SECRET)
print(REDIRECT_URI)
print(PLAYLIST_ID)
print(SPOTIFY_PLAYLIST_URL)



# File to save the playlist
PLAYLIST_FILE = "playlist.csv"

def get_spotify_access_token():
    """
    Fetches the Spotify access token using the Client ID and Client Secret.
    """
    auth_header = f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
    auth_header_base64 = base64.b64encode(auth_header).decode()
    headers = {"Authorization": f"Basic {auth_header_base64}"}
    data = {"grant_type": "client_credentials"}

    response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("Failed to fetch Spotify access token.")

def fetch_playlist_songs():
    """
    Fetches songs from the Spotify playlist.
    """
    access_token = get_spotify_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(SPOTIFY_PLAYLIST_URL, headers=headers)

    if response.status_code == 200:
        playlist_data = response.json()
        songs = [item["track"]["name"] for item in playlist_data["tracks"]["items"]]
        return songs
    else:
        raise Exception(f"Failed to fetch playlist: {response.status_code}, {response.text}")

def save_playlist_to_csv(songs):
    """
    Saves the playlist songs to a CSV file with unique random numbers from 1 to 75.
    """
    if len(songs) > 75:
        raise Exception("Playlist contains more than 75 songs. Please reduce the number of songs in the playlist.")

    random_numbers = random.sample(range(1, 76), len(songs))  # Generate unique random numbers from 1 to 75
    with open(PLAYLIST_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Song Name", "Song Number"])  # Write header
        for song, number in zip(songs, random_numbers):
            writer.writerow([song, number])  # Assign a unique random number to each song

def main():
    """
    Main function to fetch playlist and save to CSV.
    """
    try:
        print("Fetching playlist from Spotify...")
        songs = fetch_playlist_songs()
        print(f"Fetched {len(songs)} songs.")

        print(f"Saving playlist to {PLAYLIST_FILE}...")
        save_playlist_to_csv(songs)
        print(f"Playlist saved successfully to {PLAYLIST_FILE}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
