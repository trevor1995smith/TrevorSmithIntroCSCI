#Trevor Smith
#Assignment 11
#4/6/25

import json
import os

def save_game(filename, game_data):
    """Saves the game data to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump(game_data, f)
        print(f"Game saved successfully to {filename}!")
        return True
    except Exception as e:
        print(f"Error saving game: {e}")
        return False

def load_game(filename):
    """Loads game data from a JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Save file {filename} not found!")
        return None
    except Exception as e:
        print(f"Error loading game: {e}")
        return None

def get_save_files():
    """Returns a list of available save files"""
    return [f for f in os.listdir() if f.endswith('.sav')]
