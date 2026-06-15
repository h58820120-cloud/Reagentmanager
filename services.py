# services.py
# 業務邏輯服務層
# Business Logic Services

from datetime import datetime, timedelta
from models import (
    User, ReagentMaster, StockIn, StockOut, Inventory,
    InventoryCheck, ScrapRecord, BarcodeRecord, AuditLog,
    QCBatch, QCResult, DatabaseManager
)
from utils import CodeGenerator, DateHelper, BarcodeGenerator, ValidationHelper
from sqlalchemy import and_, or_, desc
import json


class UserService:
    """
    使用者服務
    User Service
    """
    
    def __init__(self, session):
        self.session = session
    
    def authenticate(self, username, password):
        """
        認證使用者
        Authenticate user
        """
        user = self.session.query(User).filter_by(
            username=username,
            is_active=True
        ).first()
        
        if user and user.verify_password(password):
            user.last_login = datetime.now()
            self.session.commit()
            # 讀取所有需要的屬性後再 expunge，避免 DetachedInstanceError
            _ = user.id
            _ = user.username
            _ = user.real_name
            _ = user.role
            _ = user.department
            _ = user.is_active
            self.session.expunge(user)
            return user
        return None
    
    def create_user(self, username, password, real_name, role='user', department=''):
        """建立新使用者"""
        try:
            # 先檢查 username 是否已存在
            existing = self.session.query(User).filter_by(username=username).first()
            if existing:
                return False, f"使用者名稱「{username}」已存在，請使用其他名稱"

            user = User(
                username=username,
                real_name=real_name,
                role=role,
                department=department
            )
            user.set_password(password)
            self.session.add(user)
            self.session.commit()
            return True, "使用者建立成功"
        except Exception as e:
            self.session.rollback()
            return False, f"建立失敗: {str(e)}"
    
    def get_user_by_id(self, user_id):
        """根據ID取得使用者"""
        return self.session.query(User).filter_by(id=user_id).first()
    
    def get_all_users(self):
        """取得所有使用者"""
        return self.session.query(User).all()
    
    def update_password(self, user_id, new_password):
        """更新密碼"""
        user = self.get_user_by_id(user_id)
        if user:
            user.set_password(new_password)
            self.session.commit()
            return True, "密碼已更新"
        return False, "使用者不存在"


class ReagentService:
    """
    試劑服務
    Reagent Service
    """
    
    def __init__(self, session):
        self.session = session
    
    def create_reagent(self, reagent_code, reagent_name, **kwargs):
        """建立試劑"""
        try:
            # 檢查代碼是否重複
            existing = self.session.query(ReagentMaster).filter_by(
                reagent_code=reagent_code
            ).first()
            if existing:
                return False, "試劑代碼已存在"
            
            reagent = ReagentMaster(
                reagent_code=reagent_code,
                reagent_name=reagent_name,
                **kwargs
            )
            self.session.add(reagent)
            self.session.commit()
            return True, f"試劑 {reagent_name} 建立成功"
        except Exception as e:
            return False, f"建立失敗: {str(e)}"
    
    def get_reagent_by_code(self, reagent_code):
        """根據代碼取得試劑"""
        return self.session.query(ReagentMaster).filter_by(
            reagent_code=reagent_code
        ).first()
    
    def get_reagent_by_id(self, reagent_id):
        """根據ID取得試劑"""
        return self.session.query(ReagentMaster).filter_by(id=reagent_id).first()
    
    def get_all_reagents(self):
        """取得所有試劑"""
        return self.session.query(ReagentMaster).filter_by(is_active=True).all()
    
    def update_reagent(self, reagent_id, **kwargs):
        """更新試劑"""
        reagent = self.get_reagent_by_id(reagent_id)
        if reagent:
            for key, value in kwargs.items():
                if hasattr(reagent, key):
                    setattr(reagent, key, value)
            reagent.updated_at = datetime.now()
            self.session.commit()
            return True, "試劑已更新"
        return False, "試劑不存在"
    
    def delete_reagent(self, reagent_id):
        """軟刪除試劑"""
        reagent = self.get_reagent_by_id(reagent_id)
        if reagent:
            reagent.is_active = False
            self.session.commit()
            return True, "試劑已刪除"
        return False, "試劑不存在"


