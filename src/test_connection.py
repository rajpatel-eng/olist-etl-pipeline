from sqlalchemy import create_engine, text
from config import DB_URL
from logger import get_logger

log = get_logger("test")

engine = create_engine(DB_URL)
with engine.connect() as conn:
    version = conn.execute(text("SELECT version()")).scalar()
    db = conn.execute(text("SELECT DATABASE()")).scalar()
    log.info(f"Connected! MySQL {version}, database: {db}")
