#Trevor Smith
#Assignment 11
#4/6/25

import json
import os
import random
import gamefunctions

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

def main():
    """
    Main game loop with save/load functionality.
    """
    print("Welcome to the game!")
    
    # Ask if user wants to load a game
    save_files = get_save_files()
    if save_files:
        print("\nWould you like to:")
        print("1) Start a new game")
        print("2) Load a saved game")
        choice = input("Enter your choice (1 or 2): ")
        
        if choice == "2":
            print("\nAvailable save files:")
            for i, filename in enumerate(save_files, 1):
                print(f"{i}) {filename}")
            print(f"{len(save_files)+1}) Cancel and start new game")
            
            try:
                load_choice = int(input("Select a save file to load: "))
                if 1 <= load_choice <= len(save_files):
                    game_data = load_game(save_files[load_choice-1])
                    if game_data:
                        user_hp = game_data['user_hp']
                        user_gold = game_data['user_gold']
                        inventory = game_data['inventory']
                        equipped_weapon = game_data.get('equipped_weapon')
                        user_name = game_data.get('user_name', 'Adventurer')
                        print(f"\nWelcome back, {user_name}!")
                    else:
                        # If loading failed, start new game
                        user_name = input("Please enter your name: ")
                        user_hp = 30
                        user_gold = 10
                        inventory = []
                        equipped_weapon = None
                else:
                    # Start new game
                    user_name = input("Please enter your name: ")
                    user_hp = 30
                    user_gold = 10
                    inventory = []
                    equipped_weapon = None
            except ValueError:
                print("Invalid input. Starting new game.")
                user_name = input("Please enter your name: ")
                user_hp = 30
                user_gold = 10
                inventory = []
                equipped_weapon = None
        else:
            # Start new game
            user_name = input("Please enter your name: ")
            user_hp = 30
            user_gold = 10
            inventory = []
            equipped_weapon = None
    else:
        # No save files, start new game
        user_name = input("Please enter your name: ")
        user_hp = 30
        user_gold = 10
        inventory = []
        equipped_weapon = None
    
    gamefunctions.print_welcome(user_name)

    while True:
        print("\nYou are in town.")
        print(f"Current HP: {user_hp}, Current Gold: {user_gold}")
        if equipped_weapon:
            print(f"Equipped Weapon: {equipped_weapon['name']} (Durability: {equipped_weapon.get('current_durability', equipped_weapon['durability'])}/{equipped_weapon['durability']})")
        print("What would you like to do?")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Visit Shop")
        print("4) Manage Inventory")
        print("5) Save and Quit")
        print("6) Quit without saving")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            user_hp, user_gold = gamefunctions.fight_monster(user_hp, user_gold)
        elif choice == "2":
            user_hp, user_gold = gamefunctions.sleep(user_hp, user_gold)
        elif choice == "3":
            user_gold, inventory = gamefunctions.visit_shop(user_gold, inventory)
        elif choice == "4":
            equipped_weapon, user_hp = gamefunctions.manage_inventory(equipped_weapon, user_hp, inventory)
        elif choice == "5":
            # Save and Quit
            game_data = {
                'user_name': user_name,
                'user_hp': user_hp,
                'user_gold': user_gold,
                'inventory': inventory,
                'equipped_weapon': equipped_weapon
            }
            filename = f"{user_name}_save.sav"
            if save_game(filename, game_data):
                print("Game saved. Goodbye!")
                break
        elif choice == "6":
            print("\nThanks for playing! Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

