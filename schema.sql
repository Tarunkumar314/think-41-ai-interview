-- schema.sql

CREATE TABLE IF NOT EXISTS distribution_centers (
  id INTEGER PRIMARY KEY,
  name TEXT,
  latitude REAL,
  longitude REAL
);

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY,
  first_name TEXT,
  last_name TEXT,
  email TEXT UNIQUE,
  age INTEGER,
  gender TEXT,
  state TEXT,
  street_address TEXT,
  postal_code TEXT,
  city TEXT,
  country TEXT,
  latitude REAL,
  longitude REAL,
  traffic_source TEXT,
  created_at TEXT
);

CREATE TABLE IF NOT EXISTS products (
  id INTEGER PRIMARY KEY,
  cost REAL,
  category TEXT,
  name TEXT,
  brand TEXT,
  retail_price REAL,
  department TEXT,
  sku TEXT,
  distribution_center_id INTEGER,
  FOREIGN KEY (distribution_center_id) REFERENCES distribution_centers(id)
);

CREATE TABLE IF NOT EXISTS inventory_items (
  id INTEGER PRIMARY KEY,
  product_id INTEGER,
  created_at TEXT,
  sold_at TEXT,
  cost REAL,
  product_category TEXT,
  product_name TEXT,
  product_brand TEXT,
  product_retail_price REAL,
  product_department TEXT,
  product_sku TEXT,
  product_distribution_center_id INTEGER,
  FOREIGN KEY (product_id) REFERENCES products(id),
  FOREIGN KEY (product_distribution_center_id) REFERENCES distribution_centers(id)
);

CREATE TABLE IF NOT EXISTS orders (
  order_id INTEGER PRIMARY KEY,
  user_id INTEGER,
  status TEXT,
  gender TEXT,
  created_at TEXT,
  returned_at TEXT,
  shipped_at TEXT,
  delivered_at TEXT,
  num_of_item INTEGER,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS order_items (
  id INTEGER PRIMARY KEY,
  order_id INTEGER,
  user_id INTEGER,
  product_id INTEGER,
  inventory_item_id INTEGER,
  status TEXT,
  created_at TEXT,
  shipped_at TEXT,
  delivered_at TEXT,
  returned_at TEXT,
  sale_price REAL,
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (product_id) REFERENCES products(id),
  FOREIGN KEY (inventory_item_id) REFERENCES inventory_items(id)
);

