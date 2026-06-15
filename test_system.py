# test_system.py
# 系統測試和驗證
# System Testing and Validation

"""
用於測試系統各組件是否正常工作的測試腳本。
Script for testing if all system components work correctly.
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path


def test_imports():
    """測試所有必要的模組是否可以導入"""
    print("\n🧪 測試 1: 模組導入")
    print("-" * 50)
    
    tests = [
        ('PyQt6', 'PyQt6.QtWidgets'),
        ('SQLAlchemy', 'sqlalchemy'),
        ('python-barcode', 'barcode'),
        ('qrcode', 'qrcode'),
        ('Pillow', 'PIL'),
        ('ReportLab', 'reportlab'),
        ('openpyxl', 'openpyxl'),
    ]
    
    passed = 0
    failed = 0
    
    for name, module in tests:
        try:
            __import__(module)
            print(f"  ✅ {name} ({module})")
            passed += 1
        except ImportError as e:
            print(f"  ❌ {name} ({module}): {e}")
            failed += 1
    
    print(f"\n結果: {passed}/{len(tests)} 通過")
    return failed == 0


def test_database():
    """測試資料庫功能"""
    print("\n🧪 測試 2: 資料庫")
    print("-" * 50)
    
    try:
        from models import DatabaseManager, User, ReagentMaster
        
        # 建立測試資料庫
        db = DatabaseManager(':memory:')  # 使用記憶體資料庫進行測試
        db.init_database()
        print("  ✅ 資料庫初始化成功")
        
        session = db.get_session()
        
        # 測試新增使用者
        user = User(username='test', real_name='測試用戶', role='user')
        user.set_password('test123')
        session.add(user)
        session.commit()
        print("  ✅ 使用者新增成功")
        
        # 測試查詢
        retrieved_user = session.query(User).filter_by(username='test').first()
        if retrieved_user and retrieved_user.verify_password('test123'):
            print("  ✅ 使用者查詢和密碼驗證成功")
        else:
            print("  ❌ 使用者查詢或密碼驗證失敗")
            return False
        
        # 測試新增試劑
        reagent = ReagentMaster(
            reagent_code='TEST001',
            reagent_name='測試試劑',
            reagent_name_en='Test Reagent',
            brand='測試品牌',
            unit='瓶',
            safety_stock=10
        )
        session.add(reagent)
        session.commit()
        print("  ✅ 試劑新增成功")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"  ❌ 資料庫測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_services():
    """測試業務邏輯服務"""
    print("\n🧪 測試 3: 業務邏輯服務")
    print("-" * 50)
    
    try:
        from models import DatabaseManager
        from services import UserService, ReagentService, StockService
        
        db = DatabaseManager(':memory:')
        db.init_database()
        session = db.get_session()
        
        # 測試 UserService
        user_service = UserService(session)
        success, msg = user_service.create_user('testuser', 'password123', '測試用戶')
        if success:
            print(f"  ✅ UserService 工作正常: {msg}")
        else:
            print(f"  ❌ UserService 失敗: {msg}")
            return False
        
        # 測試 ReagentService
        reagent_service = ReagentService(session)
        success, msg = reagent_service.create_reagent(
            reagent_code='GLU001',
            reagent_name='葡萄糖',
            brand='華東',
            safety_stock=10
        )
        if success:
            print(f"  ✅ ReagentService 工作正常: {msg}")
        else:
            print(f"  ❌ ReagentService 失敗: {msg}")
            return False
        
        # 測試 StockService
        stock_service = StockService(session)
        reagent = reagent_service.get_reagent_by_code('GLU001')
        user = user_service.get_user_by_id(1)
        
        if reagent and user:
            success, msg = stock_service.stock_in(
                reagent_id=reagent.id,
                lot_number='LOT001',
                expiry_date='2026-12-31',
                quantity=100,
                po_number='PO001',
                handler_id=user.id,
                remark='測試入庫'
            )
            if success:
                print(f"  ✅ StockService 工作正常: {msg}")
            else:
                print(f"  ❌ StockService 失敗: {msg}")
                return False
        
        session.close()
        return True
        
    except Exception as e:
        print(f"  ❌ 服務測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_utilities():
    """測試工具函數"""
    print("\n🧪 測試 4: 工具函數")
    print("-" * 50)
    
    try:
        from utils import (
            BarcodeGenerator, DateHelper, CodeGenerator,
            ValidationHelper, NetworkHelper
        )
        
        # 測試代碼生成
        code = CodeGenerator.generate_in_house_code()
        if code.startswith('R'):
            print(f"  ✅ 院內編號生成: {code}")
        else:
            print("  ❌ 院內編號生成失敗")
            return False
        
        # 測試日期助手
        days = DateHelper.get_days_until_expiry('2026-12-31')
        if days > 0:
            print(f"  ✅ 到期日期計算: {days} 天")
        else:
            print("  ❌ 到期日期計算失敗")
            return False
        
        # 測試過期狀態
        status, color = DateHelper.get_expiry_status('2026-12-31')
        print(f"  ✅ 過期狀態判斷: {status} ({color})")
        
        # 測試驗證
        is_valid, msg = ValidationHelper.validate_quantity(10)
        if is_valid:
            print("  ✅ 數量驗證通過")
        else:
            print(f"  ❌ 數量驗證失敗: {msg}")
            return False
        
        is_valid, msg = ValidationHelper.validate_expiry_date('2026-12-31')
        if is_valid:
            print("  ✅ 日期驗證通過")
        else:
            print(f"  ❌ 日期驗證失敗: {msg}")
            return False
        
        # 測試 IP 獲取
        ip = NetworkHelper.get_local_ip()
        print(f"  ✅ 本機 IP: {ip}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 工具函數測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_barcode_generation():
    """測試條碼生成"""
    print("\n🧪 測試 5: 條碼生成")
    print("-" * 50)
    
    try:
        from utils import BarcodeGenerator
        
        # 測試 Code128
        code128_path = BarcodeGenerator.generate_code128('R202608010001')
        if code128_path and os.path.exists(code128_path):
            print(f"  ✅ Code128 條碼生成: {code128_path}")
        else:
            print("  ❌ Code128 條碼生成失敗")
            return False
        
        # 測試 QR Code
        qr_data = {
            "id": "R202608010001",
            "name": "葡萄糖",
            "lot": "LOT001",
            "exp": "2026-12-31"
        }
        qrcode_path = BarcodeGenerator.generate_qrcode(qr_data)
        if qrcode_path and os.path.exists(qrcode_path):
            print(f"  ✅ QR Code 生成: {qrcode_path}")
        else:
            print("  ❌ QR Code 生成失敗")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ 條碼生成測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_structure():
    """測試檔案結構"""
    print("\n🧪 測試 6: 檔案結構")
    print("-" * 50)
    
    required_files = [
        'main.py',
        'models.py',
        'services.py',
        'utils.py',
        'config.py',
        'ui_login.py',
        'ui_main.py',
        'init_database.py',
        'requirements.txt',
        'README.md',
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} 未找到")
            missing.append(file)
    
    return len(missing) == 0


def test_configuration():
    """測試配置檔案"""
    print("\n🧪 測試 7: 配置檔案")
    print("-" * 50)
    
    try:
        from config import (
            validate_config,
            DEFAULT_REAGENTS,
            EXPIRY_WARNING_DAYS,
            EXPIRY_CRITICAL_DAYS,
            BACKUP_RETENTION_DAYS
        )
        
        # 驗證配置
        is_valid, errors = validate_config()
        if is_valid:
            print("  ✅ 配置驗證通過")
        else:
            print("  ❌ 配置驗證失敗:")
            for error in errors:
                print(f"     - {error}")
            return False
        
        # 檢查預設值
        print(f"  ✅ 快過期警示天數: {EXPIRY_WARNING_DAYS}")
        print(f"  ✅ 快過期警急天數: {EXPIRY_CRITICAL_DAYS}")
        print(f"  ✅ 備份保留天數: {BACKUP_RETENTION_DAYS}")
        print(f"  ✅ 預設試劑數: {len(DEFAULT_REAGENTS)}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 配置測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_directories():
    """測試必要的目錄"""
    print("\n🧪 測試 8: 目錄結構")
    print("-" * 50)
    
    directories = [
        'barcodes',
        'labels',
        'reports',
        'backups',
    ]
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        
        if path.exists() and path.is_dir():
            print(f"  ✅ {directory}/")
        else:
            print(f"  ❌ {directory}/ 建立失敗")
            return False
    
    return True


def generate_test_report():
    """生成測試報告"""
    print("\n" + "=" * 60)
    print("📊 系統測試報告")
    print("=" * 60)
    
    tests = [
        ("模組導入", test_imports),
        ("資料庫", test_database),
        ("業務邏輯服務", test_services),
        ("工具函數", test_utilities),
        ("條碼生成", test_barcode_generation),
        ("檔案結構", test_file_structure),
        ("配置檔案", test_configuration),
        ("目錄結構", test_directories),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"\n❌ {test_name} 測試異常: {e}")
            results[test_name] = False
    
    # 總結
    print("\n" + "=" * 60)
    print("📈 測試結果總結")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n總體結果: {passed}/{total} 項測試通過\n")
    
    for test_name, result in results.items():
        status = "✅ 通過" if result else "❌ 失敗"
        print(f"  {status} - {test_name}")
    
    print()
    
    if passed == total:
        print("🎉 所有測試通過！系統已準備好使用。")
        print("\n執行下一步:")
        print("  python main.py")
        return True
    else:
        print(f"⚠️  有 {total - passed} 項測試失敗。")
        print("\n請檢查上面的錯誤信息並修復問題。")
        print("參考 TROUBLESHOOTING.md 獲取幫助。")
        return False


def main():
    """主測試程式"""
    print("\n" + "=" * 60)
    print("🧪 醫療檢驗試劑管理系統 - 系統測試")
    print("=" * 60)
    print(f"\n測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python 版本: {sys.version}")
    print(f"工作目錄: {os.getcwd()}")
    
    success = generate_test_report()
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
