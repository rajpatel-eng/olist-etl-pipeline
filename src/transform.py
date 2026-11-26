import pandas as pd
from logger import get_logger

log = get_logger("transform")

def _strip(df):
    # text ke aage-peeche ke extra spaces hatao
    for c in df.columns:
        df[c] = df[c].str.strip()
    return df

def transform_customers(df):
    df = df[["customer_id", "customer_unique_id", "customer_zip_code_prefix",
             "customer_city", "customer_state"]].copy()
    df = _strip(df)
    df["customer_city"] = df["customer_city"].str.lower()
    df["customer_state"] = df["customer_state"].str.upper()
    return df.dropna(subset=["customer_id"]).drop_duplicates(subset=["customer_id"])

def transform_products(df):
    df = df[["product_id", "product_category_name",
             "product_weight_g", "product_photos_qty"]].copy()
    df = _strip(df)
    df["product_category_name"] = df["product_category_name"].fillna("unknown")
    df["product_weight_g"] = pd.to_numeric(df["product_weight_g"], errors="coerce")
    df["product_photos_qty"] = pd.to_numeric(df["product_photos_qty"], errors="coerce")
    return df.dropna(subset=["product_id"]).drop_duplicates(subset=["product_id"])

def transform_orders(df):
    date_cols = ["order_purchase_timestamp", "order_approved_at",
                 "order_delivered_carrier_date", "order_delivered_customer_date",
                 "order_estimated_delivery_date"]
    df = df[["order_id", "customer_id", "order_status"] + date_cols].copy()
    df = _strip(df)
    for c in date_cols:
        df[c] = pd.to_datetime(df[c], errors="coerce")
    return df.dropna(subset=["order_id"]).drop_duplicates(subset=["order_id"])

def transform_order_items(df):
    df = df[["order_id", "order_item_id", "product_id", "seller_id",
             "shipping_limit_date", "price", "freight_value"]].copy()
    df = _strip(df)
    df["order_item_id"] = pd.to_numeric(df["order_item_id"], errors="coerce")
    df = df.dropna(subset=["order_id", "order_item_id"])
    df["order_item_id"] = df["order_item_id"].astype(int)
    df["shipping_limit_date"] = pd.to_datetime(df["shipping_limit_date"], errors="coerce")
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["freight_value"] = pd.to_numeric(df["freight_value"], errors="coerce")
    return df.drop_duplicates(subset=["order_id", "order_item_id"])

TRANSFORMS = {
    "customers": transform_customers,
    "products": transform_products,
    "orders": transform_orders,
    "order_items": transform_order_items,
}

if __name__ == "__main__":
    from config import TABLES
    from extract import extract
    for name, cfg in TABLES.items():
        raw = extract(cfg["file"])
        clean = TRANSFORMS[name](raw)
        log.info(f"{name}: {len(raw)} -> {len(clean)} rows, nulls={int(clean.isnull().sum().sum())}")
