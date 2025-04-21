#Trevor Smith
#Assignment 13
#4/20/25

import random
import json
import os
import glob
import sys
from wanderingMonster import WanderingMonster

# Game constants
GRID_SIZE = 10

def show_main_menu():
    """Display main menu and return game state."""
    print("\nMAIN MENU")
    print("1) New Game")
    print("2) Load Game")
    print("3) Quit")
    
    while True:
        choice = input("Choose an option: ")
        if choice == "1": return initialize_game_state()
        elif choice == "2": return show_load_menu()
        elif choice == "3": return None
        print("Invalid choice!")

def show_load_menu():
    """Display load menu and return game state."""
    save_files = glob.glob("*.sav")
    if not save_files:
        print("No saved games found! Starting new game.")
        return initialize_game_state()
    
    print("\nAvailable Saved Games:")
    for i, file in enumerate(save_files, 1):
        print(f"{i}) {file}")
    print(f"{len(save_files)+1}) Back")
    
    while True:
        try:
            choice = int(input("Choose a save file: "))
            if choice == len(save_files)+1: return show_main_menu()
            if 1 <= choice <= len(save_files): return load_game_state(save_files[choice-1])
        except ValueError: pass
        print("Invalid choice!")

def show_save_menu(game_state):
    """Display save menu options."""
    print("\nSAVE MENU")
    print("1) Quick Save (autosave.sav)")
    print("2) Save As...")
    print("3) Load Game")
    print("4) Back")
    
    while True:
        choice = input("Choose an option: ")
        if choice == "1":
            save_game_state(game_state, "autosave.sav")
            print("Game saved to autosave.sav!")
            break
        elif choice == "2":
            filename = input("Enter save file name (e.g., mysave.sav): ")
            if not filename.endswith('.sav'):
                filename += '.sav'
            save_game_state(game_state, filename)
            print(f"Game saved to {filename}!")
            break
        elif choice == "3": 
            return show_load_menu()
        elif choice == "4": 
            break
        print("Invalid choice!")

def initialize_game_state():
    """Initialize new game state with default values."""
    return {
        'player_pos': [0, 0],
        'town_pos': [GRID_SIZE-1, GRID_SIZE-1],
        'user_hp': 30,
        'user_gold': 20,
        'inventory': [],
        'equipped_weapon': None,
        'monsters': []
    }

def load_game_state(filename):
    """Load game state from file, reconstructing monsters."""
    try:
        with open(filename, 'r') as f:
            state = json.load(f)
            print(f"Game loaded from {filename}!")
            
            # Reconstruct monsters from saved data
            if 'monsters' in state:
                state['monsters'] = [WanderingMonster(data=m) for m in state['monsters']]
            
            return {**initialize_game_state(), **state}
    except Exception as e:
        print(f"Error loading saved game: {e}. Starting new game.")
        return initialize_game_state()

def save_game_state(game_state, filename):
    """Save game state to file, converting monsters to dicts."""
    state_to_save = game_state.copy()
    state_to_save['monsters'] = [m.to_dict() for m in state_to_save.get('monsters', [])]
    
    with open(filename, 'w') as f:
        json.dump(state_to_save, f)

def print_welcome(name="Adventurer", width=20):
    """Print welcome message."""
    print(f'{f"Hello, {name}!":^{width}}')

def fight_monster(user_hp, user_gold, equipped_weapon, inventory, monster):
    """Handle combat with a monster."""
    print(f"\nA wild {monster.name} appears!")
    print(f"Health: {monster.health}, Power: {monster.power}")
    
    if equipped_weapon and equipped_weapon.get('effect') == 'auto_defeat':
        print(f"\nUsed {equipped_weapon['name']} to instantly defeat {monster.name}!")
        equipped_weapon['current_durability'] -= 1
        if equipped_weapon['current_durability'] <= 0:
            print(f"Your {equipped_weapon['name']} has been used up!")
            inventory.remove(equipped_weapon)
            equipped_weapon = None
        user_gold += monster.money
        print(f"Gained {monster.money} gold!")
        return user_hp, user_gold, equipped_weapon, inventory, True

    while monster.health > 0 and user_hp > 0:
        print("\n1) Attack")
        print("2) Run away")
        if equipped_weapon:
            print(f"({equipped_weapon['name']} durability: {equipped_weapon['current_durability']}/{equipped_weapon['durability']})")
        
        choice = input("Choose: ")
        
        if choice == "1":
            damage = random.randint(3,6) + (equipped_weapon['damage_bonus'] if equipped_weapon else 0)
            monster.health -= damage
            print(f"\nYou dealt {damage} damage!")
            
            if equipped_weapon:
                equipped_weapon['current_durability'] -= 1
                if equipped_weapon['current_durability'] <= 0:
                    print(f"Your {equipped_weapon['name']} broke!")
                    inventory.remove(equipped_weapon)
                    equipped_weapon = None
            
            user_hp -= monster.power
            print(f"The {monster.name} hit you for {monster.power} damage!")
            print(f"Your HP: {user_hp}, Monster HP: {monster.health}")
        
        elif choice == "2":
            print("\nYou ran away!")
            break
    
    defeated = False
    if monster.health <= 0:
        user_gold += monster.money
        print(f"\nDefeated {monster.name}! Gained {monster.money} gold!")
        defeated = True
    elif user_hp <= 0:
        print("\nGame Over!")
        sys.exit()
    
    print("\nReturn to town (green square) to replenish health and weapons!")
    return user_hp, user_gold, equipped_weapon, inventory, defeated

