import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

DB_URL = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME", "olist_db"),
)

# Order important hai: parent tables pehle, child baad mein
TABLES = {
    "customers":   {"file": "olist_customers_dataset.csv",   "key": ["customer_id"]},
    "products":    {"file": "olist_products_dataset.csv",    "key": ["product_id"]},
    "orders":      {"file": "olist_orders_dataset.csv",      "key": ["order_id"]},
    "order_items": {"file": "olist_order_items_dataset.csv", "key": ["order_id", "order_item_id"]},
}
