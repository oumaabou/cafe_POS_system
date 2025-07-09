import random

# ============================
# Global Data Structures
# ============================

menu = [
    {'name': 'Carrot Juice', 'price': 3.5, 'recipe': {'Carrot': 1}},
    {'name': 'Café au Lait', 'price': 4.0, 'recipe': {'Coffee Beans': 1, 'Milk': 1}},
    {'name': 'Mango Smoothie', 'price': 5.0, 'recipe': {'Mango': 2, 'Yogurt': 1}},
    {'name': 'Tropical Punch', 'price': 4.5, 'recipe': {'Mango': 1, 'Pineapple': 1, 'Orange': 1}}
]

inventory = {
    'Carrot': {'stock': 10, 'restock_price': 0.5},
    'Coffee Beans': {'stock': 10, 'restock_price': 1.2},
    'Milk': {'stock': 10, 'restock_price': 0.8},
    'Mango': {'stock': 10, 'restock_price': 1.0},
    'Yogurt': {'stock': 5, 'restock_price': 0.75},
    'Pineapple': {'stock': 5, 'restock_price': 1.5},
    'Orange': {'stock': 5, 'restock_price': 0.7}
}

prepared_items = {}
orders = []
wallet = [50.0]

# ============================
# Functions
# ============================

def view_menu():
    print("\n=== Café Menu ===")
    for idx, item in enumerate(menu, 1):
        recipe = ', '.join([f"{k}({v})" for k, v in item['recipe'].items()])
        print(f"{idx}) {item['name']} - ${item['price']:.2f} | Recipe: {recipe}")

def generate_order():
    num_items = random.randint(1, 4)
    order = {}
    for _ in range(num_items):
        item = random.choice(menu)
        qty = random.randint(1, 3)
        order[item['name']] = order.get(item['name'], 0) + qty
    orders.append(order)
    print("New incoming order generated!")

def view_orders():
    print("\n=== Incoming Orders ===")
    if not orders:
        print("No incoming orders.")
        return
    for idx, order in enumerate(orders, 1):
        print(f"Order #{idx}:")
        for item, qty in order.items():
            print(f" - {item}: {qty}")

def prepare_item():
    view_menu()
    choice = input("Which item to prepare? (number, q to quit): ")
    if choice == 'q':
        return
    idx = int(choice) - 1
    if idx < 0 or idx >= len(menu):
        print("Invalid choice.")
        return

    qty = int(input("How many to prepare?: "))
    item = menu[idx]
    for ing, amt in item['recipe'].items():
        needed = amt * qty
        if inventory[ing]['stock'] < needed:
            print(f"Not enough {ing}. Needed: {needed}, Available: {inventory[ing]['stock']}")
            return

    for ing, amt in item['recipe'].items():
        inventory[ing]['stock'] -= amt * qty

    prepared_items[item['name']] = prepared_items.get(item['name'], 0) + qty
    print(f"Prepared {qty} {item['name']}(s).")

def fulfill_orders():
    if not orders:
        print("No incoming orders to fulfill.")
        return

    for order in orders[:]:
        can_fulfill = True
        for item, qty in order.items():
            available = prepared_items.get(item, 0)
            if available < qty:
                can_fulfill = False
                break

        if can_fulfill:
            total = 0
            for item, qty in order.items():
                for m in menu:
                    if m['name'] == item:
                        total += m['price'] * qty
                prepared_items[item] -= qty
            wallet[0] += total
            print(f"Order fulfilled! +${total:.2f}")
            orders.remove(order)
        else:
            print("Not enough prepared items to fulfill order.")

def view_inventory():
    print("\n=== Raw Inventory ===")
    for ing, data in inventory.items():
        print(f"{ing}: {data['stock']}")

def view_prepared_items():
    print("\n=== Prepared Items ===")
    if not prepared_items:
        print("None prepared yet.")
    for item, qty in prepared_items.items():
        print(f"{item}: {qty}")

def restock_inventory():
    print("\n=== Restock Inventory ===")
    print(f"Wallet: ${wallet[0]:.2f}")
    for idx, (ing, data) in enumerate(inventory.items(), 1):
        print(f"{idx}) {ing} (${data['restock_price']}/unit) Stock: {data['stock']}")
    choice = input("Which ingredient to restock? (number, q to quit): ")
    if choice == 'q':
        return
    idx = int(choice) - 1
    if idx < 0 or idx >= len(inventory):
        print("Invalid choice.")
        return
    ing = list(inventory.keys())[idx]
    qty = int(input("How many units to buy?: "))
    cost = qty * inventory[ing]['restock_price']
    if wallet[0] >= cost:
        inventory[ing]['stock'] += qty
        wallet[0] -= cost
        print(f"Bought {qty} {ing} for ${cost:.2f}. New stock: {inventory[ing]['stock']}")
    else:
        print("Not enough money.")

def view_wallet():
    print(f"Wallet balance: ${wallet[0]:.2f}")

# ============================
# Main loop
# ============================

while True:
    print("\n=== Café au Lait Staff System ===")
    print("1) View Menu")
    print("2) Generate Order")
    print("3) View Orders")
    print("4) Prepare Item")
    print("5) View Prepared Items")
    print("6) Fulfill Orders")
    print("7) View Inventory")
    print("8) Restock Inventory")
    print("9) View Wallet")
    print("0) Exit")

    choice = input("> ")
    if choice == '1':
        view_menu()
    elif choice == '2':
        generate_order()
    elif choice == '3':
        view_orders()
    elif choice == '4':
        prepare_item()
    elif choice == '5':
        view_prepared_items()
    elif choice == '6':
        fulfill_orders()
    elif choice == '7':
        view_inventory()
    elif choice == '8':
        restock_inventory()
    elif choice == '9':
        view_wallet()
    elif choice == '0':
        print("Goodbye!")
        break
    else:
        print("Invalid option.")