class StockService:
    """
    庫存服務
    Stock Service
    """
    
    def __init__(self, session):
        self.session = session
    
    def stock_in(self, reagent_id, lot_number, expiry_date, quantity,
                 po_number, handler_id, remark=''):
        """
        入庫 - 每一個數量產生獨立的院內編號
        每個院內編號的 quantity = 1
        """
        try:
            is_valid, msg = ValidationHelper.validate_lot_number(lot_number)
            if not is_valid:
                return False, msg

            is_valid, msg = ValidationHelper.validate_quantity(quantity)
            if not is_valid:
                return False, msg

            is_valid, msg = ValidationHelper.validate_expiry_date(expiry_date)
            if not is_valid:
                return False, msg

            in_house_codes = []

            for _ in range(quantity):
                import time
                time.sleep(0.001)  # 確保每個編號不重複
                in_house_code = CodeGenerator.generate_in_house_code()
                in_house_codes.append(in_house_code)

                # 每一個各建一筆 StockIn，quantity=1
                stock_in_record = StockIn(
                    reagent_id=reagent_id,
                    lot_number=lot_number,
                    expiry_date=expiry_date,
                    quantity=1,
                    po_number=po_number,
                    handler_id=handler_id,
                    in_house_code=in_house_code,
                    remark=remark
                )
                self.session.add(stock_in_record)
                self.session.flush()

                # 每個院內編號各建一筆 Inventory，quantity=1
                inventory = Inventory(
                    reagent_id=reagent_id,
                    lot_number=lot_number,
                    expiry_date=expiry_date,
                    in_house_code=in_house_code,
                    current_quantity=1
                )
                self.session.add(inventory)

            self.session.commit()

            # 若試劑需要驗收，建立或取得今日的 QCBatch
            reagent = self.session.query(ReagentMaster).filter_by(id=reagent_id).first()
            if reagent and reagent.need_qc:
                today_str = datetime.now().strftime('%Y-%m-%d')
                batch = self.session.query(QCBatch).filter_by(
                    reagent_id=reagent_id,
                    lot_number=lot_number,
                    stock_in_date=today_str
                ).first()
                if not batch:
                    batch = QCBatch(
                        reagent_id=reagent_id,
                        lot_number=lot_number,
                        stock_in_date=today_str,
                        qc_levels=reagent.qc_levels,
                        is_complete=False
                    )
                    self.session.add(batch)
                    self.session.flush()
                    # 為每個 level 建立 pending 的 QCResult
                    for lv in range(1, reagent.qc_levels + 1):
                        self.session.add(QCResult(
                            batch_id=batch.id,
                            level=lv,
                            result='pending'
                        ))
                    self.session.commit()

            codes_str = ','.join(in_house_codes)
            return True, f"入庫成功 (編號: {codes_str})"

        except Exception as e:
            self.session.rollback()
            return False, f"入庫失敗: {str(e)}"
    
    def stock_out(self, in_house_code, quantity, usage_department,
                  usage_equipment, handler_id, remark=''):
        """
        出庫 - 每個院內編號 quantity=1，一次只能出庫 1 個
        """
        try:
            is_valid, msg = ValidationHelper.validate_quantity(quantity)
            if not is_valid:
                return False, msg

            stock_in = self.session.query(StockIn).filter_by(
                in_house_code=in_house_code
            ).first()

            if not stock_in:
                return False, "院內編號不存在"

            # 每個院內編號各自對應一筆 Inventory
            inventory = self.session.query(Inventory).filter_by(
                in_house_code=in_house_code
            ).first()

            if not inventory or inventory.current_quantity < quantity:
                current = inventory.current_quantity if inventory else 0
                return False, f"庫存不足 (現有: {current})"

            stock_out = StockOut(
                stock_in_id=stock_in.id,
                quantity=quantity,
                usage_department=usage_department,
                usage_equipment=usage_equipment,
                handler_id=handler_id,
                remark=remark
            )
            self.session.add(stock_out)
            inventory.current_quantity -= quantity
            self.session.commit()
            return True, "出庫成功"

        except Exception as e:
            self.session.rollback()
            return False, f"出庫失敗: {str(e)}"
    
    def get_current_inventory(self, reagent_id=None):
        """取得當前庫存"""
        query = self.session.query(Inventory)
        if reagent_id:
            query = query.filter_by(reagent_id=reagent_id)
        return query.filter(Inventory.current_quantity > 0).all()
    
    def get_stock_in_history(self, reagent_id=None, lot_number=None, days=90):
        """取得入庫歷史"""
        query = self.session.query(StockIn)
        
        if reagent_id:
            query = query.filter_by(reagent_id=reagent_id)
        
        if lot_number:
            query = query.filter_by(lot_number=lot_number)
        
        # 過去 N 天
        start_date = datetime.now() - timedelta(days=days)
        query = query.filter(StockIn.stock_in_date >= start_date)
        
        return query.order_by(desc(StockIn.stock_in_date)).all()
    
    def get_low_stock_items(self):
        """取得低庫存項目（依試劑加總後比對安全庫存）"""
        totals = {}  # reagent_id -> total_qty
        for inventory in self.session.query(Inventory).all():
            totals[inventory.reagent_id] = totals.get(inventory.reagent_id, 0) + inventory.current_quantity

        low_stock = []
        for reagent in self.session.query(ReagentMaster).filter_by(is_active=True).all():
            total = totals.get(reagent.id, 0)
            if total <= reagent.safety_stock:
                low_stock.append({
                    'reagent_name': reagent.reagent_name,
                    'lot_number': '',
                    'current': total,
                    'safety': reagent.safety_stock,
                    'shortage': reagent.safety_stock - total
                })
        return low_stock
    
    def get_expiring_items(self, days=90):
        """取得即將到期的項目"""
        expiring = []
        for inventory in self.session.query(Inventory).all():
            remaining_days = DateHelper.get_days_until_expiry(inventory.expiry_date)
            if 0 <= remaining_days <= days:
                status, color = DateHelper.get_expiry_status(inventory.expiry_date)
                expiring.append({
                    'reagent_name': inventory.reagent.reagent_name,
                    'lot_number': inventory.lot_number,
                    'expiry_date': inventory.expiry_date,
                    'remaining_days': remaining_days,
                    'quantity': inventory.current_quantity,
                    'status': status,
                    'color': color
                })
        return sorted(expiring, key=lambda x: x['remaining_days'])


