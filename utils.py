# utils.py
# 工具函數
# Utility Functions

import os
import sys
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import barcode
from barcode.writer import ImageWriter
import qrcode
from PIL import Image, ImageDraw, ImageFont
import socket

# 使用執行檔所在目錄作為基礎路徑
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(os.path.dirname(sys.executable))
else:
    BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

BARCODE_DIR = BASE_DIR / 'barcodes'
BARCODE_DIR.mkdir(exist_ok=True)

LABEL_DIR = BASE_DIR / 'labels'
LABEL_DIR.mkdir(exist_ok=True)

REPORT_DIR = BASE_DIR / 'reports'
REPORT_DIR.mkdir(exist_ok=True)


def _get_font(size):
    """
    取得字型，依序嘗試：
    1. 微軟正黑體 (msjh.ttc) - Windows 中文
    2. 新細明體 (mingliu.ttc) - Windows 中文
    3. arial.ttf - 英文
    4. PIL 預設字型
    """
    candidates = [
        'msjh.ttc', 'msjhbd.ttc',
        'mingliu.ttc', 'mingliub.ttc',
        'kaiu.ttf',
        'arial.ttf', 'Arial.ttf',
        'C:/Windows/Fonts/msjh.ttc',
        'C:/Windows/Fonts/arial.ttf',
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    return ImageFont.load_default()


class BarcodeGenerator:
    """條碼生成器"""

    @staticmethod
    def generate_code128(code, filename=None):
        try:
            if filename is None:
                filename = str(BARCODE_DIR / f'code128_{code}')
            else:
                filename = str(filename).replace('.png', '')

            ean = barcode.get_barcode_class('code128')
            ean_instance = ean(code, writer=ImageWriter())
            saved = ean_instance.save(filename)
            final = saved if saved.endswith('.png') else saved + '.png'
            return final
        except Exception as e:
            print(f"Code128 生成失敗: {e}")
            return None

    @staticmethod
    def generate_qrcode(data, filename=None):
        try:
            if filename is None:
                ts = str(datetime.now().timestamp()).replace('.', '')
                filename = str(BARCODE_DIR / f'qrcode_{ts}.png')
            if isinstance(data, dict):
                data = json.dumps(data, ensure_ascii=False)
            qr = qrcode.QRCode(version=1,
                               error_correction=qrcode.constants.ERROR_CORRECT_L,
                               box_size=10, border=4)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(filename)
            return str(filename)
        except Exception as e:
            print(f"QR Code 生成失敗: {e}")
            return None

    @staticmethod
    def generate_code128(code, filename=None):
        try:
            if filename is None:
                # 不加 .png，python-barcode 會自動加
                filename = str(BARCODE_DIR / f'code128_{code}')
            else:
                # 如果傳入帶 .png，去掉再傳
                filename = str(filename).replace('.png', '')

            ean = barcode.get_barcode_class('code128')
            ean_instance = ean(code, writer=ImageWriter())
            saved = ean_instance.save(filename)  # 回傳實際存檔路徑
            # 確保回傳帶 .png 的路徑
            final = saved if saved.endswith('.png') else saved + '.png'
            return final
        except Exception as e:
            print(f"Code128 生成失敗: {e}")
            return None

    @staticmethod
    def generate_qrcode(data, filename=None):
        try:
            if filename is None:
                ts = str(datetime.now().timestamp()).replace('.', '')
                filename = str(BARCODE_DIR / f'qrcode_{ts}.png')
            if isinstance(data, dict):
                data = json.dumps(data, ensure_ascii=False)
            qr = qrcode.QRCode(version=1,
                               error_correction=qrcode.constants.ERROR_CORRECT_L,
                               box_size=10, border=4)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(filename)
            return str(filename)
        except Exception as e:
            print(f"QR Code 生成失敗: {e}")
            return None


class LabelPrinter:
    """
    標籤列印器
    Label Printer
    """
    
    @staticmethod
    def generate_label_50x30(
        reagent_name,
        lot_number,
        expiry_date,
        quantity,
        in_house_code,
        code128_path,
        qrcode_path,
        filename=None
    ):
        """
        生成 50mm × 30mm 入庫標籤
        Generate 50mm × 30mm Stock In Label
        
        標籤內容:
        - 衛生福利部花蓮醫院
        - 試劑名稱
        - LOT號
        - 有效期限
        - 庫存量
        - 院內編號
        - Code128條碼
        - QR Code
        """
        try:
            if filename is None:
                filename = str(LABEL_DIR / f'label_{in_house_code}.png')
            
            # 50mm x 30mm @ 300 DPI = 595 x 354 pixels
            width, height = 595, 354
            
            # 建立新圖像
            label = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(label)
            
            # 嘗試使用系統字體
            try:
                title_font = _get_font(20)
                text_font  = _get_font(14)
                small_font = _get_font(10)
            except Exception:
                title_font = ImageFont.load_default()
                text_font  = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # 繪製標題
            title = "衛生福利部花蓮醫院"
            draw.text((10, 10), title, fill='black', font=title_font)
            
            # 試劑信息
            y_pos = 50
            draw.text((10, y_pos), f"試劑: {reagent_name[:20]}", fill='black', font=text_font)
            y_pos += 30
            draw.text((10, y_pos), f"LOT: {lot_number}", fill='black', font=text_font)
            y_pos += 30
            draw.text((10, y_pos), f"效期: {expiry_date}", fill='black', font=text_font)
            y_pos += 30
            draw.text((10, y_pos), f"庫存: {quantity}", fill='black', font=text_font)
            y_pos += 30
            draw.text((10, y_pos), f"編號: {in_house_code}", fill='black', font=small_font)
            
            # 嵌入 Code128 條碼（如果存在）
            if code128_path and os.path.exists(code128_path):
                try:
                    barcode_img = Image.open(code128_path)
                    barcode_img = barcode_img.resize((150, 60))
                    label.paste(barcode_img, (400, 20))
                except:
                    pass
            
            # 嵌入 QR Code（如果存在）
            if qrcode_path and os.path.exists(qrcode_path):
                try:
                    qr_img = Image.open(qrcode_path)
                    qr_img = qr_img.resize((80, 80))
                    label.paste(qr_img, (480, 200))
                except:
                    pass
            
            label.save(filename)
            return str(filename)
        except Exception as e:
            print(f"標籤生成失敗: {e}")
            return None
    
    @staticmethod
    def generate_sublabel(
        reagent_name,
        source_lot,
        distribution_date,
        usage_expiry,
        operator,
        qrcode_path,
        filename=None
    ):
        """
        生成分裝子標籤
        Generate Distribution Sub-label
        """
        try:
            if filename is None:
                filename = f'{LABEL_DIR}/sublabel_{datetime.now().timestamp()}.png'
            
            # 40mm x 20mm @ 300 DPI = 472 x 236 pixels
            width, height = 472, 236
            
            label = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(label)
            
            try:
                text_font  = _get_font(12)
                small_font = _get_font(9)
            except Exception:
                text_font  = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # 繪製信息
            draw.text((10, 5), f"試劑: {reagent_name[:15]}", fill='black', font=small_font)
            draw.text((10, 25), f"源LOT: {source_lot}", fill='black', font=small_font)
            draw.text((10, 45), f"分裝: {distribution_date}", fill='black', font=small_font)
            draw.text((10, 65), f"期限: {usage_expiry}", fill='black', font=small_font)
            draw.text((10, 85), f"操作: {operator}", fill='black', font=small_font)
            
            # 嵌入 QR Code
            if qrcode_path and os.path.exists(qrcode_path):
                try:
                    qr_img = Image.open(qrcode_path)
                    qr_img = qr_img.resize((60, 60))
                    label.paste(qr_img, (380, 150))
                except:
                    pass
            
            label.save(filename)
            return str(filename)
        except Exception as e:
            print(f"子標籤生成失敗: {e}")
            return None


class DateHelper:
    """
    日期助手
    Date Helper
    """
    
    @staticmethod
    def get_days_until_expiry(expiry_date_str):
        """
        計算距離到期日期的天數
        Calculate days until expiry
        """
        try:
            expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
            today = datetime.now()
            delta = expiry_date - today
            return delta.days
        except:
            return -999
    
    @staticmethod
    def get_expiry_status(expiry_date_str):
        """
        取得過期狀態
        Get expiry status
        
        返回: (status, color)
        - 'expired': 深紅色 (已過期)
        - 'critical': 紅色 (30天內)
        - 'warning': 黃色 (90天內)
        - 'normal': 綠色 (正常)
        """
        days = DateHelper.get_days_until_expiry(expiry_date_str)
        
        if days < 0:
            return ('expired', '#8B0000')  # 深紅色
        elif days <= 30:
            return ('critical', '#FF0000')  # 紅色
        elif days <= 90:
            return ('warning', '#FFD700')  # 黃色
        else:
            return ('normal', '#00AA00')  # 綠色
    
    @staticmethod
    def format_date(date_obj):
        """格式化日期"""
        if isinstance(date_obj, str):
            return date_obj
        return date_obj.strftime('%Y-%m-%d') if date_obj else ''


class CodeGenerator:
    """
    代碼生成器
    Code Generator
    """
    
    @staticmethod
    def generate_in_house_code():
        """
        生成院內編號
        Generate In-house Code
        
        格式: R + YYYYMMDD + 0001
        例如: R202608010001
        """
        today = datetime.now().strftime('%Y%m%d')
        timestamp = str(int(datetime.now().timestamp() * 1000000) % 10000).zfill(4)
        return f'R{today}{timestamp}'
    
    @staticmethod
    def generate_hash(text):
        """生成 SHA256 雜湊"""
        return hashlib.sha256(text.encode()).hexdigest()


class NetworkHelper:
    """
    網路助手
    Network Helper
    """
    
    @staticmethod
    def get_local_ip():
        """
        取得本機 IP 位址
        Get local IP address
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return '127.0.0.1'


class ValidationHelper:
    """
    驗證助手
    Validation Helper
    """
    
    @staticmethod
    def validate_lot_number(lot_number):
        """驗證 LOT 號"""
        if not lot_number or len(lot_number.strip()) == 0:
            return False, "LOT號不能為空"
        return True, ""
    
    @staticmethod
    def validate_quantity(quantity):
        """驗證數量"""
        try:
            qty = int(quantity)
            if qty <= 0:
                return False, "數量必須大於0"
            return True, ""
        except:
            return False, "數量必須是整數"
    
    @staticmethod
    def validate_expiry_date(expiry_date):
        """驗證到期日期"""
        try:
            datetime.strptime(expiry_date, '%Y-%m-%d')
            return True, ""
        except:
            return False, "日期格式應為 YYYY-MM-DD"
    
    @staticmethod
    def validate_password(password):
        """驗證密碼"""
        if len(password) < 6:
            return False, "密碼長度至少6個字符"
        return True, ""


if __name__ == '__main__':
    # 測試條碼生成
    print("測試 Code128 條碼生成...")
    code128_path = BarcodeGenerator.generate_code128("R202608010001")
    print(f"Code128 路徑: {code128_path}")
    
    print("測試 QR Code 生成...")
    qr_data = {
        "id": "R202608010001",
        "name": "葡萄糖",
        "lot": "LOT001",
        "exp": "2027-12-31"
    }
    qrcode_path = BarcodeGenerator.generate_qrcode(qr_data)
    print(f"QR Code 路徑: {qrcode_path}")
    
    print("測試標籤生成...")
    label_path = LabelPrinter.generate_label_50x30(
        reagent_name="葡萄糖",
        lot_number="LOT001",
        expiry_date="2027-12-31",
        quantity=100,
        in_house_code="R202608010001",
        code128_path=code128_path,
        qrcode_path=qrcode_path
    )
    print(f"標籤路徑: {label_path}")
    
    print("測試完成")
