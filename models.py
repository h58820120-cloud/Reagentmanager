# models.py
import os
import sys
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import hashlib

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    real_name = Column(String(100), nullable=False)
    role = Column(String(20), default='user')
    department = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    last_login = Column(DateTime)

    audit_logs = relationship("AuditLog", back_populates="user")
    stock_in_records = relationship("StockIn", back_populates="handler")
    stock_out_records = relationship("StockOut", back_populates="handler")

    def set_password(self, password):
        self.password = hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self.password == hashlib.sha256(password.encode()).hexdigest()


class ReagentMaster(Base):
    __tablename__ = 'reagent_master'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reagent_code = Column(String(50), unique=True, nullable=False)
    reagent_name = Column(String(200), nullable=False)
    reagent_name_en = Column(String(200))
    brand = Column(String(100))
    supplier = Column(String(100))
    specification = Column(String(200))
    unit = Column(String(20))
    safety_stock = Column(Integer, default=10)
    storage_condition = Column(String(200))
    equipment = Column(String(200))
    remark = Column(Text)
    lot_start = Column(Integer, default=0)
    lot_length = Column(Integer, default=10)
    exp_start = Column(Integer, default=10)
    exp_length = Column(Integer, default=6)
    exp_format = Column(String(20), default='YYYYMMDD')
    # 驗收設定
    need_qc = Column(Boolean, default=False)
    qc_levels = Column(Integer, default=1)   # 1, 2, 3
    # 每盒/每包數量（掃描一次=一盒，自動產生 N 個院內編號）
    units_per_box = Column(Integer, default=1)
    # 保管人
    keeper_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    is_active = Column(Boolean, default=True)

    stock_in_records = relationship("StockIn", back_populates="reagent")
    barcode_records   = relationship("BarcodeRecord", back_populates="reagent")
    qc_batches        = relationship("QCBatch", back_populates="reagent")
    keeper            = relationship("User", foreign_keys=[keeper_id])


class QCBatch(Base):
    """同一天同一試劑的入庫算同一驗收批次"""
    __tablename__ = 'qc_batch'
    id            = Column(Integer, primary_key=True, autoincrement=True)
    reagent_id    = Column(Integer, ForeignKey('reagent_master.id'), nullable=False)
    lot_number    = Column(String(100), nullable=False)
    stock_in_date = Column(String(10), nullable=False)  # YYYY-MM-DD
    qc_levels     = Column(Integer, default=1)
    is_complete   = Column(Boolean, default=False)
    created_at    = Column(DateTime, default=datetime.now)

    reagent    = relationship("ReagentMaster", back_populates="qc_batches")
    qc_results = relationship("QCResult", back_populates="batch",
                              cascade="all, delete-orphan")


class QCResult(Base):
    """每個驗收批次每個 level 的結果"""
    __tablename__ = 'qc_result'
    id           = Column(Integer, primary_key=True, autoincrement=True)
    batch_id     = Column(Integer, ForeignKey('qc_batch.id'), nullable=False)
    level        = Column(Integer, nullable=False)   # 1, 2, 3
    result       = Column(String(20), default='pending')  # pending / pass / fail
    value        = Column(String(100))   # 使用者輸入的數值/文字記錄
    notes        = Column(Text)
    handler_id   = Column(Integer, ForeignKey('users.id'))
    completed_at = Column(DateTime)
    created_at   = Column(DateTime, default=datetime.now)

    batch   = relationship("QCBatch", back_populates="qc_results")
    handler = relationship("User")


class StockIn(Base):
    __tablename__ = 'stock_in'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reagent_id = Column(Integer, ForeignKey('reagent_master.id'), nullable=False)
    lot_number = Column(String(100), nullable=False)
    expiry_date = Column(String(10), nullable=False)
    quantity = Column(Integer, nullable=False)
    po_number = Column(String(50))
    handler_id = Column(Integer, ForeignKey('users.id'))
    stock_in_date = Column(DateTime, default=datetime.now)
    in_house_code = Column(String(50), unique=True)
    remark = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    reagent = relationship("ReagentMaster", back_populates="stock_in_records")
    handler = relationship("User", back_populates="stock_in_records")
    stock_out_records = relationship("StockOut", back_populates="stock_in")


