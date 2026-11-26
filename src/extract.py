import pandas as pd
from config import RAW_DIR
from logger import get_logger

log = get_logger("extract")

def extract(file_name):
    path = RAW_DIR / file_name
    if not path.exists():
        raise FileNotFoundError(f"File nahi mili: {path}")
    # dtype=str: IDs aur zip code ke leading zeros kharab na hon
    df = pd.read_csv(path, dtype=str)
    log.info(f"{file_name}: {len(df)} rows, {len(df.columns)} columns padhe")
    return df

if __name__ == "__main__":
    from config import TABLES
    for name, cfg in TABLES.items():
        extract(cfg["file"])