class InventoryCheckService:
    """
    庫存盤點服務
    Inventory Check Service
    """
    
    def __init__(self, session):
        self.session = session
    
    def create_check_record(self, reagent_id, lot_number, actual_quantity, remark=''):
        """建立盤點紀錄"""
        try:
            # 取得系統庫存
            inventory = self.session.query(Inventory).filter_by(
                reagent_id=reagent_id,
                lot_number=lot_number
            ).first()
            
            system_quantity = inventory.current_quantity if inventory else 0
            difference = actual_quantity - system_quantity
            
            # 建立盤點紀錄
            check = InventoryCheck(
                reagent_id=reagent_id,
                lot_number=lot_number,
                system_quantity=system_quantity,
                actual_quantity=actual_quantity,
                difference=difference,
                remark=remark
            )
            self.session.add(check)
            
            # 如果有差異，更新庫存
            if difference != 0 and inventory:
                inventory.current_quantity = actual_quantity
            
            self.session.commit()
            return True, f"盤點完成 (差異: {difference:+d})"
        except Exception as e:
            self.session.rollback()
            return False, f"盤點失敗: {str(e)}"


class ScrapService:
    """
    報廢服務
    Scrap Service
    """
    
    def __init__(self, session):
        self.session = session
    
    def create_scrap_record(self, reagent_id, lot_number, quantity, reason, remark=''):
        """建立報廢紀錄"""
        try:
            is_valid, msg = ValidationHelper.validate_quantity(quantity)
            if not is_valid:
                return False, msg
            
            # 檢查是否有足夠庫存
            inventory = self.session.query(Inventory).filter_by(
                reagent_id=reagent_id,
                lot_number=lot_number
            ).first()
            
            if not inventory or inventory.current_quantity < quantity:
                return False, f"庫存不足 (現有: {inventory.current_quantity if inventory else 0})"
            
            # 建立報廢紀錄
            scrap = ScrapRecord(
                reagent_id=reagent_id,
                lot_number=lot_number,
                quantity=quantity,
                reason=reason,
                remark=remark
            )
            self.session.add(scrap)
            
            # 扣除庫存
            inventory.current_quantity -= quantity
            
            self.session.commit()
            return True, f"報廢完成 (數量: {quantity})"
        except Exception as e:
            self.session.rollback()
            return False, f"報廢失敗: {str(e)}"


