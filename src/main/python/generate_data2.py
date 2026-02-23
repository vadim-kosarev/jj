# CREATE TABLE products (product_id Int32, product_name String, brand_id Int32, seller_id Int32, updated Date) ENGINE = ReplacingMergeTree ORDER BY product_id
# CREATE TABLE remainders (date Date, product_id Int32, remainder Int32, price Int32, discount Int32, pics Int32, rating Int32, reviews Int32, new Bool) ENGINE = ReplacingMergeTree ORDER BY (date, product_id)

import argparse
import random
from datetime import datetime, timedelta
import clickhouse_connect
import time

def generate_products(start_id, num_products, period_days):
    products = []
    today = datetime.now().date()
    start_date = today - timedelta(days=period_days)

    product_names = [
        "iPhone 15 Pro", "Samsung Galaxy S24", "MacBook Air M3", "Dell XPS 13", "Sony WH-1000XM5",
        "Nike Air Max", "Adidas Ultraboost", "Levi's 501 Jeans", "H&M Cotton T-Shirt", "Zara Dress",
        "Coca-Cola 2L", "Pepsi Max", "Red Bull Energy Drink", "Starbucks Coffee Beans", "Nescafe Instant",
        "Toyota Camry", "Honda Civic", "BMW X5", "Mercedes C-Class", "Audi A4",
        "IKEA Billy Bookcase", "Wayfair Sofa", "Amazon Echo Dot", "Google Nest Hub", "Apple Watch Series 9",
        "Canon EOS R5", "Nikon Z6 II", "GoPro HERO9", "DJI Mavic Air 2", "Bose QuietComfort 35",
        "Rolex Submariner", "Omega Seamaster", "Tag Heuer Carrera", "Casio G-Shock", "Seiko Presage",
        "PlayStation 5", "Xbox Series X", "Nintendo Switch OLED", "Steam Deck", "Oculus Quest 2",
        "Tesla Model 3", "Ford Mustang", "Chevrolet Camaro", "Porsche 911", "Lamborghini Huracan",
        "Gucci Handbag", "Louis Vuitton Wallet", "Prada Sunglasses", "Chanel Perfume", "Dior Lipstick",
        "Samsung 4K TV", "LG OLED TV", "Sony Bravia", "Vizio Smart TV", "TCL Roku TV",
        "KitchenAid Mixer", "Instant Pot", "Breville Coffee Maker", "Cuisinart Blender", "Vitamix Juicer",
        "Peloton Bike", "Treadmill NordicTrack", "Bowflex Dumbbells", "Yoga Mat Manduka", "Foam Roller TriggerPoint",
        "Harry Potter Book Set", "The Lord of the Rings", "Game of Thrones", "The Hunger Games", "Dune",
        "Lego Star Wars", "Barbie Dreamhouse", "Hot Wheels Track", "Nerf Blaster", "Puzzle 1000 Pieces",
        "Patagonia Jacket", "The North Face Backpack", "Columbia Hiking Boots", "REI Tent", "Marmot Sleeping Bag",
        "Whole Foods Organic Apples", "Ben & Jerry's Ice Cream", "Kraft Mac and Cheese", "Campbell's Soup", "Oreo Cookies",
        "Johnson's Baby Shampoo", "Pampers Diapers", "Tylenol Pain Reliever", "Band-Aid Adhesive", "Neosporin Ointment",
        "Microsoft Office 365", "Adobe Photoshop", "Autodesk AutoCAD", "Zoom Video Conferencing", "Slack Team Communication",
        "Airbnb Accommodation", "Uber Ride", "Spotify Premium", "Netflix Subscription", "Amazon Prime",
        "Bitcoin Wallet", "Ethereum Mining Rig", "Cryptocurrency Exchange", "NFT Digital Art", "Blockchain Ledger",
        "Solar Panel Kit", "Wind Turbine", "Electric Car Charger", "LED Light Bulbs", "Smart Thermostat",
        "Drone Delivery Service", "Autonomous Vehicle", "AI Personal Assistant", "Quantum Computer", "5G Router"
    ]

    for i in range(num_products):
        product_id = start_id + i
        product_name = random.choice(product_names) + f" {random.uniform(1, 100):.16f}"  # Add variation
        brand_id = random.randint(1, 2147483647)
        seller_id = random.randint(1, 2147483647)
        updated = start_date + timedelta(days=random.randint(0, period_days))
        products.append((product_id, product_name, brand_id, seller_id, updated))

    return products

