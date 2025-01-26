from flask import Flask, render_template, request, session, redirect, jsonify
import requests
import base64
import csv
import os
import pandas as pd
from dotenv import load_dotenv # type: ignore


# You don't have to create songs.csv, when you run the code for first time songs.csv is automatically created.
# when the program is executed, a songs.csv file is created automatically.

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a strong secret key

# Spotify API credentials
load_dotenv()  

# Access the environment variables as usual
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
PLAYLIST_ID = os.getenv("PLAYLIST_ID")
SPOTIFY_TOKEN_URL = os.getenv("SPOTIFY_TOKEN_URL")
SPOTIFY_CURRENT_TRACK_URL = os.getenv("SPOTIFY_CURRENT_TRACK_URL")


SONGS_FILE = os.getenv("SONGS_FILE","songs.csv")
CARDS_FILE = os.getenv("CARDS_FILE")
SONGS_FILE = "songs.csv" 

# these songs are from Spotify playlist https://open.spotify.com/playlist/6j841osP77MzMGzpOOVHTs?si=ii_zJFg5SPmUmXqSl8mRww

# Load the playlist from the CSV file
def load_song_playlist():
    """
    Loads the playlist from the CSV file.
    """
    playlist = {}
    if os.path.exists("playlist.csv"):
        with open("playlist.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                song_name, song_number = row
                playlist[song_name] = int(song_number)
    return playlist

# Load the playlist when the application starts
SONG_PLAYLIST = load_song_playlist()



# Initialize the songs file if it doesn't exist or is empty
if not os.path.exists(SONGS_FILE) or os.stat(SONGS_FILE).st_size == 0:
    with open(SONGS_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Song Name", "Song Number"])  # Write header
        # Populate songs.csv from the playlist
        for song_name, song_number in SONG_PLAYLIST.items():
            writer.writerow([song_name, song_number])


@app.route("/validate_card", methods=["POST"])
def validate_card():
    """
    Validates a card by fetching its contents from the Excel file.
    """
    card_number = request.form.get("card_number")
    
    try:
        # Read the corresponding sheet
        card_data = pd.read_excel(CARDS_FILE, sheet_name=card_number)
        card_html = card_data.to_html(index=False, classes="validation-table")
        return jsonify({"success": True, "card_html": card_html})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})
# Define session_data at the beginning of the script
session_data = {"current_song": None, "revealed": False, "hidden": False}
@app.route("/")
def home():
    """
    Home page for Music Bingo.
    """
    if "access_token" not in session:
        return redirect("/login")

    # Use the same logic as generate_table_data to prepare the table data
    table_data = generate_table_data()

    return render_template(
        "home.html",
        show_reveal=not session_data["revealed"],
        table_data=table_data,
    )



@app.route("/generate_playlist", methods=["POST"])
def generate_playlist():
    """
    Executes the playlist generation script (NLTCPlaylist.py).
    """
    try:
        from NLTCPlaylist import main
        main()
        return "Playlist generated successfully."
    except Exception as e:
        return f"Error generating playlist: {e}"


@app.route("/login")
def login():
    """
    Redirects to Spotify authorization page.
    """
    auth_url = (
        "https://accounts.spotify.com/authorize"
        f"?client_id={CLIENT_ID}"
        "&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        "&scope=user-read-playback-state"
    )
    return redirect(auth_url)


@app.route("/callback")
def callback():
    """
    Handles Spotify authorization callback and retrieves access token.
    """
    code = request.args.get("code")
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {"Authorization": f"Basic {auth_header}"}
    data = {"grant_type": "authorization_code", "code": code, "redirect_uri": REDIRECT_URI}

    response = requests.post(SPOTIFY_TOKEN_URL, headers=headers, data=data)
    response_data = response.json()

    if "access_token" in response_data:
        session["access_token"] = response_data["access_token"]
        return redirect("/")
    else:
        return "Failed to authenticate with Spotify."