class AuditLogService:
    """
    審計日誌服務
    Audit Log Service
    """
    
    def __init__(self, session):
        self.session = session
    
    def log_action(self, user_id, action, table_name=None, record_id=None, 
                   details=None, ip_address=''):
        """記錄操作"""
        try:
            log = AuditLog(
                user_id=user_id,
                action=action,
                table_name=table_name,
                record_id=record_id,
                details=details,
                ip_address=ip_address
            )
            self.session.add(log)
            self.session.commit()
        except Exception as e:
            print(f"記錄失敗: {e}")


class TraceabilityService:
    """
    追溯服務
    Traceability Service
    """
    
    def __init__(self, session):
        self.session = session
    
    def get_traceability(self, in_house_code=None, lot_number=None, reagent_name=None):
        """
        查詢追溯信息
        Query traceability information
        """
        result = {
            'stock_in_records': [],
            'stock_out_records': [],
            'inventory_checks': [],
            'scrap_records': []
        }
        
        try:
            # 查詢入庫紀錄
            if in_house_code:
                stock_in = self.session.query(StockIn).filter_by(
                    in_house_code=in_house_code
                ).first()
                if stock_in:
                    result['stock_in_records'].append({
                        'date': stock_in.stock_in_date.strftime('%Y-%m-%d'),
                        'quantity': stock_in.quantity,
                        'po_number': stock_in.po_number,
                        'handler': stock_in.handler.real_name if stock_in.handler else ''
                    })
                    
                    # 查詢出庫紀錄
                    stock_outs = self.session.query(StockOut).filter_by(
                        stock_in_id=stock_in.id
                    ).all()
                    for out in stock_outs:
                        result['stock_out_records'].append({
                            'date': out.stock_out_date.strftime('%Y-%m-%d'),
                            'quantity': out.quantity,
                            'department': out.usage_department,
                            'equipment': out.usage_equipment
                        })
            
            elif lot_number:
                # 查詢同一 LOT 號的所有記錄
                checks = self.session.query(InventoryCheck).filter_by(
                    lot_number=lot_number
                ).all()
                for check in checks:
                    result['inventory_checks'].append({
                        'date': check.check_date.strftime('%Y-%m-%d'),
                        'system_qty': check.system_quantity,
                        'actual_qty': check.actual_quantity,
                        'difference': check.difference
                    })
                
                scraps = self.session.query(ScrapRecord).filter_by(
                    lot_number=lot_number
                ).all()
                for scrap in scraps:
                    result['scrap_records'].append({
                        'date': scrap.scrap_date.strftime('%Y-%m-%d'),
                        'quantity': scrap.quantity,
                        'reason': scrap.reason
                    })
            
            return result
        except Exception as e:
            print(f"追溯查詢失敗: {e}")
            return result


