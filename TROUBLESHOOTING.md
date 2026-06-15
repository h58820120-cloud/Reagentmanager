# 故障排除和常見問題
# Troubleshooting & FAQ

## 🔧 安裝問題

### 問題 1: Python 未找到
```
❌ 錯誤：找不到 Python 3.12
```

**解決方案:**
- 確保已安裝 Python 3.12 或以上版本
- Windows: https://www.python.org/downloads/
- macOS: `brew install python@3.12`
- Ubuntu/Debian: `sudo apt-get install python3.12`
- 檢查是否在 PATH 中：`python --version`

### 問題 2: 虛擬環境建立失敗
```
❌ 虛擬環境建立失敗
```

**解決方案:**
```bash
# 手動建立虛擬環境
python -m venv venv

# 啟用虛擬環境
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 問題 3: 依賴安裝失敗
```
❌ 依賴套件安裝失敗
```

**解決方案:**
```bash
# 檢查網路連接
# 更新 pip
pip install --upgrade pip

# 嘗試使用清華大學源
pip install -r requirements.txt -i https://pypi.tsinghua.edu.cn/simple

# 或使用阿里源
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 逐個安裝套件以找出問題
pip install PyQt6==6.7.0
pip install SQLAlchemy==2.0.23
# ... 依此類推
```

### 問題 4: PyQt6 無法導入
```
ModuleNotFoundError: No module named 'PyQt6'
```

**解決方案:**
```bash
# 確保虛擬環境已啟用
# 重新安裝 PyQt6
pip install --force-reinstall PyQt6==6.7.0

# 如果仍然失敗，嘗試安裝依賴
pip install PyQt6-Qt6==6.7.0
pip install PyQt6-sip==13.6.0
```

---

## 💾 資料庫問題

### 問題 5: 資料庫初始化失敗
```
❌ 資料庫初始化失敗
```

**解決方案:**
```bash
# 刪除舊資料庫
rm reagent_system.db  # Linux/macOS
del reagent_system.db # Windows

# 重新執行初始化
python init_database.py --init

# 或直接運行應用（會自動初始化）
python main.py
```

### 問題 6: 無法連接資料庫
```
❌ 無法連接資料庫: permission denied
```

**解決方案:**
- 確保資料庫文件有讀寫權限
- 關閉其他正在使用資料庫的程式
- 檢查磁碟空間是否充足

```bash
# Linux/macOS: 修改文件權限
chmod 644 reagent_system.db
chmod 755 .

# Windows: 右鍵 → 屬性 → 安全 → 編輯 → 完全控制
```

### 問題 7: "資料庫已鎖定" 錯誤
```
database is locked
```

**解決方案:**
- 關閉所有應用實例
- 刪除 `.db-journal` 文件（如果存在）
- 檢查是否有其他進程使用資料庫

```bash
# 尋找使用資料庫的進程
lsof reagent_system.db  # Linux/macOS

# 結束進程
kill -9 <PID>
```

### 問題 8: 忘記管理員密碼
```
❌ 無法登入管理員帳號
```

**解決方案:**
```bash
# 方法 1: 刪除資料庫重新初始化
python init_database.py --reset

# 方法 2: 用 SQLite 工具修改密碼（高級用戶）
# 預設密碼對應的 SHA256：21241617e8d6d1f583fef0fb9fb5df75f63a8eda08db1370ddb7a7bf9d34a3f
```

---

## 🎨 UI/顯示問題

### 問題 9: 視窗無法正確顯示
```
❌ 無法開啟主視窗
```

**解決方案:**
- 更新顯卡驅動程式
- 嘗試使用不同的顯示器或解析度
- 檢查 PyQt6 是否正確安裝

```bash
# 重新安裝 PyQt6
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip
pip install -r requirements.txt
```

### 問題 10: 字體顯示亂碼
```
❌ 中文字無法正確顯示
```

**解決方案:**
- Linux 需要安裝中文字體
- macOS 通常無此問題
- Windows 檢查系統語言設定

```bash
# Ubuntu/Debian
sudo apt-get install fonts-noto-cjk

# CentOS/RHEL
sudo yum install google-noto-sans-cjk-fonts

# Fedora
sudo dnf install google-noto-sans-cjk-fonts
```

### 問題 11: 窗口太小或太大
**解決方案:**
編輯 `config.py`：
```python
DEFAULT_WINDOW_WIDTH = 1920
DEFAULT_WINDOW_HEIGHT = 1080
```

---

## 🏷️ 條碼與標籤問題

### 問題 12: 條碼掃描不工作
```
❌ 條碼槍無反應
```

**解決方案:**
1. 確認 USB 條碼槍已連接
2. 檢查條碼槍設定（應為鍵盤模式）
3. 掃描測試條碼確認功能
4. 在應用中：點擊條碼輸入框 → 掃描

```bash
# Linux: 檢查設備
ls -la /dev/ttyUSB*
dmesg | grep usb

# Windows: 裝置管理員 → COM 連接埠
```

### 問題 13: 標籤無法列印
```
❌ 標籤列印失敗
```

**解決方案:**
1. 檢查列印機是否已連接
2. 確認列印機為預設印表機
3. 檢查列印機驅動程式
4. 確保有列印紙

```bash
# Windows: 設定 → 裝置 → 印表機和掃描器 → 設為預設

# Linux: 安裝列印機驅動
sudo apt-get install cups  # Ubuntu
```

### 問題 14: 條碼圖片生成失敗
```
❌ 條碼生成失敗
```

**解決方案:**
- 確保 `barcodes/` 和 `labels/` 目錄存在且可寫

```bash
# 建立目錄
mkdir -p barcodes labels reports backups

