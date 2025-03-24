#Trevor Smith
#Assignment 8
#3/23/25
#Functions with DocStrings and game.py importing gamefunctions.py

import random #imports the random package

def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
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

#assigns the function to num_purchased, leftovermoney and tests them with print functions

print('purchase_item function')
print('----------------------')
print()
num_purchased, leftover_money = purchase_item(1.23, 10, 3) 
print("Test 1")
print(f'Number of items purchased: {num_purchased}')
print(f'Amount of money leftover: ${leftover_money: .2f}')
print()
num_purchased, leftover_money = purchase_item(1.23, 2.01, 3)
print("Test 2")
print(f'Number of items purchased: {num_purchased}')
print(f'Amount of money leftover: ${leftover_money: .2f}')
print()
num_purchased, leftover_money = purchase_item(3.41, 21.12)
print("Test 3")
print(f'Number of items purchased: {num_purchased}')
print(f'Amount of money leftover: ${leftover_money: .2f}')
print()
num_purchased, leftover_money = purchase_item(31.41, 21.12)
print("Test 4")
print(f'Number of items purchased: {num_purchased}')
print(f'Amount of money leftover: ${leftover_money: .2f}')

print() #adds space between functions
print("new_random_monster function")
print('---------------------------')
print() #adds space between print lines

def new_random_monster(): #creates a new function new_random_monster
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

#assigns my_monster with the function new_random_monster and calls the function 3 times
for _ in range(3):
    my_monster = new_random_monster()

    #prints the randomnly selected monster profile
    print(f"Monster: {my_monster['name']}")
    print(f"Description: {my_monster['description']}")
    print(f"Health: {my_monster['health']}")
    print(f"Power: {my_monster['power']}")
    print(f"Money: {my_monster['money']}")
    print()

print() #space in between function results

def print_welcome(name, width=20):
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

#Testing
print('print_welcome function')
print('----------------------')
print()
print_welcome("Jason")
print()
print_welcome("Charlie")
print()
print_welcome("Lexy")

print() #space in between function results


def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
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


# Testing the function three times with different items and prices
print('print_shop_menu function')
print('------------------------')
print()
print_shop_menu('Bag of Chips', 7, 'Orange', 1.234)
print()
print_shop_menu('Eggs', 6.556, 'Bread', 10.48)
print()
print_shop_menu('Banana', 0.99, 'Juice', 2.50)


# Use the __name__ variable to create a test client

def test_functions(print_welcome, print_shop_menu, new_random_monster, purchase_item):
    if __name__ == "__main__":
        test_functions()
#######################################################################################
#game.py importing gamefunctions.py
# Import the gamefunctions module
import gamefunctions

def demo_game():
    # Welcome the user
    print("Welcome to the game!")
    user_name = input("Please enter your name: ")
    gamefunctions.print_welcome(user_name)

    # Demonstrate purchase_item function
    print("\nLet's simulate a purchase!")
    item_price = float(input("Enter the price of the item: "))
    starting_money = float(input("Enter the amount of money you have: "))
    quantity = int(input("Enter the quantity you want to purchase (default is 1): ") or 1)
    num_purchased, leftover_money = gamefunctions.purchase_item(item_price, starting_money, quantity)
    print(f"\nYou can purchase {num_purchased} items.")
    print(f"After the purchase, you will have ${leftover_money:.2f} left.")

    # Demonstrate new_random_monster function
    print("\nLet's generate a random monster!")
    input("Press Enter to generate a monster...")
    monster = gamefunctions.new_random_monster()
    print("\nHere's your monster:")
    print(f"Name: {monster['name']}")
    print(f"Description: {monster['description']}")
    print(f"Health: {monster['health']}")
    print(f"Power: {monster['power']}")
    print(f"Money: {monster['money']}")

    # Demonstrate print_shop_menu function
    print("\nLet's create a shop menu!")
    item1_name = input("Enter the name of the first item: ")
    item1_price = float(input(f"Enter the price of {item1_name}: "))
    item2_name = input("Enter the name of the second item: ")
    item2_price = float(input(f"Enter the price of {item2_name}: "))
    print("\nHere's your shop menu:")
    gamefunctions.print_shop_menu(item1_name, item1_price, item2_name, item2_price)

    # End of game
    print("\nThank you for playing!")

# Run the game
if __name__ == "__main__":
    demogame()
