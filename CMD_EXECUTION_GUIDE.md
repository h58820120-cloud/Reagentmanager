# Windows CMD 執行指南
# Windows Command Prompt Execution Guide

## 🖥️ 方法 1: 使用批處理檔案 (最簡單)

### 步驟 1: 準備檔案

1. 下載所有檔案
2. 將所有檔案放到一個資料夾，例如：
   ```
   C:\reagent-system\
   ```

### 步驟 2: 執行批處理檔案

#### 方式 A: 雙擊執行 (最簡單)
```
1. 打開資料夾: C:\reagent-system\
2. 找到檔案: run.bat 或 run_simple.bat
3. 雙擊執行
4. 等待應用啟動 (2-3 分鐘)
```

#### 方式 B: 在 CMD 中執行
```
1. 打開命令提示符 (Windows 鍵 + R，輸入 cmd，按 Enter)
2. 進入資料夾:
   cd C:\reagent-system\

3. 執行批處理檔案:
   run.bat
   
   或
   
   run_simple.bat
   (如果出現符號問題，使用 run_simple.bat)

4. 等待應用啟動
```

---

## 🖥️ 方法 2: 手動執行 (完全控制)

### 步驟 1: 安裝 Python

```
1. 訪問: https://www.python.org/downloads/
2. 下載 Python 3.12.x (64-bit)
3. 執行安裝程式
4. 重要: 勾選 "Add Python to PATH"
5. 點擊 "Install Now"
```

### 步驟 2: 驗證 Python 安裝

```
1. 打開命令提示符 (Windows 鍵 + R)
2. 輸入: python --version
3. 應該顯示: Python 3.12.x
```

### 步驟 3: 準備環境

```
1. 打開命令提示符
2. 進入您的資料夾:
   cd C:\reagent-system\
```

### 步驟 4: 建立虛擬環境

```
python -m venv venv
```

出現的情況:
- 會建立一個 venv 資料夾
- 需要 1-2 分鐘
- 完成後會回到提示符

### 步驟 5: 啟用虛擬環境

```
venv\Scripts\activate
```

成功標誌:
- 命令列前面會顯示: (venv)
- 例如: (venv) C:\reagent-system\>
```

### 步驟 6: 安裝依賴

```
pip install -r requirements.txt
```

如果出現網路問題，使用清華大學源:
```
pip install -r requirements.txt -i https://pypi.tsinghua.edu.cn/simple
```

等待 (2-3 分鐘):
- 會下載並安裝 13 個套件
- 最後顯示: Successfully installed ...

### 步驟 7: 初始化資料庫

```
python init_database.py --init
```

預期輸出:
```
=== 資料庫初始化 ===
建立資料庫表格...
✓ 資料庫表格建立成功
👤 建立預設管理員帳號...
✓ 預設管理員帳號已建立
初始化完成
```

### 步驟 8: 啟動應用程式

```
python main.py
```

成功標誌:
- 會自動打開應用視窗
- 顯示登入頁面
- 可以輸入帳號密碼

---

## 🆘 常見 CMD 錯誤及解決方案

### 錯誤 1: "不是內部或外部命令"

```
錯誤訊息:
'python' 不是內部或外部命令，也不是可執行程式

解決方案:
1. 檢查 Python 是否安裝: python --version
2. 如果出現相同錯誤，需要重新安裝 Python
3. 安裝時一定要勾選 "Add Python to PATH"
4. 重新啟動 CMD
```

### 錯誤 2: "不應有 &"

```
錯誤訊息:
不應有 &

解決方案:
1. 使用 run_simple.bat 代替 run.bat
2. 或手動執行命令，避免使用特殊符號
```

### 錯誤 3: "模組不存在"

```
錯誤訊息:
ModuleNotFoundError: No module named 'PyQt6'

解決方案:
1. 確認虛擬環境已啟用 (前面有 (venv))
2. 重新執行: pip install -r requirements.txt
3. 等待安裝完成
```

### 錯誤 4: "資料庫被鎖定"

```
錯誤訊息:
database is locked

