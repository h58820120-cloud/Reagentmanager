# migrate_db.py
# 資料庫升級腳本 - 新增缺少的欄位（不刪除現有資料）

import sqlite3
import os
import sys


# migrate_db.py
# 資料庫升級腳本 - 新增缺少的欄位（不刪除現有資料）

import sqlite3
import os
import sys


def get_db_path():
    """讓使用者選擇資料庫檔案"""
    # 先嘗試用 tkinter 開啟檔案選擇對話框
    try:
        import tkinter as tk
        from tkinter import filedialog, messagebox

        root = tk.Tk()
        root.withdraw()  # 隱藏主視窗

        messagebox.showinfo(
            "資料庫升級",
            "請選擇 reagent_system.db 檔案位置"
        )

        path = filedialog.askopenfilename(
            title="選擇 reagent_system.db",
            filetypes=[("SQLite 資料庫", "*.db"), ("所有檔案", "*.*")],
            initialdir=os.path.expanduser("~")
        )
        root.destroy()

        if not path:
            print("未選擇檔案，取消升級")
            return None
        return path

    except Exception:
        # tkinter 不可用時，改用 CMD 輸入路徑
        print("請輸入 reagent_system.db 的完整路徑")
        print("例如: D:\\aaa\\reagent_system.db")
        print()
        path = input("路徑: ").strip().strip('"')
        return path if path else None


def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cursor.fetchall())


def table_exists(cursor, table):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
    return cursor.fetchone() is not None


def migrate():
    db_path = get_db_path()
    if not os.path.exists(db_path):
        print(f"找不到資料庫: {db_path}")
        print("請先執行 python main.py 建立資料庫")
        return False

    print(f"資料庫位置: {db_path}")
    print("開始升級資料庫...")

    conn = sqlite3.connect(db_path)
    c    = conn.cursor()

    migrations = []

    # reagent_master 新增欄位
    reagent_cols = [
        ("lot_start",   "INTEGER DEFAULT 0"),
        ("lot_length",  "INTEGER DEFAULT 10"),
        ("exp_start",   "INTEGER DEFAULT 10"),
        ("exp_length",  "INTEGER DEFAULT 6"),
        ("exp_format",  "TEXT DEFAULT 'YYYYMMDD'"),
        ("need_qc",     "INTEGER DEFAULT 0"),
        ("qc_levels",   "INTEGER DEFAULT 1"),
        ("keeper_id",   "INTEGER REFERENCES users(id)"),
    ]

    for col, col_type in reagent_cols:
        if not column_exists(c, 'reagent_master', col):
            c.execute(f"ALTER TABLE reagent_master ADD COLUMN {col} {col_type}")
            migrations.append(f"reagent_master.{col}")

    # 建立 qc_batch 表格
    if not table_exists(c, 'qc_batch'):
        c.execute("""
            CREATE TABLE qc_batch (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                reagent_id    INTEGER NOT NULL REFERENCES reagent_master(id),
                lot_number    TEXT NOT NULL,
                stock_in_date TEXT NOT NULL,
                qc_levels     INTEGER DEFAULT 1,
                is_complete   INTEGER DEFAULT 0,
                created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        migrations.append("建立 qc_batch 表格")

    # 建立 qc_result 表格
    if not table_exists(c, 'qc_result'):
        c.execute("""
            CREATE TABLE qc_result (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id     INTEGER NOT NULL REFERENCES qc_batch(id),
                level        INTEGER NOT NULL,
                result       TEXT DEFAULT 'pending',
                notes        TEXT,
                handler_id   INTEGER REFERENCES users(id),
                completed_at DATETIME,
                created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        migrations.append("建立 qc_result 表格")

    # system_settings 表格
    if not table_exists(c, 'system_settings'):
        c.execute("""
            CREATE TABLE system_settings (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                key   TEXT UNIQUE NOT NULL,
                value TEXT
            )
        """)
        migrations.append("建立 system_settings 表格")

    # inventory 新增欄位（如果缺少）
    inv_cols = [
        ("in_house_code", "TEXT"),
    ]
    for col, col_type in inv_cols:
        if not column_exists(c, 'inventory', col):
            c.execute(f"ALTER TABLE inventory ADD COLUMN {col} {col_type}")
            migrations.append(f"inventory.{col}")

    conn.commit()
    conn.close()

    if migrations:
        print(f"\n✅ 升級完成！共 {len(migrations)} 項變更：")
        for m in migrations:
            print(f"   + {m}")
    else:
        print("\n✅ 資料庫已是最新版本，無需升級")

    return True


if __name__ == '__main__':
    success = migrate()
    print()
    if success:
        input("按 Enter 關閉...")
    else:
        input("按 Enter 關閉...")