class QCService:
    """驗收服務"""

    def __init__(self, session):
        self.session = session

    def get_pending_batches_by_date(self):
        """
        取得所有未完成驗收的批次，以入庫日期分組
        回傳 {date_str: [batch, ...], ...}，依日期倒序
        """
        batches = (self.session.query(QCBatch)
                   .filter_by(is_complete=False)
                   .order_by(QCBatch.stock_in_date.desc())
                   .all())
        grouped = {}
        for b in batches:
            grouped.setdefault(b.stock_in_date, []).append(b)
        return grouped

    def get_all_batches_by_date(self):
        """取得所有批次，以入庫日期分組（含已完成）"""
        batches = (self.session.query(QCBatch)
                   .order_by(QCBatch.stock_in_date.desc())
                   .all())
        grouped = {}
        for b in batches:
            grouped.setdefault(b.stock_in_date, []).append(b)
        return grouped

    def is_qc_required_for_out(self, reagent_id, lot_number, stock_in_date_str):
        """
        判斷出庫時是否需要列印驗收標籤：
        試劑需要驗收 且 對應批次尚未完成驗收
        """
        reagent = self.session.query(ReagentMaster).filter_by(id=reagent_id).first()
        if not reagent or not reagent.need_qc:
            return False
        batch = self.session.query(QCBatch).filter_by(
            reagent_id=reagent_id,
            lot_number=lot_number,
            stock_in_date=stock_in_date_str
        ).first()
        if not batch:
            return False
        return not batch.is_complete

    def save_result(self, batch_id, level, result, notes, handler_id):
        """儲存某個 level 的驗收結果"""
        try:
            qr = self.session.query(QCResult).filter_by(
                batch_id=batch_id, level=level
            ).first()
            if not qr:
                qr = QCResult(batch_id=batch_id, level=level)
                self.session.add(qr)
            qr.result       = result
            qr.notes        = notes
            qr.handler_id   = handler_id
            qr.completed_at = datetime.now()

            # 檢查是否所有 level 都完成
            batch   = self.session.query(QCBatch).filter_by(id=batch_id).first()
            results = self.session.query(QCResult).filter_by(batch_id=batch_id).all()
            if all(r.result in ('pass', 'fail') for r in results):
                batch.is_complete = True

            self.session.commit()
            return True, "儲存成功"
        except Exception as e:
            self.session.rollback()
            return False, str(e)

    def save_value(self, batch_id, level, value, handler_id):
        """儲存某個 level 的數值/文字記錄（不影響通過/不通過狀態）"""
        try:
            qr = self.session.query(QCResult).filter_by(
                batch_id=batch_id, level=level
            ).first()
            if not qr:
                qr = QCResult(batch_id=batch_id, level=level, result='pending')
                self.session.add(qr)
            qr.value = value
            self.session.commit()
            return True, "儲存成功"
        except Exception as e:
            self.session.rollback()
            return False, str(e)

    def set_batch_status(self, batch_id, result, handler_id):
        """
        設定整個批次的狀態（待驗收/通過/不通過）
        套用到該批次所有 level
        """
        try:
            batch   = self.session.query(QCBatch).filter_by(id=batch_id).first()
            if not batch:
                return False, "找不到批次"

            results = self.session.query(QCResult).filter_by(batch_id=batch_id).all()
            for r in results:
                r.result = result
                r.handler_id = handler_id
                r.completed_at = datetime.now() if result in ('pass', 'fail') else None

            batch.is_complete = (result in ('pass', 'fail'))

            self.session.commit()
            return True, "儲存成功"
        except Exception as e:
            self.session.rollback()
            return False, str(e)
