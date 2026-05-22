import os
import psycopg2
from faker import Faker
import random

fake = Faker()

used_phones = set()

def generate_phone():
    while True:
        phone = "+44" + str(random.randint(7000000000, 7999999999))
        if phone not in used_phones:
            used_phones.add(phone)
            return phone

# DATABASE CONNECTION (AZURE)
conn = psycopg2.connect(
    host=os.getenv("host"),
    database=os.getenv("database"),
    user=os.getenv("user"),
    password=os.getenv("password"),
    port=os.getenv("port"),
)

cur = conn.cursor()

# CONFIG
NUM_STORES = 8
NUM_CUSTOMERS = 1500
NUM_INGREDIENTS = 45
NUM_MENU_ITEMS = 25
NUM_ORDERS = 7000

# INSERT STORES
store_ids = []
for _ in range(NUM_STORES):
    cur.execute("""
        INSERT INTO Stores (address, city, phone_number)
        VALUES (%s, %s, %s)
        RETURNING store_id;
    """, (
        fake.street_address(),
        fake.city(),
        fake.unique.msisdn()[:20]
    ))
    store_ids.append(cur.fetchone()[0])

# INSERT CUSTOMERS
customer_ids = []

for _ in range(NUM_CUSTOMERS):

    # ✅ DEFINE VARIABLES FIRST
    first_name = fake.first_name()
    last_name = fake.last_name()

    email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1000,999999)}@example.com"
    phone = generate_phone()

    # ✅ THEN PASS VALUES (NO '=' HERE)
    cur.execute("""
        INSERT INTO Customers (first_name, last_name, email, phone_number)
        VALUES (%s, %s, %s, %s)
        RETURNING customer_id;
    """, (
        first_name,
        last_name,
        email,
        phone
    ))

    customer_ids.append(cur.fetchone()[0])

# INSERT INGREDIENTS
ingredient_ids = []
for _ in range(NUM_INGREDIENTS):
    cur.execute("""
        INSERT INTO Ingredients (name, stock_quantity, unit)
        VALUES (%s, %s, %s)
        RETURNING ingredient_id;
    """, (
        fake.unique.word(),
        round(random.uniform(10, 500), 2),
        random.choice(["kg", "liters", "units"])
    ))
    ingredient_ids.append(cur.fetchone()[0])

# INSERT MENU ITEMS
menu_item_ids = []
for _ in range(NUM_MENU_ITEMS):
    cur.execute("""
        INSERT INTO Menu_Items (name, category, size)
        VALUES (%s, %s, %s)
        RETURNING item_id;
    """, (
        fake.word().capitalize() + " Pizza",
        random.choice(["Pizza", "Drink", "Side"]),
        random.choice(["Small", "Medium", "Large"])
    ))
    menu_item_ids.append(cur.fetchone()[0])

# INSERT ORDERS
order_ids = []
for _ in range(NUM_ORDERS):
    total_amount = round(random.uniform(10, 80), 2)

    cur.execute("""
        INSERT INTO Orders (customer_id, store_id, total_amount)
        VALUES (%s, %s, %s)
        RETURNING order_id;
    """, (
        random.choice(customer_ids),
        random.choice(store_ids),
        total_amount
    ))
    order_ids.append(cur.fetchone()[0])

# INSERT ORDER ITEMS
for order_id in order_ids:
    num_items = random.randint(2, 4)

    for _ in range(num_items):
        quantity = random.randint(1, 3)
        price = round(random.uniform(5, 25), 2)

        cur.execute("""
            INSERT INTO Order_Items (order_id, item_id, quantity, price)
            VALUES (%s, %s, %s, %s);
        """, (
            order_id,
            random.choice(menu_item_ids),
            quantity,
            price
        ))

# COMMIT & CLOSE
conn.commit()
cur.close()
conn.close()

print("✅ Data successfully populated into Azure PostgreSQL!")