#Trevor Smith
#Assignment 9
#3/23/25


# Import the gamefunctions module
import gamefunctions
import random

# Game variables
user_hp = 30
user_gold = 10

def display_town_menu():
    """
    Displays the town menu and prompts the user for their choice.
    """
    print("\nYou are in town.")
    print(f"Current HP: {user_hp}, Current Gold: {user_gold}")
    print("What would you like to do?")
    print("1) Leave town (Fight Monster)")
    print("2) Sleep (Restore HP for 5 Gold)")
    print("3) Quit")

def fight_monster():
    """
    Handles the fight between the user and a monster.
    """
    global user_hp, user_gold

    # Generate a random monster
    monster = gamefunctions.new_random_monster()
    print("\nA wild monster appears!")
    print(f"Monster: {monster['name']}")
    print(f"Health: {monster['health']}")
    print(f"Power: {monster['power']}")

    while monster['health'] > 0 and user_hp > 0:
        # Display fight options
        print("\nWhat would you like to do?")
        print("1) Attack")
        print("2) Run away")
        choice = input("Enter your choice: ")

        if choice == "1":
            # User attacks the monster
            user_damage = random.randint(5, 15)  # Random damage between 5 and 15
            monster['health'] -= user_damage
            print(f"\nYou dealt {user_damage} damage to the {monster['name']}!")

            # Monster attacks the user
            monster_damage = random.randint(3, 10)  # Random damage between 3 and 10
            user_hp -= monster_damage
            print(f"The {monster['name']} dealt {monster_damage} damage to you!")

            # Display current stats
            print(f"\nYour HP: {user_hp}")
            print(f"{monster['name']}'s HP: {monster['health']}")

        elif choice == "2":
            # User runs away
            print("\nYou ran away!")
            break

        else:
            print("Invalid choice. Please try again.")

    # Check if the user or monster won
    if monster['health'] <= 0:
        print(f"\nYou defeated the {monster['name']}!")
        user_gold += monster['money']
        print(f"You gained {monster['money']} gold!")
    elif user_hp <= 0:
        print("\nYou were defeated... Game Over!")
        exit()

def sleep():
    """
    Restores the user's HP for 5 gold.
    """
    global user_hp, user_gold

    if user_gold >= 5:
        user_gold -= 5
        user_hp = 30
        print("\nYou slept and restored your HP to 30!")
    else:
        print("\nYou don't have enough gold to sleep.")

def main():
    """
    Main game loop.
    """
    global user_hp, user_gold

    print("Welcome to the game!")
    user_name = input("Please enter your name: ")
    gamefunctions.print_welcome(user_name)

    while True:
        display_town_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            fight_monster()
        elif choice == "2":
            sleep()
        elif choice == "3":
            print("\nThanks for playing! Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the game
if __name__ == "__main__":
    main()
