# backend/app/load_data.py

import os
import pandas as pd
from datetime import datetime
from .database import SessionLocal, Base, engine
from .models import (
    DistributionCenter, Product,
    InventoryItem, Order, OrderItem, User
)

# 1) Create tables if not exist
Base.metadata.create_all(bind=engine)
session = SessionLocal()

def parse_dt(x):
    if pd.isna(x) or x == "":
        return None
    try:
        return datetime.fromisoformat(x)
    except:
        return None

# track seen emails
existing_emails = set()

# 2) Configuration: model, CSV, converters, required, dedupe
mappings = [
    (
        DistributionCenter, 'distribution_centers.csv',
        {'id':int, 'name':str, 'latitude':float, 'longitude':float},
        ['id','name'], False
    ),
    (
        Product, 'products.csv',
        {'id':int,'cost':float,'category':str,'name':str,'brand':str,
         'retail_price':float,'department':str,'sku':str,
         'distribution_center_id':int},
        ['id','name'], False
    ),
    (
        InventoryItem, 'inventory_items.csv',
        {'id':int,'product_id':int,'created_at':parse_dt,'sold_at':parse_dt,
         'cost':float,'product_category':str,'product_name':str,
         'product_brand':str,'product_retail_price':float,
         'product_department':str,'product_sku':str,
         'product_distribution_center_id':int},
        ['id','product_id'], False
    ),
    (
        Order, 'orders.csv',
        {'order_id':int,'user_id':int,'status':str,'gender':str,
         'created_at':parse_dt,'returned_at':parse_dt,
         'shipped_at':parse_dt,'delivered_at':parse_dt,
         'num_of_item':int},
        ['order_id','user_id'], False
    ),
    (
        OrderItem, 'order_items.csv',
        {'id':int,'order_id':int,'user_id':int,'product_id':int,
         'inventory_item_id':int,'status':str,'created_at':parse_dt,
         'shipped_at':parse_dt,'delivered_at':parse_dt,'returned_at':parse_dt},
        ['id','order_id'], False
    ),
    (
        User, 'users.csv',
        {'id':int,'first_name':str,'last_name':str,'email':str,'age':int,
         'gender':str,'state':str,'street_address':str,'postal_code':str,
         'city':str,'country':str,'latitude':float,'longitude':float,
         'traffic_source':str,'created_at':parse_dt},
        ['id','email'], True       # <— dedupe on email for User
    ),
]

# 3) Process each CSV
for Model, fname, conv, required, dedupe in mappings:
    df = pd.read_csv(os.path.join('data', fname))
    loaded = skipped = duped = 0

    for _, row in df.iterrows():
        # build kwargs
        kwargs = {}
        for col, fn in conv.items():
            val = row.get(col, None)
            if pd.isna(val):
                val = None
            kwargs[col] = fn(val) if val is not None else None

        # skip if any required missing/blank
        if any(kwargs.get(r) in (None, "", 0) for r in required):
            skipped += 1
            continue

        # additional dedupe for users by email
        if dedupe:
            email = kwargs.get('email')
            if email in existing_emails:
                duped += 1
                continue
            existing_emails.add(email)

        # upsert
        session.merge(Model(**kwargs))
        loaded += 1

    session.commit()
    print(f"{fname}: loaded {loaded}, skipped {skipped}" + (f", duped {duped}" if dedupe else ""))

session.close()
print("✅ Data load complete.")
