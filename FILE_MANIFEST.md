# FILE_MANIFEST.md
# 檔案清單與說明
# File Manifest and Documentation

## 📦 完整檔案清單

本系統包含 **15 個主要檔案**，分為以下幾類：

---

## 🔴 核心應用檔案 (6 個)

### 1. **main.py** (Application Entry Point)
- **大小**: ~2 KB
- **類型**: Python 應用入口
- **說明**: 系統主程式，負責初始化資料庫和啟動 UI
- **功能**:
  - 初始化 SQLAlchemy 資料庫
  - 建立預設管理員帳號
  - 顯示登入視窗
  - 處理登入成功事件
  - 啟動主應用視窗
- **使用方式**: `python main.py`
- **依賴**: models.py, ui_login.py, ui_main.py

### 2. **models.py** (Database Models)
- **大小**: ~8 KB
- **類型**: SQLAlchemy 模型定義
- **說明**: 定義所有資料庫表格結構和 ORM 模型
- **包含的類**:
  - User (使用者表)
  - ReagentMaster (試劑主檔)
  - StockIn (入庫紀錄)
  - StockOut (出庫紀錄)
  - Inventory (庫存快照)
  - InventoryCheck (盤點紀錄)
  - ScrapRecord (報廢紀錄)
  - BarcodeRecord (條碼紀錄)
  - AuditLog (操作日誌)
  - DatabaseManager (資料庫管理器)
- **密碼加密**: SHA256
- **資料庫**: SQLite3

### 3. **services.py** (Business Logic Layer)
- **大小**: ~15 KB
- **類型**: 業務邏輯服務
- **說明**: 實現所有系統功能的核心邏輯
- **包含的服務類**:
  - UserService (使用者認證和管理)
  - ReagentService (試劑管理)
  - StockService (入出庫和 FEFO 邏輯)
  - InventoryCheckService (盤點管理)
  - ScrapService (報廢管理)
  - AuditLogService (審計日誌)
  - TraceabilityService (批號追溯)
- **主要功能**:
  - 入庫 (FEFO 邏輯)
  - 出庫（庫存檢查）
  - 庫存查詢
  - 快過期警示
  - 低庫存警示

### 4. **utils.py** (Utility Functions)
- **大小**: ~12 KB
- **類型**: 工具函數庫
- **說明**: 提供各種輔助功能
- **主要類和函數**:
  - BarcodeGenerator (Code128, QR Code 生成)
  - LabelPrinter (50×30mm 標籤生成)
  - DateHelper (日期計算和過期狀態判斷)
  - CodeGenerator (院內編號生成)
  - NetworkHelper (IP 獲取)
  - ValidationHelper (輸入驗證)
- **特點**:
  - 院內編號格式: R202608010001
  - 自動條碼生成
  - QR Code 包含試劑信息
  - 過期狀態顏色標示

### 5. **config.py** (Configuration)
- **大小**: ~6 KB
- **類型**: 系統配置檔案
- **說明**: 所有可調整的系統設定
- **可配置項**:
  - 資料庫路徑
  - 警示閾值（過期天數）
  - 備份設定
  - 列印機型號
  - 顏色方案
  - 功能開關
  - 預設試劑
  - 角色權限定義
- **默認值**:
  - 快過期警示: 90 天
  - 快過期警急: 30 天
  - 備份保留: 30 天
  - 自動備份時間: 凌晨 2:00

### 6. **init_database.py** (Database Setup)
- **大小**: ~5 KB
- **類型**: 初始化工具
- **說明**: 資料庫初始化和驗證工具
- **功能**:
  - 初始化資料庫和表格
  - 建立預設管理員
  - 建立預設試劑
  - 驗證資料庫完整性
  - 清理舊檔案
- **使用方式**:
  ```bash
  python init_database.py --init      # 初始化
  python init_database.py --reset     # 重置
  python init_database.py --verify    # 驗證
  python init_database.py --cleanup   # 清理
  ```

---

## 🟡 UI 介面檔案 (2 個)

### 7. **ui_login.py** (Login Window)
- **大小**: ~3 KB
- **類型**: PyQt6 使用者介面
- **說明**: 登入視窗
- **功能**:
  - 使用者名稱和密碼輸入
  - 登入驗證
  - 信號發射（登入成功）
  - 預設帳號顯示
- **視窗大小**: 500×350
- **登入信號**: login_success(user)
- **特點**:
  - 回車鍵快速登入
  - 密碼掩蔽顯示
  - 清除按鈕

