"""
任務管理系統 — 資料庫初始化與連線管理

提供 get_db() 取得資料庫連線，以及 init_db() 初始化資料表。
"""

import sqlite3
import os

# 資料庫檔案路徑（放在專案根目錄的 instance/ 下）
DATABASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'instance')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'database.db')

# SQL Schema 檔案路徑
SCHEMA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'database', 'schema.sql')


def get_db():
    """
    取得 SQLite 資料庫連線。

    回傳的連線會啟用 WAL 模式與外鍵約束，
    並使用 sqlite3.Row 作為 row_factory 方便以欄位名稱存取資料。

    Returns:
        sqlite3.Connection: 資料庫連線物件。

    Raises:
        sqlite3.Error: 無法連線至資料庫時拋出。
    """
    # 確保 instance 資料夾存在
    os.makedirs(DATABASE_DIR, exist_ok=True)

    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row          # 讓查詢結果可以用欄位名稱存取
    conn.execute("PRAGMA journal_mode=WAL")  # 啟用 WAL 模式提升效能
    conn.execute("PRAGMA foreign_keys=ON")   # 啟用外鍵約束
    return conn


def init_db():
    """
    初始化資料庫：讀取 database/schema.sql 並執行建表語法。

    若資料表已存在（CREATE TABLE IF NOT EXISTS），不會重複建立。
    如果初始化失敗會印出錯誤訊息但不中斷程式。
    """
    db = None
    try:
        db = get_db()
        with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
            db.executescript(f.read())
        print("[init_db] 資料庫初始化成功。")
    except FileNotFoundError:
        print(f"[init_db] 找不到 schema 檔案：{SCHEMA_PATH}")
    except sqlite3.Error as e:
        print(f"[init_db] 資料庫初始化錯誤：{e}")
    except Exception as e:
        print(f"[init_db] 非預期錯誤：{e}")
    finally:
        if db:
            db.close()


def close_db(conn):
    """
    關閉資料庫連線。

    Args:
        conn (sqlite3.Connection | None): 要關閉的連線物件。
    """
    if conn:
        conn.close()
