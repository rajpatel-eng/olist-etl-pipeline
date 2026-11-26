from sqlalchemy import create_engine, text
from config import DB_URL
from logger import get_logger

log = get_logger("schema")

DDL = [
    """
    CREATE TABLE IF NOT EXISTS customers (
        customer_id VARCHAR(32) PRIMARY KEY,
        customer_unique_id VARCHAR(32),
        customer_zip_code_prefix VARCHAR(10),
        customer_city VARCHAR(100),
        customer_state CHAR(2)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS products (
        product_id VARCHAR(32) PRIMARY KEY,
        product_category_name VARCHAR(100),
        product_weight_g DOUBLE,
        product_photos_qty DOUBLE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS orders (
        order_id VARCHAR(32) PRIMARY KEY,
        customer_id VARCHAR(32),
        order_status VARCHAR(20),
        order_purchase_timestamp DATETIME,
        order_approved_at DATETIME NULL,
        order_delivered_carrier_date DATETIME NULL,
        order_delivered_customer_date DATETIME NULL,
        order_estimated_delivery_date DATETIME NULL,
        INDEX idx_customer (customer_id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS order_items (
        order_id VARCHAR(32),
        order_item_id INT,
        product_id VARCHAR(32),
        seller_id VARCHAR(32),
        shipping_limit_date DATETIME NULL,
        price DECIMAL(10,2),
        freight_value DECIMAL(10,2),
        PRIMARY KEY (order_id, order_item_id),
        INDEX idx_product (product_id)
    )
    """,
]

def create_tables(engine):
    with engine.begin() as conn:
        for stmt in DDL:
            conn.execute(text(stmt))
    log.info("Tables ready")

if __name__ == "__main__":
    create_tables(create_engine(DB_URL))
