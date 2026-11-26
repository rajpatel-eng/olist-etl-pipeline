import sys
import time
from sqlalchemy import create_engine
from config import DB_URL, TABLES
from logger import get_logger
from schema import create_tables
from extract import extract
from transform import TRANSFORMS
from quality import run_checks
from load import upsert

log = get_logger("main")

def run():
    start = time.time()
    engine = create_engine(DB_URL)
    create_tables(engine)

    failed = []
    total_new = 0
    for name, cfg in TABLES.items():
        t0 = time.time()
        try:
            raw = extract(cfg["file"])
            clean = TRANSFORMS[name](raw)
            run_checks(name, clean, cfg["key"])
            total_new += upsert(clean, name, engine)
            log.info(f"{name} done in {time.time() - t0:.1f}s")
        except Exception:
            log.exception(f"{name} FAILED")
            failed.append(name)

    log.info(f"Pipeline khatam: {total_new} naye rows, {time.time() - start:.1f}s, failed={failed}")
    if failed:
        sys.exit(1)

if __name__ == "__main__":
    run()
