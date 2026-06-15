# 多台電腦共用資料庫設定指南

## 三種方式比較

| 方式 | 台數 | 穩定性 | 設定難度 | 推薦場景 |
|------|------|--------|----------|----------|
| SQLite 本機 | 1台 | ✅ 穩定 | 簡單 | 單機使用 |
| SQLite 網路共享 | 2-3台 | ⚠️ 一般 | 簡單 | 小科室 |
| PostgreSQL | 不限 | ✅ 最穩定 | 中等 | 多人使用（推薦）|

---

## 方式 A：SQLite 網路共享（2-3台，最快設定）

### Server 電腦設定

1. 建立共享資料夾
   ```
   建立資料夾: C:\reagent-data\
   右鍵 → 內容 → 共用 → 進階共用
   勾選「共用此資料夾」
   設定名稱: reagent-data
   權限: Everyone → 完全控制
   ```

2. 把資料庫放進去
   ```
   複製 reagent_system.db 到 C:\reagent-data\
   ```

3. 查詢 Server IP
   ```cmd
   ipconfig
   ```
   記下 IPv4 位址，例如: 192.168.1.100

### 所有電腦的設定

1. 確認可以存取共享資料夾
   ```
   在檔案總管輸入: \\192.168.1.100\reagent-data
   應該看到 reagent_system.db
   ```

2. 修改 `db_config.py`
   ```python
   DB_MODE = 'sqlite_network'
   SQLITE_NETWORK_PATH = r'\\192.168.1.100\reagent-data\reagent_system.db'
   ```

3. 測試連線
   ```cmd
   python db_config.py
   ```
   應顯示: ✅ 資料庫連線成功

### 注意事項
- 同一時間最多 2-3 人同時操作
- Server 電腦必須保持開機
- 網路斷線時無法使用

---

## 方式 B：PostgreSQL（推薦，穩定多人使用）

### Server 電腦安裝 PostgreSQL

1. 下載 PostgreSQL
   ```
   https://www.postgresql.org/download/windows/
   選擇 PostgreSQL 16（Windows x86-64）
   ```

2. 安裝設定
   ```
   Port: 5432（預設，不要改）
   密碼: 設定一個強密碼（記住這個密碼）
   ```

3. 執行自動設定腳本
   ```cmd
   setup_postgresql.bat
   ```
   這會自動建立:
   - 資料庫: reagent_db
   - 使用者: reagent_user
   - 密碼: Reagent@2024

4. 允許其他電腦連線

   編輯 PostgreSQL 設定（通常在 C:\Program Files\PostgreSQL\16\data\）

   **pg_hba.conf** 加入這行：
   ```
   host    all    all    192.168.1.0/24    md5
   ```
   （192.168.1.0/24 改成你的網段）

   **postgresql.conf** 修改：
   ```
   listen_addresses = '*'
   ```

5. 重啟 PostgreSQL 服務
   ```cmd
   net stop postgresql-x64-16
   net start postgresql-x64-16
   ```

6. 防火牆開放 5432 port
   ```cmd
   netsh advfirewall firewall add rule name="PostgreSQL" ^
     dir=in action=allow protocol=TCP localport=5432
   ```

### 所有電腦的設定

1. 安裝 Python PostgreSQL 驅動
   ```cmd
   pip install psycopg2-binary
   ```

2. 修改 `db_config.py`
   ```python
   DB_MODE = 'postgresql'

   PG_HOST     = '192.168.1.100'  # Server 的 IP
   PG_PORT     = 5432
   PG_DATABASE = 'reagent_db'
   PG_USER     = 'reagent_user'
   PG_PASSWORD = 'Reagent@2024'
   ```

3. 測試連線
   ```cmd
   python db_config.py
   ```
   應顯示: ✅ 資料庫連線成功

4. 第一台電腦初始化資料庫
   ```cmd
   python main.py
   ```
   第一次執行會自動建立所有表格和預設帳號

5. 其他電腦直接執行
   ```cmd
   python main.py
   ```

### 優點
- 不限台數
- 穩定不鎖死
- 支援多人同時操作
- 有完整的連線管理

---

## db_config.py 說明

```python
# 三種模式
DB_MODE = 'sqlite_local'    # 本機（預設）
DB_MODE = 'sqlite_network'  # 網路共享
DB_MODE = 'postgresql'      # PostgreSQL

# SQLite 網路共享路徑
SQLITE_NETWORK_PATH = r'\\Server\reagent-data\reagent_system.db'

# PostgreSQL 連線設定
PG_HOST     = '192.168.1.100'
PG_PORT     = 5432
PG_DATABASE = 'reagent_db'
PG_USER     = 'reagent_user'
PG_PASSWORD = 'Reagent@2024'
```

---

## 測試連線

```cmd
python db_config.py
```

成功：
```
✅ 資料庫連線成功
   模式: postgresql
   伺服器: 192.168.1.100:5432/reagent_db
```

失敗常見原因：
- 防火牆未開放 5432
- PostgreSQL 服務未啟動
- 密碼錯誤
- 網路不通

---

## 常見問題

**Q: 多人同時操作會衝突嗎？**
A: PostgreSQL 有完整的鎖定機制，不會衝突。SQLite 網路共享模式有 30 秒 timeout，偶爾可能等待。

**Q: Server 電腦關機怎麼辦？**
A: 無法使用。建議 Server 電腦設定為不會自動休眠。

**Q: 資料怎麼備份？**
A: PostgreSQL 可用以下指令備份：
```cmd
pg_dump -U reagent_user reagent_db > backup.sql
```
還原：
```cmd
psql -U reagent_user reagent_db < backup.sql
```

**Q: 可以從 SQLite 轉移到 PostgreSQL 嗎？**
A: 可以，請聯繫開發人員協助資料轉移。

---

版本: 1.0.0
日期: 2024-08-01
