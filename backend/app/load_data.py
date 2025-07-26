import csv
from datetime import datetime
from app.database import SessionLocal, engine
from app.models import (
    DistributionCenter, Product, InventoryItem,
    User, Order, OrderItem
)

# create tables
from app.models import Base
Base.metadata.create_all(bind=engine)

# helper to parse datetime

def parse_dt(val):
    try:
        return datetime.fromisoformat(val) if val else None
    except ValueError:
        return None

# track existing emails to skip duplicates
existing_emails = set()

def load_csv(model, csv_path, transform_row=None):
    session = SessionLocal()
    with open(csv_path, newline='', encoding='utf-8', errors='ignore') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if transform_row:
                row = transform_row(row)
            # filter only valid model fields
            filtered = {k: v for k, v in row.items() if k in model.__table__.columns.keys()}
            # skip duplicate emails for User
            if model is User:
                email = filtered.get('email')
                if not email or email in existing_emails:
                    continue
                existing_emails.add(email)
            obj = model(**filtered)
            session.add(obj)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error loading {model.__tablename__}: {e}")
    session.close()

if __name__ == '__main__':
    data_dir = './data'
    # distribution_centers
    load_csv(
        DistributionCenter,
        f"{data_dir}/distribution_centers.csv",
        lambda r: {
            **r,
            'latitude': float(r.get('latitude', 0)),
            'longitude': float(r.get('longitude', 0))
        }
    )
    # products
    load_csv(
        Product,
        f"{data_dir}/products.csv",
        lambda r: {
            **r,
            'cost': float(r.get('cost', 0)),
            'retail_price': float(r.get('retail_price', 0)),
            'distribution_center_id': int(r.get('distribution_center_id', 0))
        }
    )
    # inventory_items
    load_csv(
        InventoryItem,
        f"{data_dir}/inventory_items.csv",
        lambda r: {
            **r,
            'product_id': int(r.get('product_id', 0)),
            'created_at': parse_dt(r.get('created_at')),
            'sold_at': parse_dt(r.get('sold_at')),
            'cost': float(r.get('cost', 0)),
            'product_retail_price': float(r.get('product_retail_price', 0)),
            'product_distribution_center_id': int(r.get('product_distribution_center_id', 0))
        }
    )
    # users (skip duplicates)
    load_csv(
        User,
        f"{data_dir}/users.csv",
        lambda r: {
            **r,
            'age': int(r.get('age', 0)),
            'latitude': float(r.get('latitude', 0)),
            'longitude': float(r.get('longitude', 0)),
            'created_at': parse_dt(r.get('created_at'))
        }
    )
    # orders
    load_csv(
        Order,
        f"{data_dir}/orders.csv",
        lambda r: {
            'order_id': int(r.get('order_id', 0)),
            'user_id': int(r.get('user_id', 0)),
            'status': r.get('status'),
            'gender': r.get('gender'),
            'created_at': parse_dt(r.get('created_at')),
            'returned_at': parse_dt(r.get('returned_at')),
            'shipped_at': parse_dt(r.get('shipped_at')),
            'delivered_at': parse_dt(r.get('delivered_at')),
            'num_of_item': int(r.get('num_of_item', 0))
        }
    )
    # order_items
    load_csv(
        OrderItem,
        f"{data_dir}/order_items.csv",
        lambda r: {
            'order_id': int(r.get('order_id', 0)),
            'user_id': int(r.get('user_id', 0)),
            'product_id': int(r.get('product_id', 0)),
            'inventory_item_id': int(r.get('inventory_item_id', 0)),
            'status': r.get('status'),
            'created_at': parse_dt(r.get('created_at')),
            'shipped_at': parse_dt(r.get('shipped_at')),
            'delivered_at': parse_dt(r.get('delivered_at')),
            'returned_at': parse_dt(r.get('returned_at'))
        }
    )
    print("Data loaded into SQLite database with duplicates skipped.")