def manage_inventory(equipped_weapon, user_hp, inventory):
    """Handle inventory management menu."""
    while True:
        print("\n=== INVENTORY ===")
        if equipped_weapon:
            print(f"Equipped: {equipped_weapon['name']} (Durability: {equipped_weapon['current_durability']}/{equipped_weapon['durability']})")
        
        if not inventory:
            print("Your inventory is empty")
            print("1) Back to town")
            choice = input("Choose: ")
            if choice == "1":
                break
            continue
        
        for i, item in enumerate(inventory, 1):
            durability_info = ""
            if item['type'] == "weapon":
                durability_info = f" (Durability: {item['current_durability']}/{item['durability']})"
            print(f"{i}) {item['name']}{durability_info}")
        
        print(f"{len(inventory)+1}) Back to town")
        
        choice = input("Choose an item: ")
        try:
            choice = int(choice)
            if choice == len(inventory)+1:
                break
            elif 1 <= choice <= len(inventory):
                item = inventory[choice-1]
                if item['type'] == "weapon":
                    equipped_weapon = item
                    print(f"Equipped {item['name']}")
                elif item['type'] == "consumable":
                    user_hp += item['amount']
                    inventory.remove(item)
                    print(f"Used {item['name']}. HP now: {user_hp}")
        except ValueError:
            print("Please enter a number!")
    
    return equipped_weapon, user_hp, inventory

def visit_shop(user_gold, inventory):
    """Handle shop menu and purchases."""
    shop_items = [
        {"name": "Sword", "type": "weapon", "price": 15, "damage_bonus": 5, "durability": 5, "current_durability": 5},
        {"name": "Axe", "type": "weapon", "price": 10, "damage_bonus": 3, "durability": 3, "current_durability": 3},
        {"name": "Health Potion", "type": "consumable", "price": 5, "effect": "heal", "amount": 10},
        {"name": "Monster Potion", "type": "weapon", "price": 20, "effect": "auto_defeat", "durability": 1, "current_durability": 1}
    ]
    
    while True:
        print("\nWelcome to the shop!")
        print(f"Your gold: {user_gold}")
        print("Available items:")
        
        for i, item in enumerate(shop_items, 1):
            durability_info = ""
            if item['type'] == "weapon":
                durability_info = f" (Durability: {item['current_durability']}/{item['durability']})"
            print(f"{i}) {item['name']} - {item['price']} gold{durability_info}")
        
        print(f"{len(shop_items)+1}) Back to town")
        
        choice = input("Choose an item: ")
        try:
            choice = int(choice)
            if choice == len(shop_items)+1:
                break
            elif 1 <= choice <= len(shop_items):
                item = shop_items[choice-1]
                if user_gold >= item['price']:
                    user_gold -= item['price']
                    inventory.append(item.copy())
                    print(f"You bought {item['name']}!")
                else:
                    print("Not enough gold!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter a number!")
    
    return user_gold, inventory

def sleep(user_hp, user_gold):
    """Handle sleeping to restore HP."""
    cost = 5
    if user_gold >= cost:
        user_gold -= cost
        user_hp = 30
        print("\nYou slept and restored your HP to 30!")
    else:
        print("\nYou don't have enough gold to sleep.")
    return user_hp, user_gold

def display_town_menu(user_hp, user_gold, equipped_weapon):
    """Display town menu options."""
    print("\nYou are in town.")
    print(f"HP: {user_hp}, Gold: {user_gold}")
    if equipped_weapon:
        print(f"Weapon: {equipped_weapon['name']} (Durability: {equipped_weapon['current_durability']}/{equipped_weapon['durability']})")
    print("\n1) Leave town")
    print("2) Sleep (Restore HP for 5 Gold)")
    print("3) Visit Shop")
    print("4) Manage Inventory")
    print("5) Save and Quit")


