from flask import Flask, render_template, request, session, redirect, jsonify
import requests
import base64
import csv
import os
import pandas as pd

# Replace this with the exact path where you want to save the file
SONGS_FILE = "/Users/jyothsna.kattakinda/documents/nltctest/songs.csv"
# You don't have to create songs.csv, when you run the code for first time songs.csv is automatically created.
# when the program is executed, a songs.csv file is created automatically.

# Known Bug 2: If you click on reveal without the songs.csv, it throws an "FileNotFoundError:" error. Fix this by catching the exception.
# Workaround for this is to rerun the program again.

# Ensure the directory exists
os.makedirs(os.path.dirname(SONGS_FILE), exist_ok=True)



app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a strong secret key

# Spotify API credentials
CLIENT_ID = ""  # Replace with your Spotify app's Client ID
CLIENT_SECRET = ""  # Replace with your Spotify app's Client Secret
REDIRECT_URI = "http://127.0.0.1:7325/callback" 
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_CURRENT_TRACK_URL = "https://api.spotify.com/v1/me/player/currently-playing"

SONGS_FILE = "songs.csv"  # File to store song details

# The songs here are hard coded and assigned a number from 1 to 75 (as Bingo card contains 75 numbers)
# The code only works for these 75 songs any other would be assigned to a value "Unknown" - you can verify this in the generated songs.csv file
 

# Enhancement 1: Please also note that the name of the song here should match with the spotify song name. 
# You can use spotify APIs to get the name and finetune this current code.
# these songs are from Spotify playlist https://open.spotify.com/playlist/6j841osP77MzMGzpOOVHTs?si=ii_zJFg5SPmUmXqSl8mRww

SONG_PLAYLIST = {
    "Kissik (From \"Pushpa 2 The Rule\") [TELUGU]": 1,
    "Bangaru Kalla": 2,
    "Kurchi Madathapetti": 3,
    "Buttabomma - Telugu": 4,
    "Subhalekha": 5,
    "Janavule Nerajanavule": 6,
    "Kanya Kumaari": 7,
    "Inkem Inkem Inkem Kaavaale": 8,
    "Abbanee": 9,
    "Samajavaragamana": 10,
    "Rowdy Baby": 11,
    "Undiporaadhey": 12,
    "Kadalalle (From \"Dear Comrade\")": 13,
    "Blockbuster Pongal (From \"Sankranthiki Vasthunam\")": 14,
    "Manohari": 15,
    "Vayari Bhama": 16,
    "Nelluri Nerajana": 17,
    "O Sakkanoda (From \"Guru\")": 18,
    "Whattey Beauty - Telugu": 19,
    "Jalsa Jalsa": 20,
    "Nuvvasthanante": 21,
    "Jigelu Rani (From \"Rangasthalam\")": 22,
    "Kevvu Keka": 23,
    "Dhimmathirigae": 24,
    "Barbie Girl": 25,
    "Choolenge Aasma": 26,
    "Diyalo Diyala": 27,
    "Ek Niranjan": 28,
    "Pilichina": 29,
    "Radhe Govinda": 30,
    "Singles Anthem - Telugu": 31,
    "Nee Kallalona (From \"Jai Lava Kusa\")": 32,
    "Come To The Party": 33,
    "Peelings [TELUGU]": 34,
    "Vennelave Vennelave": 35,
    "Tauba Tauba": 36,
    "Hello Guru": 37,
    "Andhamyna Bhamalu": 38,
    "Cinema Choopistha Mama": 39,
    "Andamaina Premarani": 40,
    "Naalo Chilipi Kala (Theme Song)": 41,
    "Crazy Feeling": 42,
    "Dimaak Kharaab - From \"Ismart Shankar\"": 43,
    "Pakka Local (From \"Janatha Garage\")": 44,
    "Arere Vaanaa": 45,
    "Feel My Love": 46,
    "Hey Pillagaada": 47,
    "Ma Ma Mahesha (From \"Sarkaru Vaari Paata\")": 48,
    "Super Machi": 49,
    "Kung Fu Kumaari": 50,
    "Oka Maaru": 51,
    "Dhaari Choodu": 52,
    "Sailaja Sailaja": 53,
    "Raanu Raanu": 54,
    "Boss Party (From \"Waltair Veerayya\")": 55,
    "Bapu Gari Bommo": 56,
    "Yentha Sakkagunnave (From \"Rangasthalam\")": 57,
    "Darlingey": 58,
    "Ramuloo Ramulaa": 59,
    "Lux Papa": 60,
    "Sankranthi": 61,
    "Guruvaram": 62,
    "Gaajuvaka Pilla": 63,
    "Baavavi Nuuvu": 64,
    "Banthi Poola Janaki": 65,
    "Bullettu Bandi": 66,
    "Oo Antava Oo Oo Antava (From \"Pushpa - The Rise\")(Telugu)": 67,
    "Andala Ada Bomma": 68,
    "Dai Dai Dhamma": 69,
    "Mama Ek Peg La": 70,
    "Guche Gulabi": 71,
    "Tillu Anna DJ Pedithe": 72,
    "Godari Gattu Meedha (From \"Sankranthiki Vasthunam\")": 73,
    "Ay Pilla - Telugu": 74,
    "Nenu Nuvvantu": 75,
}



# Initialize the songs file if it doesn't exist
if not os.path.exists(SONGS_FILE):
    with open(SONGS_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Song Name", "Song Number"])  # Write header

CARDS_FILE = "/Users/jyothsna.kattakinda/downloads/MusicBingoCards_Final.xlsx"  # Update the path - here is where the bingo cards are stored.

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
        "index.html",
        show_reveal=not session_data["revealed"],
        table_data=table_data,
    )




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

# Known Bug 1: There is a known bug in this method, if an unknown song (not part of the playlist) is played, the record in songs.csv is saved as unknown
# for the corresponding song. When you click on reveal it throws error, as type int is expected but found string (unknown).
@app.route("/reveal", methods=["POST"])
def reveal():
    """
    Reveals the currently playing song.
    """
    if "access_token" not in session:
        return redirect("/login")

    headers = {"Authorization": f"Bearer {session['access_token']}"}
    response = requests.get(SPOTIFY_CURRENT_TRACK_URL, headers=headers)

    song_name = None
    song_number = None

    if response.status_code == 200:
        track_info = response.json()
        song_name = track_info["item"]["name"]
        song_number = SONG_PLAYLIST.get(song_name, "Unknown")
        session_data["current_song"] = song_name
        session_data["revealed"] = True
        session_data["hidden"] = False

        # Check if the song is already present in the file
        with open(SONGS_FILE, "r") as file:
            reader = csv.reader(file)
            existing_songs = [row for row in reader]

        # Append the song only if it's not already in the file
        if [song_name, song_number] not in existing_songs:
            with open(SONGS_FILE, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([song_name, song_number])
    elif response.status_code == 401:
        # Token expired, clear session and re-authenticate
        session.clear()
        return redirect("/login")

    return render_template(
        "index.html",
        show_reveal=False,
        song_name=song_name,
        song_number=song_number,
        table_data=generate_table_data()
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


@app.route("/hide", methods=["POST"])
def hide():
    """
    Hides the currently revealed song.
    """
    session_data["hidden"] = True
    session_data["revealed"] = False
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=7325)