### 8. **ui_main.py** (Main Application Window)
- **大小**: ~65 KB
- **類型**: PyQt6 主應用視窗
- **說明**: 系統所有功能的 UI 實現
- **包含的標籤頁**:
  1. 首頁 (Dashboard)
  2. 試劑設定 (Reagent Management)
  3. 入庫 (Stock In)
  4. 出庫 (Stock Out)
  5. 查詢 (Inventory Query)
  6. 盤點 (Inventory Check)
  7. 報廢 (Scrap Management)
  8. 追溯 (Traceability)
  9. 報表 (Reports) - Admin only
  10. 系統設定 (System Settings) - Admin only

- **主要功能**:
  - 即時統計卡片
  - 快過期試劑警示
  - 低庫存警示
  - 條碼掃描支援
  - Excel/PDF 匯出
  - 表單驗證
  - 彈出對話框

- **視窗大小**: 1920×1080 (可最大化)
- **風格**: HIS/LIS 專業風格

---

## 🟢 執行腳本 (2 個)

### 9. **run.bat** (Windows Batch Script)
- **大小**: ~1 KB
- **類型**: Windows 批處理檔案
- **說明**: Windows 自動執行腳本
- **自動化功能**:
  - ✓ 檢查 Python 安裝
  - ✓ 建立虛擬環境
  - ✓ 安裝依賴
  - ✓ 初始化資料庫
  - ✓ 啟動應用程式
- **使用**: 在 Windows 上雙擊或執行 `run.bat`
- **平台**: Windows 7 及以上

### 10. **run.sh** (Linux/macOS Shell Script)
- **大小**: ~1 KB
- **類型**: Unix Shell 腳本
- **說明**: Linux/macOS 自動執行腳本
- **自動化功能**: 同上
- **使用**: 
  ```bash
  chmod +x run.sh
  ./run.sh
  ```
- **平台**: Linux (Ubuntu/Debian/CentOS) 和 macOS

---

## 🔵 配置與文件 (5 個)

### 11. **requirements.txt** (Dependencies)
- **大小**: ~0.5 KB
- **類型**: Python 依賴清單
- **說明**: 列出所有必需的 Python 套件和版本
- **包含的套件** (13 個):
  - PyQt6==6.7.0 (GUI 框架)
  - SQLAlchemy==2.0.23 (ORM)
  - python-barcode==1.3.3 (條碼)
  - qrcode==7.4.2 (QR Code)
  - Pillow==10.1.0 (影像)
  - ReportLab==4.0.7 (PDF)
  - openpyxl==3.11.0 (Excel)
  - 等等...
- **安裝**: `pip install -r requirements.txt`

### 12. **README.md** (Main Documentation)
- **大小**: ~15 KB
- **類型**: Markdown 說明文件
- **內容**:
  - 系統簡介
  - 系統需求
  - 安裝步驟
  - 快速開始
  - 使用指南（8 章）
  - 常見問題
  - 版本歷史
  - 系統架構
- **用途**: 主要說明文檔，所有使用者必讀

### 13. **PROJECT_STRUCTURE.md** (Architecture Documentation)
- **大小**: ~20 KB
- **類型**: Markdown 技術文檔
- **內容**:
  - 完整專案結構
  - 檔案說明表
  - 系統工作流程圖
  - 資料庫表格詳解
  - 關鍵類別和方法
  - 安全機制
  - 自訂擴展指南
- **用途**: 開發人員和進階使用者

### 14. **TROUBLESHOOTING.md** (Problem Solving Guide)
- **大小**: ~18 KB
- **類型**: Markdown 故障排除指南
- **內容**:
  - 20+ 常見問題及解決方案
  - 日誌排查方法
  - 進階排查技巧
  - 常見錯誤列表
  - 系統檢查清單
- **涵蓋的問題類型**:
  - 安裝問題 (4 個)
  - 資料庫問題 (5 個)
  - UI 問題 (3 個)
  - 條碼與標籤 (3 個)
  - 報表問題 (2 個)
  - 安全與權限 (2 個)
  - 效能問題 (2 個)
- **用途**: 解決常見問題

---

## 🟣 測試與快速指南 (2 個)

### 15. **test_system.py** (System Test Suite)
- **大小**: ~10 KB
- **類型**: Python 測試腳本
- **說明**: 系統全面測試工具
- **測試項目** (8 個):
  1. 模組導入測試
  2. 資料庫測試
  3. 服務層測試
  4. 工具函數測試
  5. 條碼生成測試
  6. 檔案結構測試
  7. 配置驗證測試
  8. 目錄結構測試
- **使用**: `python test_system.py`
- **輸出**: 詳細的測試報告
- **用途**: 驗證系統完整性

