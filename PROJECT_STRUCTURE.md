# 專案結構文件
# Project Structure Documentation

## 📁 完整專案結構

```
reagent-system/
│
├── 📄 README.md                      # 系統說明文件
├── 📄 requirements.txt               # Python 依賴清單
├── 🐍 main.py                        # 應用程式入口
├── 🐍 config.py                      # 系統配置
├── 🐍 models.py                      # 資料庫模型 (SQLAlchemy)
├── 🐍 services.py                    # 業務邏輯服務層
├── 🐍 utils.py                       # 工具函數
├── 🐍 init_database.py               # 資料庫初始化腳本
│
├── UI 模組/
│  ├── 🐍 ui_login.py                # 登入視窗
│  └── 🐍 ui_main.py                 # 主應用視窗
│
├── 運行腳本/
│  ├── 📝 run.bat                    # Windows 執行腳本
│  └── 📝 run.sh                     # Linux/macOS 執行腳本
│
├── 資料庫/
│  └── 💾 reagent_system.db          # SQLite 資料庫（首次執行時建立）
│
├── 輸出目錄/
│  ├── 📁 barcodes/                  # Code128 & QR Code 條碼
│  ├── 📁 labels/                    # 標籤圖片
│  ├── 📁 reports/                   # 匯出的報表
│  └── 📁 backups/                   # 資料庫備份
│
└── 虛擬環境/
   └── 📁 venv/                       # Python 虛擬環境（執行後建立）
```

## 📋 檔案說明

### 核心應用檔案

| 檔案 | 說明 |
|------|------|
| `main.py` | 應用程式入口，初始化並啟動系統 |
| `models.py` | SQLAlchemy 資料庫模型定義，包含所有表格結構 |
| `services.py` | 業務邏輯層，實現所有功能的核心邏輯 |
| `utils.py` | 工具函數集合（條碼、標籤、日期、驗證等） |
| `config.py` | 系統配置文件（可自訂修改） |

### UI 介面

| 檔案 | 說明 |
|------|------|
| `ui_login.py` | PyQt6 登入視窗 |
| `ui_main.py` | PyQt6 主應用視窗，包含所有功能頁面 |

### 初始化與運行

| 檔案 | 說明 |
|------|------|
| `init_database.py` | 資料庫初始化工具 |
| `run.bat` | Windows 執行腳本（推薦使用） |
| `run.sh` | Linux/macOS 執行腳本（推薦使用） |
| `requirements.txt` | Python 依賴清單 |

### 資料庫檔案

| 檔案 | 說明 |
|------|------|
| `reagent_system.db` | SQLite 主資料庫（首次執行時自動建立） |

### 輸出目錄

| 目錄 | 說明 |
|------|------|
| `barcodes/` | 條碼圖片存儲位置 |
| `labels/` | 標籤圖片存儲位置 |
| `reports/` | 匯出的 Excel 和 PDF 報表 |
| `backups/` | 資料庫自動備份 |

## 🔄 系統工作流程

```
啟動應用
  ↓
初始化資料庫 (models.py)
  ↓
顯示登入視窗 (ui_login.py)
  ↓
使用者認證 (services.UserService)
  ↓
顯示主應用視窗 (ui_main.py)
  ↓
各功能模組:
  ├─ 試劑設定 → ReagentService
  ├─ 入庫 → StockService.stock_in()
  ├─ 出庫 → StockService.stock_out() + FEFO邏輯
  ├─ 查詢 → StockService.get_current_inventory()
  ├─ 盤點 → InventoryCheckService
  ├─ 報廢 → ScrapService
  ├─ 追溯 → TraceabilityService
  └─ 報表 → 匯出至 Excel/PDF
  ↓
記錄操作日誌 (AuditLogService)
  ↓
生成條碼/標籤 (BarcodeGenerator, LabelPrinter)
  ↓
自動備份 (每日凌晨)
```