解決方案:
1. 刪除 reagent_system.db 檔案
2. 重新執行: python init_database.py --init
3. 重新啟動應用
```

### 錯誤 5: "虛擬環境啟用失敗"

```
錯誤訊息:
無法進入虛擬環境

解決方案:
1. 刪除 venv 資料夾
2. 重新建立: python -m venv venv
3. 重新啟用: venv\Scripts\activate
```

---

## 📋 完整執行流程 (快速版)

```
C:\> cd C:\reagent-system\

C:\reagent-system\> run.bat

[自動執行以下步驟]
- 檢查 Python
- 建立虛擬環境
- 安裝依賴
- 初始化資料庫
- 啟動應用

[應用視窗自動打開]
帳號: admin
密碼: admin123
```

---

## 🎯 推薦執行步驟

### 第一次使用

```
1. 雙擊 run.bat (最簡單)
   或
   在 CMD 中執行: run.bat

2. 等待應用啟動

3. 登入系統:
   帳號: admin
   密碼: admin123

4. 首次登入後修改密碼
```

### 後續使用

```
第二次及以後:
1. 直接雙擊 run.bat
   或
   在 CMD 中執行: run.bat

2. 應用會快速啟動 (10 秒內)
```

---

## 🔧 進階: 直接在 CMD 中執行

如果不想使用批處理檔案，可以逐行執行:

```batch
REM 進入資料夾
cd C:\reagent-system\

REM 建立虛擬環境 (只需一次)
python -m venv venv

REM 啟用虛擬環境
venv\Scripts\activate

REM 安裝依賴 (只需一次)
pip install -r requirements.txt

REM 初始化資料庫 (只需一次)
python init_database.py --init

REM 啟動應用 (每次使用)
python main.py
```

---

## 📊 檔案校驗

執行前確認您有以下檔案:

```
✓ run.bat              (批處理執行檔)
✓ run_simple.bat       (簡化版執行檔)
✓ main.py              (應用程式)
✓ models.py            (資料庫模型)
✓ services.py          (業務邏輯)
✓ utils.py             (工具函數)
✓ config.py            (配置檔案)
✓ ui_login.py          (登入介面)
✓ ui_main.py           (主應用介面)
✓ ui_enhanced.py       (增強設計)
✓ init_database.py     (初始化工具)
✓ requirements.txt     (依賴清單)
```

共 12 個 Python 檔案

---

## ✅ 執行檢查清單

啟動應用後檢查:

- [ ] 命令列顯示正確的步驟訊息
- [ ] 沒有出現 "不應有 &" 錯誤
- [ ] 應用視窗成功打開
- [ ] 看到登入頁面
- [ ] 能輸入帳號和密碼
- [ ] 按 Enter 或點擊登入按鈕
- [ ] 成功進入主視窗
- [ ] 看到首頁儀表板

---

## 📞 仍有問題?

### 檢查清單

1. **Python 已安裝?**
   ```
   python --version
   ```
   應該顯示: Python 3.12.x

2. **在正確的資料夾?**
   ```
   dir
   ```
   應該看到 run.bat 和 main.py

3. **虛擬環境已啟用?**
   ```
   命令列前面應該有 (venv)
   ```

4. **依賴已安裝?**
   ```
   pip list
   ```
   應該看到 PyQt6, SQLAlchemy 等

### 嘗試方案

1. 使用 run_simple.bat 代替 run.bat
2. 檢查 Python 版本 (必須是 3.12+)
3. 重新安裝依賴: pip install -r requirements.txt
4. 刪除虛擬環境重新建立

---

## 🎉 成功!

一旦應用啟動，您就可以:

✅ 登入系統  
✅ 新增試劑  
✅ 執行入庫  
✅ 執行出庫  
✅ 查詢庫存  
✅ 執行所有操作  

享受使用!

---

**版本**: 1.0.0  
**開發日期**: 2024-08-01  
**支援平台**: Windows 7 及以上
