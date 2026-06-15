# 建立獨立執行檔 (.exe)
# Create Standalone Executable

## 快速步驟 (10 分鐘)

### 步驟 1: 安裝 PyInstaller
```cmd
cd C:\reagent-system\
pip install pyinstaller
```

### 步驟 2: 建立 .exe 執行檔
```cmd
pyinstaller --onefile --windowed --name "ReagentSystem" main.py
```

### 步驟 3: 完成
執行檔在: `dist\ReagentSystem.exe`

可以直接雙擊執行，無需任何依賴！

---

## 詳細步驟

### 1. 確保已啟用虛擬環境
```cmd
cd C:\reagent-system\
venv\Scripts\activate
```

### 2. 安裝 PyInstaller
```cmd
pip install pyinstaller
```

### 3. 建立執行檔
```cmd
pyinstaller --onefile ^
    --windowed ^
    --name "ReagentSystem" ^
    main.py
```

### 4. 等待完成 (2-3 分鐘)
- 會自動編譯所有代碼
- 建立 dist\ 資料夾
- 生成 ReagentSystem.exe

### 5. 使用執行檔
```
C:\reagent-system\dist\ReagentSystem.exe
```

直接雙擊執行，不需要 Python!

---

## 優點

✅ 單一 .exe 檔案
✅ 無需安裝 Python
✅ 無需下載依賴
✅ 可直接分發給他人
✅ 雙擊即可運行

---

## 注意事項

⚠️ 第一次建立時會比較慢 (2-3 分鐘)
⚠️ 執行檔比較大 (約 200-300 MB)
⚠️ 啟動時間略長 (5-10 秒)

---

## 使用我準備的批處理檔案

也可以直接執行:
```cmd
build_exe.bat
```

它會自動完成所有步驟!

---

## 分發

完成後，可以將 `dist\ReagentSystem.exe` 發送給其他人。

他們只需要:
1. 下載 ReagentSystem.exe
2. 雙擊執行
3. 完成!

無需安裝 Python 或任何其他軟體。

---

## 疑難排除

如果出現錯誤:

1. 確保所有 Python 檔案都在同一資料夾
2. 確保虛擬環境已啟用
3. 嘗試: `pip install --upgrade pyinstaller`
4. 刪除 build\ 和 dist\ 資料夾，重新嘗試
