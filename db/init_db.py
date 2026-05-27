"""
DB 초기화 스크립트 — python -m db.init_db
SQLite는 파일만 있으면 되므로 CREATE DATABASE 불필요.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.db import init_schema, DB_PATH

if __name__ == "__main__":
    print(f"[DB] SQLite path: {DB_PATH.resolve()}")
    init_schema()
    print("[DB] Done.")
