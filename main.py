import sys
import os
import sqlite3

# 支援 PyInstaller 打包後的路徑
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, 'reagent_system.db')

try:
    from PyQt6.QtWidgets import QApplication, QMessageBox
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(1)

from models import DatabaseManager
from ui_login import LoginWindow
from ui_main import MainWindow


def auto_migrate(db_path):
    """每次啟動時自動檢查並補齊缺少的欄位，不刪除任何資料"""
    if not os.path.exists(db_path):
        return  # 全新資料庫，init_database() 會建立

    conn = sqlite3.connect(db_path)
    c    = conn.cursor()

    def col_exists(table, col):
        c.execute(f"PRAGMA table_info({table})")
        return any(r[1] == col for r in c.fetchall())

    def tbl_exists(table):
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
        return c.fetchone() is not None

    # reagent_master 新增欄位
    for col, typ in [
        ("lot_start",  "INTEGER DEFAULT 0"),
        ("lot_length", "INTEGER DEFAULT 10"),
        ("exp_start",  "INTEGER DEFAULT 10"),
        ("exp_length", "INTEGER DEFAULT 6"),
        ("exp_format", "TEXT DEFAULT 'YYYYMMDD'"),
        ("need_qc",    "INTEGER DEFAULT 0"),
        ("qc_levels",  "INTEGER DEFAULT 1"),
        ("keeper_id",  "INTEGER"),
        ("units_per_box", "INTEGER DEFAULT 1"),
    ]:
        if not col_exists('reagent_master', col):
            c.execute(f"ALTER TABLE reagent_master ADD COLUMN {col} {typ}")

    # inventory 補欄位
    if tbl_exists('inventory') and not col_exists('inventory', 'in_house_code'):
        c.execute("ALTER TABLE inventory ADD COLUMN in_house_code TEXT")

    # qc_batch 表格
    if not tbl_exists('qc_batch'):
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

    # qc_result 表格
    if not tbl_exists('qc_result'):
        c.execute("""
            CREATE TABLE qc_result (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                batch_id     INTEGER NOT NULL REFERENCES qc_batch(id),
                level        INTEGER NOT NULL,
                result       TEXT DEFAULT 'pending',
                value        TEXT,
                notes        TEXT,
                handler_id   INTEGER REFERENCES users(id),
                completed_at DATETIME,
                created_at   DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

    # qc_result 補欄位（既有資料庫）
    if tbl_exists('qc_result') and not col_exists('qc_result', 'value'):
        c.execute("ALTER TABLE qc_result ADD COLUMN value TEXT")

    # system_settings 表格
    if not tbl_exists('system_settings'):
        c.execute("""
            CREATE TABLE system_settings (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                key   TEXT UNIQUE NOT NULL,
                value TEXT
            )
        """)

    conn.commit()
    conn.close()


def main():
    # 自動升級資料庫（補欄位）
    auto_migrate(DB_PATH)

    db_manager = DatabaseManager(DB_PATH)
    try:
        db_manager.init_database()
        db_manager.create_default_admin()
    except Exception as e:
        print(f"Database error: {e}")

    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    login_window = LoginWindow(DB_PATH)

    def on_login_success(user_id):
        try:
            main_window = MainWindow(user_id, DB_PATH)
            main_window.show()
            login_window.hide()
            app.main_window = main_window
        except Exception as e:
            QMessageBox.critical(login_window, "Error", str(e))

    login_window.login_success.connect(on_login_success)
    login_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
