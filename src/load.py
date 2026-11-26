from sqlalchemy import text
from logger import get_logger

log = get_logger("load")

def upsert(df, table, engine):
    stg = f"stg_{table}"
    # 1. Data pehle staging table mein
    df.to_sql(stg, engine, if_exists="replace", index=False, chunksize=5000)
    cols = ", ".join(f"`{c}`" for c in df.columns)
    try:
        # 2. Staging se asli table mein, sirf naye rows (ek transaction mein)
        with engine.begin() as conn:
            res = conn.execute(text(
                f"INSERT IGNORE INTO `{table}` ({cols}) SELECT {cols} FROM `{stg}`"
            ))
            inserted = res.rowcount
    finally:
        # 3. Staging table hamesha delete
        with engine.begin() as conn:
            conn.execute(text(f"DROP TABLE IF EXISTS `{stg}`"))
    log.info(f"{table}: {inserted} naye rows insert hue, {len(df) - inserted} already the")
    return inserted

if __name__ == "__main__":
    # Test: sirf customers load karke dekho
    from sqlalchemy import create_engine
    from config import DB_URL, TABLES
    from extract import extract
    from transform import TRANSFORMS
    from quality import run_checks

    engine = create_engine(DB_URL)
    cfg = TABLES["customers"]
    clean = TRANSFORMS["customers"](extract(cfg["file"]))
    run_checks("customers", clean, cfg["key"])
    upsert(clean, "customers", engine)