class StockOut(Base):
    __tablename__ = 'stock_out'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_in_id = Column(Integer, ForeignKey('stock_in.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    usage_department = Column(String(100))
    usage_equipment = Column(String(100))
    handler_id = Column(Integer, ForeignKey('users.id'))
    stock_out_date = Column(DateTime, default=datetime.now)
    remark = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    stock_in = relationship("StockIn", back_populates="stock_out_records")
    handler = relationship("User", back_populates="stock_out_records")


class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reagent_id = Column(Integer, ForeignKey('reagent_master.id'), nullable=False)
    lot_number = Column(String(100), nullable=False)
    expiry_date = Column(String(10), nullable=False)
    in_house_code = Column(String(50), unique=True)
    current_quantity = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    reagent = relationship("ReagentMaster")


class InventoryCheck(Base):
    __tablename__ = 'inventory_check'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reagent_id = Column(Integer, ForeignKey('reagent_master.id'), nullable=False)
    lot_number = Column(String(100), nullable=False)
    system_quantity = Column(Integer)
    actual_quantity = Column(Integer)
    difference = Column(Integer)
    check_date = Column(DateTime, default=datetime.now)
    remark = Column(Text)
    created_at = Column(DateTime, default=datetime.now)


class ScrapRecord(Base):
    __tablename__ = 'scrap_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reagent_id = Column(Integer, ForeignKey('reagent_master.id'), nullable=False)
    lot_number = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    reason = Column(String(100))
    scrap_date = Column(DateTime, default=datetime.now)
    remark = Column(Text)
    created_at = Column(DateTime, default=datetime.now)


class BarcodeRecord(Base):
    __tablename__ = 'barcode_records'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reagent_id = Column(Integer, ForeignKey('reagent_master.id'), nullable=False)
    in_house_code = Column(String(50), unique=True, nullable=False)
    lot_number = Column(String(100), nullable=False)
    expiry_date = Column(String(10), nullable=False)
    code128_path = Column(String(255))
    qrcode_path = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)

    reagent = relationship("ReagentMaster", back_populates="barcode_records")


class SystemSettings(Base):
    __tablename__ = 'system_settings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(100), unique=True, nullable=False)
    value = Column(Text)

class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(50), nullable=False)
    table_name = Column(String(100))
    record_id = Column(Integer)
    details = Column(Text)
    ip_address = Column(String(15))
    timestamp = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="audit_logs")


class DatabaseManager:
    def __init__(self, db_path=None):
        try:
            from db_config import get_database_url, get_engine_kwargs, DB_MODE
            url, resolved_path = get_database_url()
            kwargs = get_engine_kwargs()
            self.db_mode = DB_MODE
        except ImportError:
            # 找不到 db_config.py 時退回本機 SQLite
            if db_path is None:
                if getattr(sys, 'frozen', False):
                    base = os.path.dirname(sys.executable)
                else:
                    base = os.path.dirname(os.path.abspath(__file__))
                db_path = os.path.join(base, 'reagent_system.db')
            url    = f'sqlite:///{db_path}'
            kwargs = {'echo': False,
                      'connect_args': {'timeout': 30, 'check_same_thread': False}}
            self.db_mode = 'sqlite_local'

        self.engine = create_engine(url, **kwargs)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            expire_on_commit=False
        )

    def init_database(self):
        Base.metadata.create_all(self.engine)

    def get_session(self):
        return self.SessionLocal()

    def create_default_admin(self):
        session = self.get_session()
        try:
            admin = session.query(User).filter_by(username='admin').first()
            if not admin:
                admin_user = User(
                    username='admin',
                    real_name='Admin',
                    role='admin',
                    department='System'
                )
                admin_user.set_password('admin123')
                session.add(admin_user)
                session.commit()
        finally:
            session.close()