@app.route("/reveal", methods=["POST"])
def reveal():
    if "access_token" not in session:
        return redirect("/login")

    # Reload the playlist dynamically
    global SONG_PLAYLIST
    SONG_PLAYLIST = load_song_playlist()

    if not os.path.exists(SONGS_FILE):
        with open(SONGS_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Song Name", "Song Number"])  # Write header

    headers = {"Authorization": f"Bearer {session['access_token']}"}
    response = requests.get(SPOTIFY_CURRENT_TRACK_URL, headers=headers)

    song_name = None
    song_number = None
    message = None  # Custom message for unknown songs

    if response.status_code == 200:
        track_info = response.json()
        song_name = track_info.get("item", {}).get("name", None)  # Get song name if available
        song_number = SONG_PLAYLIST.get(song_name, None)  # Get song number, or None if not in the playlist

        if song_number is not None:
            # Song is part of the playlist
            session_data["current_song"] = song_name
            session_data["revealed"] = True
            session_data["hidden"] = False

            # Append the song to the file if it's not already there
            with open(SONGS_FILE, "a", newline="") as file:
                writer = csv.writer(file)

                # Check if the song is already in songs.csv
                with open(SONGS_FILE, "r") as read_file:
                    existing_songs = [row[0] for row in csv.reader(read_file)]
                    if song_name not in existing_songs:
                        writer.writerow([song_name, song_number])
        else:
            # Song is not part of the playlist
            message = "Song not part of the game"
            session_data["current_song"] = None
            session_data["revealed"] = False
            session_data["hidden"] = False
    elif response.status_code == 401:
        # Token expired, clear session and re-authenticate
        session.clear()
        return redirect("/login")

    # Render the appropriate message
    return render_template(
        "index.html",
        show_reveal=False,
        song_name=message if message else song_name,
        song_number="" if message else song_number,
        table_data=generate_table_data()
    )

 

@app.route("/play_game")
def play_game():
    """
    Redirects to the main game page (index.html) with necessary variables.
    """
    # Generate table data (numbers already picked)
    table_data = generate_table_data()
    SONG_PLAYLIST = load_song_playlist()
    # Initialize session data
    session_data = {"current_song": None, "revealed": False, "hidden": False}

    # Render the index.html template with default values
    return render_template(
        "index.html",
        show_reveal=True,  # Default to showing the "Reveal" button
        song_name=None,  # No song revealed initially
        song_number=None,  # No number revealed initially
        table_data=table_data, # Pass the table data
        SONG_PLAYLIST=SONG_PLAYLIST 
    )



# To display the numbers already picked.
def generate_table_data():
    """
    Generates the table data where numbers are arranged in ascending order in their respective positions.
    """
    table_data = [[None for _ in range(15)] for _ in range(5)]  # 5 rows, 15 columns

    if os.path.exists(SONGS_FILE):
        with open(SONGS_FILE, "r") as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            songs = [(int(row[1]), row[0]) for row in reader]  # List of (number, name) tuples
            sorted_songs = sorted(songs)  # Sort by song number

            for number, name in sorted_songs:
                row = (number - 1) // 15  # Determine row (0-indexed)
                col = (number - 1) % 15  # Determine column (0-indexed)
                table_data[row][col] = number  # Place the number in its respective position

    return table_data

@app.route("/generate_cards", methods=["POST"])
def generate_cards():
    """
    Executes the Bingo card generation script (NLTCBingoCardGenerator.py).
    """
    try:
        card_count = int(request.form.get("card_count", 0))
        if card_count < 1 or card_count > 500:
            return "Error: Please enter a number between 1 and 500."
        
        from NLTCBingoCardGenerator import main
        main(card_count)
        return f"{card_count} Bingo cards generated successfully. Check 'MusicBingoCards.xlsx'."
    except Exception as e:
        return f"Error generating cards: {e}"




@app.route("/hide", methods=["POST"])
def hide():
    """
    Hides the currently revealed song.
    """

    session_data["hidden"] = True
    session_data["revealed"] = False
    return redirect("/play_game")

if __name__ == "__main__":
    app.run(debug=True, port=7325)