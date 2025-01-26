import pandas as pd
import random
import os
import csv

# Playlist file
PLAYLIST_FILE = "playlist.csv"
CARDS_FILE = "MusicBingoCards.xlsx"

def load_playlist():
    """
    Loads the playlist from the CSV file and returns it as a list of dictionaries.
    """
    if not os.path.exists(PLAYLIST_FILE):
        raise FileNotFoundError(f"{PLAYLIST_FILE} not found. Run NLTCPlaylist.py first.")
    
    playlist = []
    with open(PLAYLIST_FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            playlist.append(row)
    return playlist

def generate_bingo_card(playlist):
    """
    Generates a single Bingo card using the playlist.
    """
    card = {"B": [], "I": [], "N": [], "G": [], "O": []}

    # Shuffle playlist for randomness
    shuffled_playlist = playlist.copy()
    random.shuffle(shuffled_playlist)

    # Helper function to pick songs for a column
    def pick_songs(start, end, count):
        songs = [song for song in shuffled_playlist if start <= int(song["Song Number"]) <= end]
        return random.sample(songs, count)

    # Populate card
    card["B"] = pick_songs(1, 15, 5)
    card["I"] = pick_songs(16, 30, 5)
    card["N"] = pick_songs(31, 45, 4)  # 4 numbers for N
    card["N"].insert(2, {"Song Name": "FREE", "Song Number": " "})  # Add free space in the center
    card["G"] = pick_songs(46, 60, 5)
    card["O"] = pick_songs(61, 75, 5)

    return card

def save_cards_to_excel(cards, count):
    """
    Saves multiple Bingo cards to a multi-sheet Excel file.
    """
    writer = pd.ExcelWriter(CARDS_FILE, engine="xlsxwriter")

    for i, card in enumerate(cards):
        data = []
        for row in range(5):
            data.append([
                f'{card["B"][row]["Song Name"]} {card["B"][row]["Song Number"]}',
                f'{card["I"][row]["Song Name"]} {card["I"][row]["Song Number"]}',
                f'{card["N"][row]["Song Name"]} {card["N"][row]["Song Number"]}',
                f'{card["G"][row]["Song Name"]} {card["G"][row]["Song Number"]}',
                f'{card["O"][row]["Song Name"]} {card["O"][row]["Song Number"]}',
            ])
        
        df = pd.DataFrame(data, columns=["B", "I", "N", "G", "O"])
        sheet_name = f"{i+1:03d}"  # Generate sheet name like 001, 002, ...
        df.to_excel(writer, index=False, sheet_name=sheet_name)

    # Close the writer to finalize the file
    writer.close()
    print(f"{count} Bingo cards saved to {CARDS_FILE}.")


def main(card_count):
    """
    Main function to generate Bingo cards.
    """
    if card_count > 500:
        raise ValueError("Cannot generate more than 500 cards.")

    print(f"Generating {card_count} Bingo cards...")
    playlist = load_playlist()
    cards = [generate_bingo_card(playlist) for _ in range(card_count)]
    
    # Check for uniqueness
    check_card_uniqueness(cards)

    # Save cards to Excel
    save_cards_to_excel(cards, card_count)
    print("All cards generated successfully.")


def check_card_uniqueness(cards):
    """
    Ensures all generated Bingo cards are unique.
    """
    seen_cards = set()
    for card in cards:
        # Create a string representation of the card for comparison
        card_repr = "".join(
            f'{col["Song Name"]} ({col["Song Number"]})'
            for col in card["B"] + card["I"] + card["N"] + card["G"] + card["O"]
        )
        if card_repr in seen_cards:
            raise ValueError("Duplicate card detected!")
        seen_cards.add(card_repr)
    print("All cards are unique.")


if __name__ == "__main__":
    card_count = int(input("Enter the number of cards to generate (Max: 500): "))
    main(card_count)