## 🗄️ 資料庫表格詳細說明

### users - 使用者表
```sql
users
├── id (INTEGER PRIMARY KEY)
├── username (STRING UNIQUE) - 登入用戶名
├── password (STRING) - SHA256加密密碼
├── real_name (STRING) - 真實姓名
├── role (STRING) - admin 或 user
├── department (STRING)
├── is_active (BOOLEAN)
├── created_at (DATETIME)
└── last_login (DATETIME)
```

### reagent_master - 試劑主檔
```sql
reagent_master
├── id (INTEGER PRIMARY KEY)
├── reagent_code (STRING UNIQUE) - 試劑代碼
├── reagent_name (STRING) - 中文名稱
├── reagent_name_en (STRING) - 英文名稱
├── brand (STRING) - 廠牌
├── supplier (STRING) - 供應商
├── specification (STRING) - 規格 (e.g., 500mL)
├── unit (STRING) - 單位 (e.g., 瓶)
├── safety_stock (INTEGER) - 安全庫存量
├── storage_condition (STRING) - 儲存條件 (e.g., 2-8°C)
├── equipment (STRING) - 對應儀器
├── remark (TEXT)
├── created_at (DATETIME)
├── updated_at (DATETIME)
└── is_active (BOOLEAN)
```

### stock_in - 入庫紀錄
```sql
stock_in
├── id (INTEGER PRIMARY KEY)
├── reagent_id (INTEGER FK) → reagent_master.id
├── lot_number (STRING) - LOT號
├── expiry_date (STRING) - YYYY-MM-DD
├── quantity (INTEGER) - 入庫數量
├── po_number (STRING) - 採購單號
├── handler_id (INTEGER FK) → users.id
├── stock_in_date (DATETIME)
├── in_house_code (STRING UNIQUE) - R202608010001
└── remark (TEXT)
```

### stock_out - 出庫紀錄
```sql
stock_out
├── id (INTEGER PRIMARY KEY)
├── stock_in_id (INTEGER FK) → stock_in.id
├── quantity (INTEGER) - 出庫數量
├── usage_department (STRING) - 使用部門
├── usage_equipment (STRING) - 使用儀器
├── handler_id (INTEGER FK) → users.id
├── stock_out_date (DATETIME)
└── remark (TEXT)
```

### inventory - 當前庫存
```sql
inventory
├── id (INTEGER PRIMARY KEY)
├── reagent_id (INTEGER FK) → reagent_master.id
├── lot_number (STRING)
├── expiry_date (STRING)
├── in_house_code (STRING)
├── current_quantity (INTEGER) - 實時庫存
└── updated_at (DATETIME)
```

### inventory_check - 盤點紀錄
```sql
inventory_check
├── id (INTEGER PRIMARY KEY)
├── reagent_id (INTEGER FK)
├── lot_number (STRING)
├── system_quantity (INTEGER) - 系統庫存
├── actual_quantity (INTEGER) - 實際庫存
├── difference (INTEGER) - 差異 = actual - system
├── check_date (DATETIME)
└── remark (TEXT)
```

### scrap_records - 報廢紀錄
```sql
scrap_records
├── id (INTEGER PRIMARY KEY)
├── reagent_id (INTEGER FK)
├── lot_number (STRING)
├── quantity (INTEGER)
├── reason (STRING) - 過期/變質/QC失敗/儀器停用/其他
├── scrap_date (DATETIME)
└── remark (TEXT)
```

### barcode_records - 條碼紀錄
```sql
barcode_records
├── id (INTEGER PRIMARY KEY)
├── reagent_id (INTEGER FK)
├── in_house_code (STRING UNIQUE)
├── lot_number (STRING)
├── expiry_date (STRING)
├── code128_path (STRING) - 條碼圖檔路徑
├── qrcode_path (STRING) - QR碼圖檔路徑
└── created_at (DATETIME)
```