### 16. **QUICKSTART.md** (Quick Start Guide)
- **大小**: ~12 KB
- **類型**: Markdown 快速指南
- **內容**:
  - 5 分鐘快速開始
  - 完整檔案清單
  - 功能速查表
  - 關鍵操作步驟
  - 顏色代碼說明
  - 系統提示
  - 進階配置
- **用途**: 新使用者快速上手

---

## 📊 自動建立的檔案/目錄

執行程式後會自動建立：

### 資料庫檔案
- **reagent_system.db** (SQLite 資料庫)
  - 包含所有系統資料
  - 大小: 初始 100 KB，會隨資料增加

### 虛擬環境
- **venv/** (Python 虛擬環境目錄)
  - Windows: `venv\Scripts\python.exe`
  - Linux/macOS: `venv/bin/python`
  - 大小: ~200 MB

### 輸出目錄
- **barcodes/** (條碼圖片)
  - 存儲 Code128 和 QR Code 圖片
  - 格式: PNG

- **labels/** (標籤圖片)
  - 存儲 50×30mm 標籤圖片
  - 格式: PNG

- **reports/** (匯出報表)
  - Excel 檔案: .xlsx
  - PDF 檔案: .pdf

- **backups/** (資料庫備份)
  - 每日自動備份
  - 保留 30 天

---

## 📈 檔案大小統計

| 類型 | 數量 | 總大小 | 說明 |
|------|------|--------|------|
| Python 代碼 | 8 | ~110 KB | 應用邏輯 |
| 執行腳本 | 2 | ~2 KB | 自動化 |
| 文檔 | 5 | ~70 KB | 說明和指南 |
| 配置 | 1 | ~1 KB | requirements.txt |
| **總計** | **16** | **~183 KB** | **原始檔案** |

虛擬環境安裝後會增加 ~200 MB（包括所有依賴）

---

## 🔑 關鍵檔案依賴關係

```
main.py
├── models.py
├── ui_login.py
├── ui_main.py
│   ├── models.py
│   ├── services.py
│   │   ├── models.py
│   │   └── utils.py
│   └── utils.py
└── config.py

init_database.py
├── models.py
└── config.py

test_system.py
├── models.py
├── services.py
├── config.py
└── utils.py
```

---

## 📋 檔案修改指南

### 安全修改
✅ 可以修改的檔案：
- `config.py` - 系統配置
- `DEFAULT_REAGENTS` 的內容

### 謹慎修改
⚠️ 需要小心修改：
- `models.py` - 修改需要重新初始化資料庫
- `services.py` - 修改核心業務邏輯
- `ui_main.py` - 修改 UI 可能影響使用者體驗

### 不建議修改
❌ 不建議修改：
- `main.py` - 修改可能無法啟動
- `requirements.txt` - 修改可能導致不相容

---

## 🔐 檔案權限設定

### Linux/macOS
```bash
# 執行權限
chmod +x run.sh

# 資料庫檔案
chmod 644 reagent_system.db
chmod 755 .

# 目錄
chmod 755 barcodes labels reports backups
```

### Windows
- 檔案應具有讀寫權限
- 目錄應可讀可寫可執行
- 若權限不足，右鍵 → 屬性 → 安全 → 編輯

---

## 📦 備份建議

### 需要備份的檔案
- ✅ `reagent_system.db` (最重要)
- ✅ `config.py` (自訂設定)
- ✅ `backups/` 目錄 (自動備份)

### 不需要備份
- ❌ `venv/` (可重新建立)
- ❌ `barcodes/`, `labels/`, `reports/` (可重新生成)
- ❌ Python 源代碼 (已有版本控制)

---

## 🔄 版本更新流程

1. **備份資料庫**
   ```bash
   cp reagent_system.db reagent_system.db.backup
   ```

2. **下載新版本檔案** (Python 代碼)

3. **保留資料庫** (reagent_system.db)

4. **執行應用**
   ```bash
   python main.py
   ```

5. **驗證功能** (檢查資料是否完整)

---

## 📞 檔案相關常見問題

**Q: 可以刪除虛擬環境嗎？**
A: 可以，但需要重新建立。執行 `run.bat` 或 `run.sh` 會自動重建。

**Q: 條碼和標籤檔案可以刪除嗎？**
A: 可以，系統會自動重新生成。但備份比較重要的標籤。

**Q: 資料庫檔案損壞怎麼辦？**
A: 使用備份還原：`cp reagent_system.db.backup reagent_system.db`

**Q: 能否移動檔案到其他目錄？**
A: 只要保持相對路徑和檔案名稱正確即可。建議保持整個 reagent-system 目錄結構不變。

---

最後更新：2024-08-01
版本：1.0.0
