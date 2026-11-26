from logger import get_logger

log = get_logger("quality")

class DataQualityError(Exception):
    pass

def run_checks(name, df, key_cols):
    # 1. Data khali na ho
    if df.empty:
        raise DataQualityError(f"{name}: data khali hai")

    # 2. Key columns mein null na ho
    nulls = int(df[key_cols].isnull().sum().sum())
    if nulls > 0:
        raise DataQualityError(f"{name}: key columns mein {nulls} null")

    # 3. Key duplicate na ho
    dups = int(df.duplicated(subset=key_cols).sum())
    if dups > 0:
        raise DataQualityError(f"{name}: {dups} duplicate keys")

    # 4. Table-specific check
    if name == "order_items":
        bad = int((df["price"] < 0).sum() + (df["freight_value"] < 0).sum())
        if bad > 0:
            raise DataQualityError(f"{name}: {bad} negative price/freight")

    # 5. Zyada nulls wale columns sirf warning dete hain
    null_pct = (df.isnull().mean() * 100).round(1)
    heavy = null_pct[null_pct > 30]
    if not heavy.empty:
        log.warning(f"{name}: zyada nulls wale columns: {heavy.to_dict()}")

    log.info(f"{name}: quality checks pass ({len(df)} rows)")

if __name__ == "__main__":
    from config import TABLES
    from extract import extract
    from transform import TRANSFORMS
    for name, cfg in TABLES.items():
        clean = TRANSFORMS[name](extract(cfg["file"]))
        run_checks(name, clean, cfg["key"])
