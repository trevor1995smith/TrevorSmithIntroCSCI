#Trevor Smith
#Assignment 8
#3/23/25
#Functions with DocStrings

import random #imports the random package

def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    if __name__ == "__main__":
        purchase_item()
    """
    Calculates the number of items that can be purchased and the leftover money.

    Parameters:
    itemPrice (float): The price of one item.
    startingMoney (float): The amount of money available for purchase.
    quantityToPurchase (int, optional): The desired quantity to purchase. Defaults to 1.

    Returns:
    tuple: A tuple containing:
        - quantityToPurchase (int): The number of items that can be purchased.
        - leftover_money (float): The amount of money remaining after the purchase.

    Examples:
    >>> purchase_item(1.23, 10, 3)
    (3, 6.31)  # Purchases 3 items, $6.31 leftover

    """
    
    total_cost = itemPrice * quantityToPurchase # total cost of purchase

    if total_cost > startingMoney:
        quantityToPurchase = int(startingMoney // itemPrice) #how many can be bought with startingMoney

    leftover_money = startingMoney - (itemPrice * quantityToPurchase) #how much money is leftover
    
    return quantityToPurchase, leftover_money #returns the number to purchase and leftover money

def visit_shop(user_gold, inventory):
    """Allows the user to buy items from the shop."""

    # Shop items
    shop_items = [
        {"name": "Sword", "type": "weapon", "price": 15, "damage_bonus": 5, "durability": 5},
        {"name": "Axe", "type": "weapon", "price": 10, "damage_bonus": 3, "durability": 3},
        {"name": "Monster Repellent", "type": "weapon", "price": 8, "damage_bonus": 0, "durability": 1, "effect": "auto_defeat"},
        {"name": "Health Potion", "type": "consumable", "price": 5, "effect": "heal", "amount": 10}
    ]
    
    print("\nWelcome to the shop!")
    print(f"Your gold: {user_gold}")
    print("Available items:")
    
    for i, item in enumerate(shop_items, 1):
        print(f"{i}) {item['name']} - {item['price']} gold (Type: {item['type']})")
    
    print(f"{len(shop_items)+1}) Back to town")
    
    while True:
        choice = input("Enter your choice: ")
        
        try:
            choice = int(choice)
            if choice == len(shop_items)+1:
                return user_gold, inventory
            elif 1 <= choice <= len(shop_items):
                selected_item = shop_items[choice-1]
                if user_gold >= selected_item['price']:
                    user_gold -= selected_item['price']
                    # Create a new copy of the item for inventory
                    new_item = selected_item.copy()
                    # For weapons, add current durability equal to max durability
                    if new_item['type'] == 'weapon':
                        new_item['current_durability'] = new_item['durability']
                    inventory.append(new_item)
                    print(f"\nYou bought {selected_item['name']}!")
                    print(f"Remaining gold: {user_gold}")
                    break
                else:
                    print("\nNot enough gold!")
                    break
            else:
                print("\nInvalid choice. Please try again.")
        except ValueError:
            print("\nPlease enter a number.")
    return user_gold, inventory
    
def manage_inventory(equipped_weapon, user_hp, inventory):
    """Allows the user to view, equip, unequip, and use items."""
    
    while True:
        print("\n=== INVENTORY ===")
        if not inventory:
            print("Your inventory is empty.")
            print("1) Back to town")
            choice = input("Enter your choice: ")
            if choice == "1":
                return
            continue
        
        # Display equipped weapon status
        if equipped_weapon:
            print(f"Currently equipped: {equipped_weapon['name']} "
                  f"({equipped_weapon.get('current_durability', equipped_weapon['durability'])}/{equipped_weapon['durability']} dura)")
        else:
            print("No weapon currently equipped")
        
        # Display all items
        for i, item in enumerate(inventory, 1):
            item_info = f"{i}) {item['name']} ({item['type']})"
            if item == equipped_weapon:
                item_info += " [EQUIPPED]"
            elif item['type'] == 'weapon':
                durability = item.get('current_durability', item['durability'])
                item_info += f" [Weapon - {durability}/{item['durability']} dura]"
            print(item_info)
        
        print(f"\nOptions:")
        print("1-{}) Select item".format(len(inventory)))
        if equipped_weapon:
            print("U) Unequip current weapon")
        print("B) Back to town")
        
        choice = input("\nWhat would you like to do? ").upper()

        if choice == "B":
            return
        elif choice == "U" and equipped_weapon:
            print(f"\nYou unequipped {equipped_weapon['name']}")
            equipped_weapon = None
            continue
        else:
            try:
                choice = int(choice)
                if 1 <= choice <= len(inventory):
                    selected_item = inventory[choice-1]
                    
                    if selected_item['type'] == "weapon":
                        if selected_item == equipped_weapon:
                            print(f"\n{selected_item['name']} is already equipped!")
                        else:
                            if equipped_weapon:
                                print(f"\nSwapped {equipped_weapon['name']} for {selected_item['name']}")
                            else:
                                print(f"\nEquipped {selected_item['name']}")
                            equipped_weapon = selected_item
                    
                    elif selected_item['type'] == "consumable":
                        user_hp, inventory = use_consumable(selected_item, user_hp, inventory)
                        return  # Return to town after using consumable
                    
                    else:
                        print("\nThis item has no special use.")
                else:
                    print("\nInvalid choice. Please try again.")
            except ValueError:
                print("\nPlease enter a valid item number or command.")
            return equipped_weapon, user_hp

def use_consumable(item, user_hp, inventory):
    """Uses a consumable item from the inventory."""
    
    if item['effect'] == "heal":
        user_hp += item['amount']
        print(f"You used {item['name']} and healed {item['amount']} HP!")
    elif item['effect'] == "auto_defeat":
        print(f"You used {item['name']} - it will automatically defeat the next monster!")
    
    inventory.remove(item)

    return user_hp, inventory
                
def new_random_monster(): #creates a new function new_random_monster
    if __name__ == "__main__":
        new_random_monster()
    """
    Generates a random monster with attributes such as name, description, health, power, and money.

    Returns:
    dict: A dictionary containing the monster's attributes:
        - name (str): The name of the monster.
        - description (str): A description of the monster.
        - health (int): The health of the monster, randomly generated within a range.
        - power (int): The power of the monster, randomly generated within a range.
        - money (int): The money the monster carries, randomly generated within a range.

    Example:
    >>> new_random_monster()
    {
        'name': 'Vampire',
        'description': 'Vampires are very dangerous at night...',
        'health': 25,
        'power': 8,
        'money': 15
    }
    
    """
    #creates a dictionary within a list
    monsters = [
        {   'name': 'Vampire',
            'description': 'Vampires are very dangerous at night, and causes death to a player if encountered within 5 feet.',
            'health_range': (10, 40),  
            'power_range': (5, 10),    
            'money_range': (3, 25)},
        {
            'name': 'Bigfoot',
            'description': 'Bigfoot specializes in camouflage, and can cause heavy damage to a player if encountered.',
            'health_range': (15, 75),    
            'power_range': (10, 20),     
            'money_range': (10, 50)},
        {
            'name': 'Dragon',
            'description': 'Dragons can breathe fire, causing heavy damage if burned, they can also capture players.',
            'health_range': (50, 100),
            'power_range': (20, 40),   
            'money_range': (50, 100)}
        ]
    
    # randomnly selects a monster from the list above
    monster = random.choice(monsters)
    
    # randomnly chooses a number for health, power, money within the range provided above
    health = random.randint(monster['health_range'][0], monster['health_range'][1])
    power = random.randint(monster['power_range'][0], monster['power_range'][1])
    money = random.randint(monster['money_range'][0], monster['money_range'][1])

    # creates and returns the monster dictionary
    return {
        'name': monster['name'],
        'description': monster['description'],
        'health': health,
        'power': power,
        'money': money
    }


def print_welcome(name, width=20):
    if __name__ == "__main__":
        print_welcome()
    """
    Prints a welcome message for the supplied 'name' parameter.
    The output is centered within a field of the specified width.

    Parameters:
    name (str): The name to include in the welcome message.
    width (int, optional): The width of the field for centering the message. Defaults to 20.

    Returns:
    None

    Example:
    >>> print_welcome("Jason")
       Hello, Jason!            

    """
    # Print the welcome message, centered within the specified width
    print(f'{f"Hello, {name}!":^{width}}')


def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    if __name__ == __main__:
        print_shop_menu()
    """
    Prints a sign that contains a list of two items and their corresponding prices.
    Items are left-aligned in the menu, while the prices are right-aligned (with decimal points lining up).
    Prices are formatted to show 2 decimal places, and preceded with a dollar sign
    (with no space between the dollar sign and the price).
    The item name field has 12 characters, and the item price field has 8 characters.
    The sign is surrounded with a nice border to differentiate it from other text.

    Parameters:
    item1Name (str): The name of the first item.
    item1Price (float): The price of the first item.
    item2Name (str): The name of the second item.
    item2Price (float): The price of the second item.

    Returns:
    None

    Example:
    >>> print_shop_menu('Bag of Chips', 7, 'Orange', 1.234)

    """

    print('/----------------------\\') #print border
    print(f'| {item1Name:<12} ${item1Price:>7.2f} |') #print the first item and price
    print(f'| {item2Name:<12} ${item2Price:>7.2f} |') #print the second item and price
    print('\\----------------------/') #print border

def display_town_menu(user_hp, user_gold, equipped_weapon):
    """Displays the town menu and prompts the user for their choice."""
    print("\nYou are in town.")
    print(f"Current HP: {user_hp}, Current Gold: {user_gold}")
    if equipped_weapon:
        print(f"Equipped Weapon: {equipped_weapon['name']} (Durability: {equipped_weapon['durability']})")
    print("What would you like to do?")
    print("1) Leave town (Fight Monster)")
    print("2) Sleep (Restore HP for 5 Gold)")
    print("3) Visit Shop")
    print("4) Manage Inventory")
    print("5) Quit")

def fight_monster(user_hp, user_gold):
    """
    Handles the fight between the user and a monster.
    """
    # Generate a random monster
    monster = new_random_monster()
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
    return user_hp, user_gold

def sleep(user_hp, user_gold):
    """
    Restores the user's HP for 5 gold.
    """
    if user_gold >= 5:
        user_gold -= 5
        user_hp = 30
        print("\nYou slept and restored your HP to 30!")
    else:
        print("\nYou don't have enough gold to sleep.")
    return user_hp, user_gold






        
