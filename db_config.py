# db_config.py
# 資料庫連線設定
# 修改這個檔案來切換資料庫模式

import os
import sys

# ============================================================
# 選擇資料庫模式（修改這裡）
# ============================================================
# 'sqlite_local'   → 本機 SQLite（單機使用）
# 'sqlite_network' → 網路共享資料夾 SQLite（2-3台電腦）
# 'postgresql'     → PostgreSQL（多台電腦，推薦）
# ============================================================

DB_MODE = 'sqlite_local'

# ============================================================
# SQLite 本機設定
# ============================================================
SQLITE_LOCAL_PATH = 'reagent_system.db'

# ============================================================
# SQLite 網路共享設定
# 把資料庫放在網路共享資料夾
# 例如: \\\\Server\\reagent-data\\reagent_system.db
# ============================================================
SQLITE_NETWORK_PATH = r'\\Server\reagent-data\reagent_system.db'

# ============================================================
# PostgreSQL 設定
# 需要先安裝 PostgreSQL Server
# ============================================================
PG_HOST     = '192.168.1.100'   # PostgreSQL Server 的 IP
PG_PORT     = 5432
PG_DATABASE = 'reagent_db'
PG_USER     = 'reagent_user'
PG_PASSWORD = 'your_password'


def get_database_url():
    """
    根據 DB_MODE 回傳對應的資料庫連線字串
    """
    if DB_MODE == 'sqlite_local':
        if getattr(sys, 'frozen', False):
            base = os.path.dirname(sys.executable)
        else:
            base = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base, SQLITE_LOCAL_PATH)
        return f'sqlite:///{path}', path

    elif DB_MODE == 'sqlite_network':
        return f'sqlite:///{SQLITE_NETWORK_PATH}', SQLITE_NETWORK_PATH

    elif DB_MODE == 'postgresql':
        url = (f'postgresql://{PG_USER}:{PG_PASSWORD}'
               f'@{PG_HOST}:{PG_PORT}/{PG_DATABASE}')
        return url, None

    else:
        raise ValueError(f"不支援的 DB_MODE: {DB_MODE}")


def get_engine_kwargs():
    """
    根據資料庫類型回傳對應的 SQLAlchemy engine 參數
    """
    if DB_MODE in ('sqlite_local', 'sqlite_network'):
        return {
            'echo': False,
            'connect_args': {
                'timeout': 30,           # 等待鎖定最多 30 秒
                'check_same_thread': False
            }
        }
    elif DB_MODE == 'postgresql':
        return {
            'echo': False,
            'pool_size': 10,             # 連線池大小
            'max_overflow': 20,          # 最大溢出連線
            'pool_pre_ping': True,       # 自動重連
            'pool_recycle': 3600,        # 每小時回收連線
        }
    return {}


def test_connection():
    """
    測試資料庫連線
    """
    try:
        from sqlalchemy import create_engine, text
        url, path = get_database_url()
        kwargs    = get_engine_kwargs()
        engine    = create_engine(url, **kwargs)
        with engine.connect() as conn:
            conn.execute(text('SELECT 1'))
        print(f"✅ 資料庫連線成功")
        print(f"   模式: {DB_MODE}")
        if path:
            print(f"   路徑: {path}")
        else:
            print(f"   伺服器: {PG_HOST}:{PG_PORT}/{PG_DATABASE}")
        return True
    except Exception as e:
        print(f"❌ 資料庫連線失敗: {e}")
        return False


if __name__ == '__main__':
    test_connection()
