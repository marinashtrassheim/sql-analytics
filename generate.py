import os
import random
import time
from datetime import datetime, timedelta
from faker import Faker
import clickhouse_connect

HOST = os.getenv('CLICKHOUSE_HOST', 'localhost')
PORT = int(os.getenv('CLICKHOUSE_PORT', 8123))
USER = os.getenv('CLICKHOUSE_USER', 'default')
PASSWORD = os.getenv('CLICKHOUSE_PASSWORD', '')
TOTAL_ROWS = int(os.getenv('ROWS_COUNT', 2_000_000))

fake = Faker()
client = clickhouse_connect.get_client(host=HOST, port=PORT, user=USER, password=PASSWORD)
print("Connected to ClickHouse")

categories = [(1, 'Electronics'), (2, 'Clothing'), (3, 'Books'), (4, 'Home')]
regions = [(1, 'North'), (2, 'South'), (3, 'East'), (4, 'West')]
products = [(i, fake.word()) for i in range(1, 501)]

def generate_row(date):
    product_id, product_name = random.choice(products)
    category_id, category_name = random.choice(categories)
    region_id, region_name = random.choice(regions)
    quantity = random.randint(1, 5)
    price = round(random.uniform(5, 500), 2)
    discount = round(random.uniform(0, 0.3), 2)
    total = quantity * price * (1 - discount)
    sale_datetime = datetime.combine(date, datetime.min.time()) + timedelta(seconds=random.randint(0, 86400))
    return (
        random.randint(1, 10**9),   # sale_id
        date,                       # sale_date
        sale_datetime,              # sale_datetime
        product_id,
        product_name,
        category_id,
        category_name,
        region_id,
        region_name,
        random.randint(1, 100000),  # customer_id
        random.randint(18, 70),     # customer_age
        random.choice(['M', 'F']),  # customer_gender
        quantity,
        price,
        discount,
        round(total, 2)             # total
    )

start_date = datetime.now().date() - timedelta(days=3*365)
rows_batch = []
batch_size = 100000

print(f"Generating {TOTAL_ROWS} rows...")
for i in range(TOTAL_ROWS):
    days_offset = random.randint(0, 3*365)
    date = start_date + timedelta(days=days_offset)
    rows_batch.append(generate_row(date))
    if len(rows_batch) >= batch_size:
        client.insert('sales', rows_batch, column_names=[
            'sale_id', 'sale_date', 'sale_datetime', 'product_id', 'product_name',
            'category_id', 'category_name', 'region_id', 'region_name',
            'customer_id', 'customer_age', 'customer_gender',
            'quantity', 'price', 'discount', 'total'
        ])
        print(f"Inserted {len(rows_batch)} rows")
        rows_batch = []

if rows_batch:
    client.insert('sales', rows_batch, column_names=[...])
    print(f"Inserted final {len(rows_batch)} rows")

print("Data generation completed.")