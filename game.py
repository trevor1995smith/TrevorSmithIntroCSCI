#Trevor Smith
#Assignment 10
#4/3/25


# Import the gamefunctions module
import gamefunctions
import random

def main():
    """
    Main game loop.
    """
    user_hp = 30
    user_gold = 10
    inventory = []
    equipped_weapon = None  # Initialize as None at the global level

    print("Welcome to the game!")
    user_name = input("Please enter your name: ")
    gamefunctions.print_welcome(user_name)

    while True:
        gamefunctions.display_town_menu(user_hp, user_gold, equipped_weapon)
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
            print("\nThanks for playing! Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the game
if __name__ == "__main__":
    main()
