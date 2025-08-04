import sqlite3
import pandas as pd

# Connect to SQLite DB
conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# Run schema.sql
with open('schema.sql', 'r') as f:
    schema = f.read()
    cursor.executescript(schema)
    conn.commit()

# Load CSVs
csv_path = 'archive/'

distribution_centers = pd.read_csv(csv_path + 'distribution_centers.csv')
users = pd.read_csv(csv_path + 'users.csv')
products = pd.read_csv(csv_path + 'products.csv')
inventory_items = pd.read_csv(csv_path + 'inventory_items.csv')
orders = pd.read_csv(csv_path + 'orders.csv')
order_items = pd.read_csv(csv_path + 'order_items.csv')

# Load to DB
distribution_centers.to_sql('distribution_centers', conn, if_exists='replace', index=False)
users.to_sql('users', conn, if_exists='replace', index=False)
products.to_sql('products', conn, if_exists='replace', index=False)
inventory_items.to_sql('inventory_items', conn, if_exists='replace', index=False)
orders.to_sql('orders', conn, if_exists='replace', index=False)
order_items.to_sql('order_items', conn, if_exists='replace', index=False)

# Quick Verification
print("Users sample:")
print(pd.read_sql("SELECT id, first_name, email FROM users LIMIT 5", conn))

print("\nOrders sample:")
print(pd.read_sql("SELECT order_id, user_id, status FROM orders LIMIT 5", conn))

conn.close()