### audit_logs - 操作日誌
```sql
audit_logs
├── id (INTEGER PRIMARY KEY)
├── user_id (INTEGER FK)
├── action (STRING) - 登入/新增/修改/刪除/入庫/出庫/盤點/報廢
├── table_name (STRING) - 被操作的表名
├── record_id (INTEGER) - 被操作的記錄ID
├── details (TEXT) - 詳細內容
├── ip_address (STRING)
└── timestamp (DATETIME)
```

## 🎯 關鍵類別與方法

### services.py

#### UserService
- `authenticate(username, password)` - 認證使用者
- `create_user(...)` - 建立新使用者
- `get_user_by_id(user_id)` - 根據ID取得使用者
- `update_password(user_id, new_password)` - 更新密碼

#### ReagentService
- `create_reagent(...)` - 建立新試劑
- `get_reagent_by_code(code)` - 根據代碼查詢
- `get_all_reagents()` - 取得所有試劑
- `update_reagent(id, **kwargs)` - 更新試劑
- `delete_reagent(id)` - 刪除試劑

#### StockService
- `stock_in(...)` - 執行入庫
- `stock_out(...)` - 執行出庫（含FEFO邏輯）
- `get_current_inventory()` - 取得當前庫存
- `get_low_stock_items()` - 取得低庫存項目
- `get_expiring_items(days)` - 取得即將過期項目

#### InventoryCheckService
- `create_check_record(...)` - 建立盤點紀錄

#### ScrapService
- `create_scrap_record(...)` - 建立報廢紀錄

#### TraceabilityService
- `get_traceability(...)` - 查詢批號追溯

### utils.py

#### BarcodeGenerator
- `generate_code128(code)` - 生成Code128條碼
- `generate_qrcode(data)` - 生成QR Code

#### LabelPrinter
- `generate_label_50x30(...)` - 生成50×30mm標籤
- `generate_sublabel(...)` - 生成分裝子標籤

#### DateHelper
- `get_days_until_expiry(date_str)` - 計算距離到期日期
- `get_expiry_status(date_str)` - 取得過期狀態與顏色

#### CodeGenerator
- `generate_in_house_code()` - 生成院內編號 (R202608010001)

## 🔐 安全機制

1. **密碼安全**
   - 採用 SHA256 加密
   - 不儲存明文密碼

2. **操作追蹤**
   - 每項操作記錄在 audit_logs
   - 包含使用者、時間、IP、內容

3. **角色權限**
   - Admin：完全權限
   - User：限制權限（無系統設定、無刪除）

4. **資料備份**
   - 每日凌晨自動備份
   - 保留30天備份

5. **資料完整性**
   - 外鍵約束
   - 級聯更新/刪除

## 📈 效能優化

1. **資料庫索引**
   - unique 欄位自動建立索引
   - primary key 自動建立索引

2. **查詢最佳化**
   - 使用 filter 進行過濾
   - 使用 join 進行關聯查詢

3. **UI 反應**
   - 異步加載資料（可擴展）
   - 表格虛擬化（大量資料時）

## 🔧 自訂擴展

### 新增自訂試劑
編輯 `config.py` 中的 `DEFAULT_REAGENTS`：

```python
DEFAULT_REAGENTS = [
    {
        'reagent_code': 'YOUR-CODE',
        'reagent_name': '你的試劑名稱',
        # ... 其他欄位
    },
]
```

### 修改警示閾值
編輯 `config.py`：

```python
EXPIRY_WARNING_DAYS = 90  # 修改為所需天數
EXPIRY_CRITICAL_DAYS = 30
```

### 自訂報表
編輯 `ui_main.py` 中的 `export_excel_report()` 和 `export_pdf_report()`

## 📞 技術支援

如有問題，請檢查：
1. Python 版本是否為 3.12+
2. 所有依賴是否正確安裝
3. 資料庫文件是否可寫
4. 列印機是否正確連接

---

更新日期: 2024-08-01
版本: 1.0.0
