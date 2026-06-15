# config.py
# 系統配置
# System Configuration

import os
from pathlib import Path

# 資料庫配置
DATABASE_NAME = 'reagent_system.db'
DATABASE_PATH = os.path.join(os.getcwd(), DATABASE_NAME)

# 檔案路徑配置
DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)

BARCODES_DIR = Path('barcodes')
BARCODES_DIR.mkdir(exist_ok=True)

LABELS_DIR = Path('labels')
LABELS_DIR.mkdir(exist_ok=True)

REPORTS_DIR = Path('reports')
REPORTS_DIR.mkdir(exist_ok=True)

BACKUPS_DIR = Path('backups')
BACKUPS_DIR.mkdir(exist_ok=True)

# 應用程式配置
APP_NAME = '醫療檢驗試劑管理系統'
APP_VERSION = '1.0.0'
APP_COMPANY = '衛生福利部花蓮醫院'

# 系統預設值
DEFAULT_ADMIN_USERNAME = 'admin'
DEFAULT_ADMIN_PASSWORD = 'admin123'

# 警示閾值設定
EXPIRY_WARNING_DAYS = 90  # 快過期警示（天數）
EXPIRY_CRITICAL_DAYS = 30  # 快過期警急（天數）

# 條碼設定
BARCODE_WIDTH = 50  # mm
BARCODE_HEIGHT = 30  # mm

# 標籤列印機設定（支援 Zebra, TSC, Godex）
PRINTER_MODELS = [
    'Zebra ZD420',
    'TSC TTP-244 Pro',
    'Godex GX430t'
]

# 日誌設定
LOG_LEVEL = 'INFO'  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = 'reagent_system.log'

# 備份設定
AUTO_BACKUP_TIME = '02:00'  # 每日備份時間
BACKUP_RETENTION_DAYS = 30  # 保留備份天數

# 操作日誌保留天數
AUDIT_LOG_RETENTION_DAYS = 365

# UI 設定
DEFAULT_WINDOW_WIDTH = 1920
DEFAULT_WINDOW_HEIGHT = 1080

# 表格設定
ITEMS_PER_PAGE = 20  # 每頁項目數

# 顏色方案（HIS/LIS 風格）
COLOR_SCHEME = {
    'primary': '#0078D4',      # 藍色
    'success': '#107C10',      # 綠色
    'warning': '#FFB900',      # 黃色
    'danger': '#D13438',       # 紅色
    'critical': '#8B0000',     # 深紅色
    'info': '#0078D4',         # 藍色
    'light': '#F0F0F0',        # 淺灰
    'dark': '#333333',         # 深灰
}

# 狀態代碼
STATUS_NORMAL = 'normal'
STATUS_WARNING = 'warning'
STATUS_CRITICAL = 'critical'
STATUS_EXPIRED = 'expired'

# FEFO 邏輯（先到期先出）
USE_FEFO = True

# 匯出格式
EXPORT_FORMATS = ['Excel', 'PDF', 'CSV']

# API 設定（若將來使用）
API_HOST = 'localhost'
API_PORT = 5000
API_DEBUG = False

# 功能開關
FEATURE_BARCODE_SCANNER = True      # 條碼掃描功能
FEATURE_LABEL_PRINTING = True       # 標籤列印功能
FEATURE_AUTO_BACKUP = True          # 自動備份功能
FEATURE_AUDIT_LOG = True            # 審計日誌功能
FEATURE_TRACEABILITY = True         # 追溯功能

# 權限定義
ROLE_PERMISSIONS = {
    'admin': [
        'reagent_create',
        'reagent_update',
        'reagent_delete',
        'stock_in',
        'stock_out',
        'inventory_check',
        'scrap_management',
        'user_management',
        'report_generation',
        'system_settings',
        'audit_log_view'
    ],
    'user': [
        'stock_in',
        'stock_out',
        'inventory_query',
        'inventory_check'
    ]
}


def get_permission_level(role):
    """
    取得角色的權限列表
    Get permissions for a role
    """
    return ROLE_PERMISSIONS.get(role, [])


def has_permission(role, permission):
    """
    檢查角色是否有特定權限
    Check if role has specific permission
    """
    return permission in get_permission_level(role)


# 預設試劑示例
DEFAULT_REAGENTS = [
    {
        'reagent_code': 'GLUCOSE-001',
        'reagent_name': '葡萄糖試劑',
        'reagent_name_en': 'Glucose Reagent',
        'brand': '華東醫學',
        'supplier': '華東醫學',
        'specification': '500mL',
        'unit': '瓶',
        'safety_stock': 10,
        'storage_condition': '2-8°C 避光保存',
        'equipment': '全自動生化儀'
    },
    {
        'reagent_code': 'ALT-001',
        'reagent_name': 'ALT 試劑',
        'reagent_name_en': 'ALT Reagent',
        'brand': '華東醫學',
        'supplier': '華東醫學',
        'specification': '200mL',
        'unit': '瓶',
        'safety_stock': 8,
        'storage_condition': '2-8°C',
        'equipment': '全自動生化儀'
    },
]


# 系統配置驗證
def validate_config():
    """驗證系統配置"""
    errors = []
    
    if not DATABASE_PATH:
        errors.append("資料庫路徑未設定")
    
    if not BACKUP_RETENTION_DAYS > 0:
        errors.append("備份保留天數必須大於0")
    
    if EXPIRY_CRITICAL_DAYS > EXPIRY_WARNING_DAYS:
        errors.append("快過期警急天數應小於警示天數")
    
    return len(errors) == 0, errors


if __name__ == '__main__':
    is_valid, errors = validate_config()
    if is_valid:
        print("✓ 配置驗證通過")
    else:
        print("✗ 配置驗證失敗:")
        for error in errors:
            print(f"  - {error}")