# 檢查權限
chmod 755 barcodes labels reports backups
```

---

## 📊 報表與匯出問題

### 問題 15: Excel 報表無法建立
```
❌ 匯出 Excel 失敗
```

**解決方案:**
- 確保目錄可寫
- 檢查磁碟空間
- 確保文件名有效

```bash
# 建立 reports 目錄
mkdir -p reports

# 檢查權限
chmod 755 reports
```

### 問題 16: PDF 報表出現亂碼
```
❌ PDF 中文顯示亂碼
```

**解決方案:**
編輯 `ui_main.py` 中的 PDF 生成部分，添加中文字體：

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 註冊字體（需提供 .ttf 字體文件）
pdfmetrics.registerFont(TTFont('SimSun', 'simsun.ttf'))

# 在樣式中使用
ParagraphStyle(..., fontName='SimSun')
```

---

## 🔐 安全與權限問題

### 問題 17: 無法新增使用者
```
❌ 建立使用者失敗
```

**解決方案:**
- 確認是否以管理員身份登入
- 檢查使用者名稱是否已存在
- 確保密碼長度至少 6 個字符

### 問題 18: 操作被拒絕
```
❌ 您沒有權限執行此操作
```

**解決方案:**
- 確認使用者角色是否正確
- Admin 帳號才能：刪除試劑、修改系統設定、生成報表
- 聯繫系統管理員升級權限

---

## ⚙️ 效能問題

### 問題 19: 應用程式運行緩慢
```
❌ 操作時有明顯延遲
```

**解決方案:**
1. 檢查系統資源
   ```bash
   # Linux/macOS
   top
   free -h
   
   # Windows
   # 工作管理員 → 效能
   ```

2. 清理舊資料
   ```bash
   python init_database.py --cleanup
   ```

3. 優化資料庫
   ```bash
   # SQLite 資料庫最佳化
   sqlite3 reagent_system.db "VACUUM;"
   ```

### 問題 20: 記憶體使用過高
```
❌ 應用占用太多記憶體
```

**解決方案:**
- 減少表格顯示行數
- 實施分頁查詢
- 優化影像處理

編輯 `config.py`：
```python
ITEMS_PER_PAGE = 20  # 每頁顯示項目數
```

---

## 🌐 網路相關問題

### 問題 21: 無法使用線上資源
```
❌ 無法連接到線上服務
```

**解決方案:**
- 檢查網路連接
- 檢查防火牆設定
- 嘗試使用代理伺服器

---

## 📝 日誌排查

### 查看應用日誌
```bash
# 執行應用並查看輸出
python main.py 2>&1 | tee app.log

# 檢查日誌文件
tail -f reagent_system.log  # Linux/macOS
type reagent_system.log     # Windows
```

### 啟用 Debug 模式
編輯 `config.py`：
```python
LOG_LEVEL = 'DEBUG'  # 改為 DEBUG

# 或在 models.py 中啟用 SQLAlchemy 日誌
from sqlalchemy import create_engine
engine = create_engine('sqlite:///reagent_system.db', echo=True)
```

---

## 📞 進階排查

### 使用 SQLite 瀏覽器檢查資料庫
```bash
# 安裝 SQLite 工具
# Ubuntu: sudo apt-get install sqlite3
# macOS: brew install sqlite
# Windows: 下載 DB Browser for SQLite

# 命令行查詢
sqlite3 reagent_system.db
> SELECT * FROM users;
> SELECT COUNT(*) FROM stock_in;
> .exit
```

### Python REPL 測試
```python
from models import DatabaseManager
from services import ReagentService

db = DatabaseManager()
session = db.get_session()
service = ReagentService(session)

# 測試服務
reagents = service.get_all_reagents()
print(f"試劑數量: {len(reagents)}")

session.close()
```

---

## 📌 常見錯誤列表

| 錯誤代碼 | 錯誤信息 | 解決方案 |
|---------|---------|---------|
| 401 | 認證失敗 | 檢查使用者名稱和密碼 |
| 403 | 無權限 | 請求管理員權限 |
| 404 | 未找到 | 檢查試劑/單位是否存在 |
| 500 | 伺服器錯誤 | 檢查日誌找出問題 |
| SQLite | database locked | 關閉其他應用實例 |
| PyQt6 | Platform plugin error | 更新顯卡驅動或重裝 PyQt6 |

---

## ✅ 系統檢查清單

執行前檢查：
- [ ] Python 3.12+ 已安裝
- [ ] 虛擬環境已建立並啟用
- [ ] 依賴已安裝（`pip list` 檢查）
- [ ] 資料庫目錄可寫
- [ ] 條碼/標籤目錄存在
- [ ] 默認列印機已設定（如需列印功能）

執行後檢查：
- [ ] 資料庫文件已建立 (reagent_system.db)
- [ ] 可以以 admin 帳號登入
- [ ] 首頁統計資訊正常顯示
- [ ] 可以進行基本操作（新增試劑、入庫等）

---

## 📧 獲取幫助

如上述解決方案無法解決問題，請蒐集以下信息：

1. 完整的錯誤信息和堆疊追蹤
2. 系統資訊（OS, Python 版本）
3. 依賴版本清單（`pip list`）
4. 最近的日誌文件
5. 重現問題的步驟

聯繫系統管理員提供支援。

---

最後更新：2024-08-01
版本：1.0.0