def generate_remainders(products, remainders_per_product, period_days):
    remainders = []
    today = datetime.now().date()
    start_date = today - timedelta(days=period_days)

    for product in products:
        product_id = product[0]
        if product_id % 100 == 0:
            print(f"Generated remainders for {product_id} products")
        for _ in range(remainders_per_product):
            date = start_date + timedelta(days=random.randint(0, period_days))
            remainder = random.randint(0, 2147483647)
            price = random.randint(100, 2147483647)
            discount = random.randint(0, 2147483647)
            pics = random.randint(0, 2147483647)
            rating = random.randint(1, 2147483647)
            reviews = random.randint(0, 2147483647)
            new = random.choice([True, False])
            remainders.append((date, product_id, remainder, price, discount, pics, rating, reviews, int(new)))

    return remainders

def main():
    parser = argparse.ArgumentParser(description='Generate sample data for products and remainders tables or execute SQL queries')
    parser.add_argument('--period_days', type=int, help='Maximum age of data in days')
    parser.add_argument('--num_products', type=int, help='Number of products to generate')
    parser.add_argument('--remainders_per_product', type=int, help='Number of remainders per product')
    parser.add_argument('--clickhouse_url', type=str, help='ClickHouse DSN URL (required for insertion or queries)')
    parser.add_argument('--sql', type=str, help='SQL query to execute')
    parser.add_argument('--start_id', type=int, default=1, help='Starting product ID (default: 1)')

    args = parser.parse_args()

    if args.sql:
        if not args.clickhouse_url:
            parser.error("--clickhouse_url is required for --sql")
        client = clickhouse_connect.get_client(dsn=args.clickhouse_url)
        query_start = time.time()
        result = client.query(args.sql)
        query_time = time.time() - query_start
        print(f"Total rows: {len(result.result_rows)}")
        print(f"Query executed in {query_time:.2f} seconds")
    else:
        if not args.period_days or not args.num_products or not args.remainders_per_product:
            parser.error("--period_days, --num_products, --remainders_per_product are required for data generation")

        start_time = time.time()
        if args.clickhouse_url:
            # Connect to ClickHouse and generate/insert data in batches
            client = clickhouse_connect.get_client(dsn=args.clickhouse_url)
            # Get the next product_id from DB
            result = client.query("SELECT max(product_id) FROM products")
            max_id = result.result_rows[0][0] if result.result_rows and result.result_rows[0][0] is not None else 0
            start_product_id = max_id + 1
            insert_start = time.time()
            total_records = 0
            for batch_start in range(0, args.num_products, 100):
                batch_size = min(100, args.num_products - batch_start)
                products_batch = generate_products(start_product_id, batch_size, args.period_days)
                remainders_batch = generate_remainders(products_batch, args.remainders_per_product, args.period_days)
                client.insert('products', products_batch, column_names=['product_id', 'product_name', 'brand_id', 'seller_id', 'updated'])
                client.insert('remainders', remainders_batch, column_names=['date', 'product_id', 'remainder', 'price', 'discount', 'pics', 'rating', 'reviews', 'new'])
                total_records += len(products_batch) + len(remainders_batch)
                print(f"Inserted batch: {len(products_batch)} products, {len(remainders_batch)} remainders")
                start_product_id += batch_size
            gen_time = time.time()
            print(f"Data generation and insertion completed in {gen_time - start_time:.2f} seconds, {total_records / (gen_time - insert_start):.2f} records/second")
            print("Data inserted into ClickHouse successfully.")
        else:
            # Generate all data first, then output INSERT statements
            products = generate_products(args.start_id, args.num_products, args.period_days)
            remainders = generate_remainders(products, args.remainders_per_product, args.period_days)
            gen_time = time.time()
            print(f"Data generation completed in {gen_time - start_time:.2f} seconds")

            output_start = time.time()
            print("INSERT INTO products (product_id, product_name, brand_id, seller_id, updated) VALUES")
            for i, product in enumerate(products):
                end = ";" if i == len(products) - 1 else ","
                print(f"({product[0]}, '{product[1]}', {product[2]}, {product[3]}, '{product[4]}'){end}")

            print("\nINSERT INTO remainders (date, product_id, remainder, price, discount, pics, rating, reviews, new) VALUES")
            for i, remainder in enumerate(remainders):
                end = ";" if i == len(remainders) - 1 else ","
                print(f"('{remainder[0]}', {remainder[1]}, {remainder[2]}, {remainder[3]}, {remainder[4]}, {remainder[5]}, {remainder[6]}, {remainder[7]}, {remainder[8]}){end}")
            output_time = time.time() - output_start
            print(f"SQL output completed in {output_time:.2f} seconds")

if __name__ == "__main__":
    main()
