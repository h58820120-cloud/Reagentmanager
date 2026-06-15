# init_database.py
# 資料庫初始化和設定
# Database Initialization and Setup

"""
這個腳本用於初始化資料庫並進行基本設定。
This script initializes the database and performs basic setup.
"""

import sys
import os
from datetime import datetime
from models import DatabaseManager, User, ReagentMaster
from config import DEFAULT_REAGENTS


def init_database():
    """初始化資料庫"""
    print("=" * 60)
    print("醫療檢驗試劑管理系統 - 資料庫初始化")
    print("=" * 60)
    print()
    
    try:
        # 建立資料庫管理器
        db_manager = DatabaseManager('reagent_system.db')
        
        # 建立所有表格
        print("📦 建立資料庫表格...")
        db_manager.init_database()
        print("✓ 資料庫表格建立成功")
        print()
        
        # 建立預設管理員
        print("👤 建立預設管理員帳號...")
        db_manager.create_default_admin()
        print("✓ 預設管理員帳號已建立 (username: admin, password: admin123)")
        print()
        
        # 建立預設試劑
        print("🧪 建立預設試劑...")
        session = db_manager.get_session()
        
        for reagent_data in DEFAULT_REAGENTS:
            # 檢查是否已存在
            existing = session.query(ReagentMaster).filter_by(
                reagent_code=reagent_data['reagent_code']
            ).first()
            
            if not existing:
                reagent = ReagentMaster(**reagent_data)
                session.add(reagent)
                print(f"  ✓ {reagent_data['reagent_name']}")
        
        session.commit()
        session.close()
        print("✓ 預設試劑建立成功")
        print()
        
        # 顯示系統信息
        print("=" * 60)
        print("✅ 資料庫初始化完成！")
        print("=" * 60)
        print()
        print("📝 系統信息：")
        print(f"  資料庫文件: reagent_system.db")
        print(f"  初始化時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("🔐 登入信息：")
        print("  使用者名稱: admin")
        print("  密碼: admin123")
        print()
        print("⚠️  注意：首次登入後請立即修改密碼！")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ 初始化失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def verify_database():
    """驗證資料庫完整性"""
    print("驗證資料庫...")
    
    try:
        db_manager = DatabaseManager('reagent_system.db')
        session = db_manager.get_session()
        
        # 檢查各表的記錄數
        tables_info = {
            'User': session.query(User).count(),
            'ReagentMaster': session.query(ReagentMaster).count(),
        }
        
        session.close()
        
        print("\n📊 資料庫統計：")
        for table_name, count in tables_info.items():
            print(f"  {table_name}: {count} 條記錄")
        
        return True
    except Exception as e:
        print(f"❌ 驗證失敗: {str(e)}")
        return False


def show_usage():
    """顯示使用說明"""
    print("\n📖 使用說明：")
    print("\n1. 執行應用程式：")
    print("   python main.py")
    print("\n2. 使用預設帳號登入：")
    print("   使用者名稱: admin")
    print("   密碼: admin123")
    print("\n3. 首次登入後修改密碼（推薦）")
    print("\n4. 開始使用系統：")
    print("   - 試劑設定：管理試劑主檔")
    print("   - 入庫：記錄試劑入庫")
    print("   - 出庫：記錄試劑出庫")
    print("   - 查詢：查看當前庫存")
    print("   - 盤點：進行實物盤點")
    print("   - 報廢：報廢過期或變質試劑")
    print("   - 追溯：查詢批號歷史")
    print("   - 報表：匯出各類報表（管理員）")
    print("\n5. 系統設定（管理員）：")
    print("   - 使用者管理：新增/修改使用者")
    print("   - 審計日誌：查看所有操作記錄")


def cleanup_old_files():
    """清理舊檔案"""
    import shutil
    from pathlib import Path
    
    print("\n清理舊檔案...")
    
    dirs_to_clean = [
        Path('barcodes'),
        Path('labels'),
        Path('reports'),
    ]
    
    for dir_path in dirs_to_clean:
        if dir_path.exists():
            try:
                # 保留目錄，只清空內容
                for file in dir_path.glob('*'):
                    if file.is_file():
                        file.unlink()
                print(f"  ✓ {dir_path}/")
            except Exception as e:
                print(f"  ⚠️  無法清理 {dir_path}: {e}")
    
    print("✓ 清理完成")


def main():
    """主程式"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='醫療檢驗試劑管理系統 - 資料庫初始化工具'
    )
    parser.add_argument(
        '--init',
        action='store_true',
        help='初始化資料庫'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='驗證資料庫'
    )
    parser.add_argument(
        '--cleanup',
        action='store_true',
        help='清理舊檔案'
    )
    parser.add_argument(
        '--reset',
        action='store_true',
        help='重置資料庫（刪除現有資料庫）'
    )
    
    args = parser.parse_args()
    
    # 如果沒有指定任何參數，執行完整初始化
    if not any(vars(args).values()):
        args.init = True
    
    # 重置資料庫
    if args.reset:
        if os.path.exists('reagent_system.db'):
            print("⚠️  即將刪除現有資料庫...")
            response = input("確定要刪除嗎？ (yes/no): ")
            if response.lower() == 'yes':
                os.remove('reagent_system.db')
                print("✓ 資料庫已刪除")
            else:
                print("操作已取消")
                return
    
    # 初始化資料庫
    if args.init:
        success = init_database()
        if not success:
            sys.exit(1)
    
    # 驗證資料庫
    if args.verify:
        verify_database()
    
    # 清理檔案
    if args.cleanup:
        cleanup_old_files()
    
    # 顯示使用說明
    if args.init:
        show_usage()
    
    print("\n" + "=" * 60)
    print("✅ 所有操作完成！")
    print("=" * 60)


if __name__ == '__main__':
    main()
