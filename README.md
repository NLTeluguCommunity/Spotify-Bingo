# Spotify-Bingo

This is a Flask-based web application for playing a music-themed bingo game. The app integrates with the Spotify API to fetch currently playing songs and allows players to validate bingo cards against the playlist.

---

## Features

- Integration with Spotify API to fetch the currently playing track.
- Ability to reveal or hide songs during gameplay.
- Validate bingo cards from an Excel sheet containing card data.
- Store song data in a CSV file.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.8+
- pip (Python package manager)

---

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Replace the `CLIENT_ID` and `CLIENT_SECRET` values in the `NLTCMusicBingo.py` file with your Spotify API credentials.

   ### Setting up Spotify API

   To use the Spotify API, follow these steps:

   1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).
   2. Log in with your Spotify account.
   3. Click **Create an App** and fill in the required details (e.g., App Name, Description).
   4. After creating the app, go to the app’s **Settings** and set the **Redirect URI** to:
      ```
      http://127.0.0.1:7325/callback
      ```
   5. Note down the **Client ID** and **Client Secret** from the app’s dashboard.
   6. Replace the placeholder values in the `NLTCMusicBingo.py` file with these credentials.
  
Note: If you would like, I can also add you to my current spotify app.

4. Ensure the following files and directories exist:

   - A file named `songs.csv` will be created automatically upon first used.

---

## Running the Application

1. Start the Flask application:

   ```bash
   python NLTCMusicBingo.py
   ```

2. Open your browser and go to:

   ```
   http://127.0.0.1:7325/
   ```

3. Log in with your Spotify account to authorize the app.

---

## Packages Used

Here are the main Python packages required for the project:

- **Flask**: Web framework to build the application.
- **Requests**: For making HTTP requests to Spotify APIs.
- **pandas**: For handling and validating bingo card data stored in Excel files.
- **openpyxl**: For reading and writing Excel files.
- **python-dotenv**: For managing environment variables.

Install these dependencies using:

```bash
pip install flask requests pandas openpyxl python-dotenv
```

---

## Known Issues

1. If you click "Reveal" without `songs.csv` being present, a `FileNotFoundError` occurs. To fix:

   - Restart the application, and the file will be created automatically.

2. If an unknown song (not part of the predefined playlist) is played, it will be recorded as "Unknown" in `songs.csv`. Clicking "Reveal" for such songs may throw an error. To fix:

   - Ensure the song names in your playlist match the predefined `SONG_PLAYLIST` dictionary. Here is the current playlist I have used https://open.spotify.com/playlist/6j841osP77MzMGzpOOVHTs?si=LH4Jrku5TUKb0GPIQdTGGQ

---

## Enhancements

1. Automatically fetch the correct song names and numbers from Spotify API.
2. Improve error handling for missing or misconfigured files.

---

## Folder Structure

```
.
├── static/
│   └── background.png       # Background image for the web UI
├── templates/
│   ├── index.html           # Main HTML file for the UI
├── songs.csv                # Automatically generated file for storing song data
├── MusicBingoCards_Final.xlsx # Excel file containing bingo card data
├── NLTCMusicBingo.py        # Main Python application
├── requirements.txt         # List of required Python packages
└── README.md                # Project documentation
```

---


## Author

Developed by Jyothsna Priya Kattakinda.

