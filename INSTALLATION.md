# INSTALLATION.md
# 完整安裝指南
# Complete Installation Guide

## 📋 目錄
1. [系統需求](#系統需求)
2. [Windows 安裝](#windows-安裝)
3. [Linux 安裝](#linux-安裝)
4. [macOS 安裝](#macos-安裝)
5. [虛擬環境配置](#虛擬環境配置)
6. [依賴套件安裝](#依賴套件安裝)
7. [資料庫初始化](#資料庫初始化)
8. [驗證安裝](#驗證安裝)

---

## 系統需求

### 硬體需求
- **CPU**: Intel i5 或同級以上
- **RAM**: 4GB 或以上（推薦 8GB）
- **磁碟**: 500MB 以上可用空間
- **USB 介面**: 用於條碼掃描槍（選填）

### 軟體需求
- **Python**: 3.12 或以上版本
- **作業系統**:
  - Windows 7 Service Pack 1 或以上
  - Ubuntu 18.04+ / Debian 9+ / CentOS 7+
  - macOS 10.13+
- **網路**: 首次安裝需要網路下載依賴

---

## Windows 安裝

### 步驟 1: 安裝 Python 3.12

1. 訪問 https://www.python.org/downloads/
2. 下載 Windows installer（64-bit 推薦）
3. 執行安裝程式
4. ⚠️ **重要**: 勾選 "Add Python 3.12 to PATH"

```
□ Install launcher for all users
✓ Add Python 3.12 to PATH  ← 必須勾選
```

5. 點擊 "Install Now"
6. 等待安裝完成

### 步驟 2: 驗證 Python 安裝

打開「命令提示符」(cmd.exe) 輸入：

```cmd
python --version
```

應顯示 `Python 3.12.x` 或以上。

### 步驟 3: 下載專案檔案

1. 建立專案目錄：
```cmd
mkdir C:\reagent-system
cd C:\reagent-system
```

2. 將所有專案檔案放入此目錄

### 步驟 4: 執行安裝腳本

在專案目錄中執行：

```cmd
run.bat
```

腳本會自動進行以下操作：
- ✓ 建立 Python 虛擬環境
- ✓ 安裝依賴套件
- ✓ 初始化資料庫
- ✓ 啟動應用程式

### 步驟 5: 首次登入

使用預設帳號登入：
```
使用者名稱: admin
密碼: admin123
```

✅ **完成！** 應用程式已啟動。

---

## Linux 安裝

### Ubuntu/Debian

#### 步驟 1: 更新系統

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

#### 步驟 2: 安裝 Python 3.12

```bash
# Ubuntu 22.04 或更新版本
sudo apt-get install -y python3.12 python3.12-venv python3.12-dev

# 或使用 deadsnakes PPA（如果上面的不可用）
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3.12 python3.12-venv
```

#### 步驟 3: 安裝依賴

```bash
sudo apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-pip \
    git
```

#### 步驟 4: 建立專案目錄

```bash
mkdir -p ~/reagent-system
cd ~/reagent-system

# 下載/複製所有專案檔案到這個目錄
```

#### 步驟 5: 給執行腳本權限

```bash
chmod +x run.sh
```

#### 步驟 6: 執行安裝腳本

```bash
./run.sh
```

### CentOS/RHEL/Fedora

#### 步驟 1: 安裝 Python 3.12

```bash
# CentOS/RHEL 7
sudo yum install -y python3.12 python3.12-devel

# CentOS/RHEL 8+
sudo dnf install -y python3.12 python3.12-devel

# Fedora
sudo dnf install -y python3.12 python3.12-devel
```

#### 步驟 2: 安裝依賴

```bash
# CentOS/RHEL 7
sudo yum groupinstall -y "Development Tools"
sudo yum install -y openssl-devel libffi-devel

# CentOS/RHEL 8+ 或 Fedora
sudo dnf groupinstall -y "Development Tools"
sudo dnf install -y openssl-devel libffi-devel
```

#### 步驟 3: 後續步驟同上（4-6）

---

## macOS 安裝

### 使用 Homebrew（推薦）

#### 步驟 1: 安裝 Homebrew

如果未安裝，執行：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### 步驟 2: 安裝 Python 3.12

```bash
brew install python@3.12
```

#### 步驟 3: 建立符號連結（可選但推薦）

```bash
# 使 python3.12  命令可用
brew link python@3.12
```

#### 步驟 4: 驗證安裝

```bash
python3.12 --version
```

#### 步驟 5: 建立專案目錄

```bash
mkdir -p ~/reagent-system
cd ~/reagent-system

# 複製所有專案檔案
```

#### 步驟 6: 執行安裝腳本

```bash
chmod +x run.sh
./run.sh
```

### 手動安裝（不使用 Homebrew）

1. 訪問 https://www.python.org/downloads/macos/
2. 下載 macOS 64-bit installer
3. 執行安裝程式
4. 後續步驟同上（5-6）

---

## 虛擬環境配置

### 為什麼使用虛擬環境？

虛擬環境可以：
- 隔離專案依賴，避免與系統 Python 衝突
- 方便卸載（只需刪除目錄）
- 支援多個不同配置的 Python 環境

### 手動建立虛擬環境

如果自動腳本失敗，可手動建立：

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3.12 -m venv venv
source venv/bin/activate
```

### 啟用/停用虛擬環境

```bash
# 啟用
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 停用
deactivate
```

虛擬環境啟用後，提示符會顯示：
```
(venv) user@computer:~/reagent-system$
```

---

## 依賴套件安裝

### 自動安裝（推薦）

使用 `run.bat` 或 `run.sh` 會自動安裝所有依賴。

### 手動安裝

1. 首先啟用虛擬環境（見上面）

2. 安裝所有依賴：
```bash
pip install -r requirements.txt
```

3. 如果網路較慢，可使用清華大學源：
```bash
pip install -r requirements.txt -i https://pypi.tsinghua.edu.cn/simple
```

4. 或阿里雲源：
```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### 驗證依賴安裝

```bash
pip list
```

應顯示所有必要套件，例如：
```
PyQt6             6.7.0
SQLAlchemy        2.0.23
python-barcode    1.3.3
qrcode            7.4.2
Pillow            10.1.0
...
```

### 單個套件安裝（故障排除）

如果某個套件安裝失敗，可單獨安裝：

```bash
# 例如 PyQt6
pip install PyQt6==6.7.0

# 帶詳細輸出
pip install -v PyQt6==6.7.0

# 強制重新安裝
pip install --force-reinstall PyQt6==6.7.0
```

---

## 資料庫初始化

### 自動初始化

執行應用時會自動進行資料庫初始化：
```bash
python main.py
```

首次運行會自動：
- ✓ 建立 `reagent_system.db`
- ✓ 建立所有表格
- ✓ 建立預設管理員帳號

### 手動初始化

```bash
# 標準初始化
python init_database.py --init

# 重置資料庫（刪除現有資料）
python init_database.py --reset

# 驗證資料庫
python init_database.py --verify

# 清理舊檔案
python init_database.py --cleanup
```

### 初始化後查看資料庫

```bash
# 安裝 SQLite 瀏覽器（可選）
# Ubuntu/Debian:
sudo apt-get install sqlite3 sqlitebrowser

# macOS:
brew install sqlite3
brew install --cask db-browser-for-sqlite

# 查看資料庫
sqlite3 reagent_system.db
> SELECT * FROM users;
> .exit
```

---

## 驗證安裝

### 步驟 1: 執行系統測試

```bash
# 啟用虛擬環境
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

# 執行測試
python test_system.py
```

應顯示：
```
✅ 所有測試通過！系統已準備好使用。
```

### 步驟 2: 手動驗證

1. **啟動應用**
   ```bash
   python main.py
   ```

2. **檢查視窗**
   - 登入視窗應正常顯示
   - 視窗標題應為「醫療檢驗試劑管理系統 - 登入」

3. **測試登入**
   - 使用者名稱: `admin`
   - 密碼: `admin123`
   - 點擊「登入」

4. **檢查主視窗**
   - 主視窗應正常顯示
   - 所有標籤（試劑設定、入庫、出庫等）應可點擊
   - 首頁應顯示統計卡片和表格

5. **測試基本功能**
   - 點擊「試劑設定」
   - 點擊「新增試劑」
   - 輸入試劑信息並保存
   - 試劑應出現在表格中

### 步驟 3: 檢查檔案結構

```bash
# 應該看到以下檔案/目錄
ls -la  # Linux/macOS
dir     # Windows

reagent_system.db       # 資料庫檔案
venv/                   # 虛擬環境目錄
barcodes/               # 條碼目錄
labels/                 # 標籤目錄
reports/                # 報表目錄
backups/                # 備份目錄
```

---

## 常見安裝問題

### 問題：Python 未在 PATH 中

**症狀**: 
```
'python' 不是內部或外部命令
```

**解決方案**:
1. 重新安裝 Python，勾選 "Add Python to PATH"
2. 或手動添加到 PATH
3. 重新啟動命令提示符/終端

### 問題：虛擬環境啟用失敗

**症狀**:
```
無法找到 activate 腳本
```

**解決方案**:
```bash
# 重新建立虛擬環境
rm -rf venv  # 刪除舊環境
python3 -m venv venv  # 重新建立
source venv/bin/activate  # 或 venv\Scripts\activate
```

### 問題：依賴安裝超時

**解決方案**:
```bash
# 使用國內鏡像源
pip install -r requirements.txt \
    -i https://pypi.tsinghua.edu.cn/simple \
    --default-timeout=1000

# 或提高超時時間
pip install --default-timeout=1000 PyQt6==6.7.0
```

### 問題：PyQt6 導入失敗

**症狀**:
```
ModuleNotFoundError: No module named 'PyQt6'
```

**解決方案**:
```bash
# 確保虛擬環境已啟用
pip show PyQt6  # 檢查是否安裝

# 重新安裝
pip uninstall PyQt6 -y
pip install PyQt6==6.7.0
```

### 問題：資料庫鎖定

**症狀**:
```
database is locked
```

**解決方案**:
1. 關閉所有應用實例
2. 刪除 `.db-journal` 文件（如果存在）
3. 重試運行

```bash
rm reagent_system.db-journal
```

---

## 升級和更新

### 更新依賴

```bash
# 啟用虛擬環境
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 升級所有套件
pip install --upgrade -r requirements.txt

# 或只升級特定套件
pip install --upgrade PyQt6
```

### 備份資料庫

升級前備份資料庫：

```bash
# 複製資料庫
cp reagent_system.db reagent_system.db.backup

# 或使用 SQLite 工具
sqlite3 reagent_system.db ".backup reagent_system.db.backup"
```

---

## 卸載應用

### 完整卸載

```bash
# 刪除虛擬環境
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows

# 刪除資料庫（可選）
rm reagent_system.db

# 刪除生成的目錄
rm -rf barcodes labels reports backups

# 刪除整個專案目錄
rm -rf ~/reagent-system  # Linux/macOS
rmdir /s reagent-system  # Windows
```

### 保留資料卸載

如要保留資料庫但卸載應用：

```bash
# 只刪除虛擬環境和應用檔案
rm -rf venv
rm -rf *.py *.bat *.sh requirements.txt

# 保留：reagent_system.db 和備份
```

---

## 安裝檢查清單

- [ ] Python 3.12+ 已安裝
- [ ] Python 在 PATH 中
- [ ] 虛擬環境已建立
- [ ] 虛擬環境已啟用
- [ ] requirements.txt 已安裝
- [ ] test_system.py 測試通過
- [ ] 應用可正常啟動
- [ ] 可以用預設帳號登入
- [ ] 資料庫檔案已建立
- [ ] 所有目錄都已建立

---

## 下一步

安裝完成後，參考以下檔案：
- `README.md` - 完整系統說明
- `QUICKSTART.md` - 快速開始指南
- `PROJECT_STRUCTURE.md` - 專案結構詳解
- `TROUBLESHOOTING.md` - 故障排除指南

執行應用：
```bash
python main.py
```

---

最後更新：2024-08-01
版本：1.0.0
