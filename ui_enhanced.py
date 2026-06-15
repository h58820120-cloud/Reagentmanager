# ui_enhanced.py
# 增強的 UI 設計 - 融合 Frontend Design Skill
# Enhanced UI Design with Frontend Design Skill Integration

"""
基於 Anthropic frontend-design skill 的最佳實踐：
- 設計系統原則
- 視覺層級
- 響應式佈局
- 可訪問性 (A11y)
- 用戶體驗優化
"""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QComboBox,
    QSpinBox, QDateEdit, QTextEdit, QDialog, QMessageBox,
    QTabWidget, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt, QDate, QSize, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QIcon, QPixmap, QPalette, QBrush
from PyQt6.QtCore import Qt as QtCore


class DesignSystem:
    """
    設計系統
    Design System - 遵循 frontend-design skill 原則
    """
    
    # 色彩調色板 (HIS/LIS 專業風格)
    COLORS = {
        # 主色調
        'primary': '#0078D4',      # 藍色 - 主操作
        'primary_hover': '#005A9E',
        'primary_active': '#003E7A',
        
        # 成功色
        'success': '#107C10',      # 綠色 - 成功/正常
        'success_light': '#D4EDDA',
        
        # 警示色
        'warning': '#FFB900',      # 黃色 - 警示
        'warning_light': '#FFF3CD',
        
        # 危險色
        'danger': '#D13438',       # 紅色 - 危險
        'danger_light': '#F8D7DA',
        'danger_dark': '#8B0000',  # 深紅 - 已過期
        
        # 信息色
        'info': '#0078D4',
        'info_light': '#D1E7F7',
        
        # 中性色
        'light': '#F0F0F0',        # 淺灰
        'light_gray': '#E5E5E5',
        'medium_gray': '#999999',
        'dark_gray': '#666666',
        'dark': '#333333',         # 深灰
        
        # 邊框和背景
        'border': '#CCCCCC',
        'background': '#FFFFFF',
        'background_alt': '#F5F5F5',
    }
    
    # 排版系統 (Typography)
    TYPOGRAPHY = {
        'h1': {'size': 28, 'weight': 'bold', 'family': 'Arial'},      # 主標題
        'h2': {'size': 24, 'weight': 'bold', 'family': 'Arial'},      # 副標題
        'h3': {'size': 18, 'weight': 'bold', 'family': 'Arial'},      # 三級標題
        'body': {'size': 12, 'weight': 'normal', 'family': 'Arial'},  # 正文
        'label': {'size': 11, 'weight': 'normal', 'family': 'Arial'}, # 標籤
        'caption': {'size': 10, 'weight': 'normal', 'family': 'Arial'},# 說明文字
        'mono': {'size': 11, 'weight': 'normal', 'family': 'Courier'},# 等寬字體
    }
    
    # 間距系統 (Spacing Scale)
    SPACING = {
        'xs': 4,      # 超小
        'sm': 8,      # 小
        'md': 16,     # 中
        'lg': 24,     # 大
        'xl': 32,     # 超大
        'xxl': 48,    # 特大
    }
    
    # 圓角系統 (Border Radius)
    RADIUS = {
        'none': 0,
        'sm': 4,
        'md': 6,
        'lg': 8,
        'full': 999,
    }
    
    # 陰影系統 (Shadows)
    SHADOWS = {
        'sm': '0 1px 2px rgba(0,0,0,0.05)',
        'md': '0 4px 6px rgba(0,0,0,0.1)',
        'lg': '0 10px 15px rgba(0,0,0,0.1)',
        'xl': '0 20px 25px rgba(0,0,0,0.15)',
    }
    
    # 尺寸系統 (Size Scale)
    SIZES = {
        'button_sm': (60, 32),
        'button_md': (80, 40),
        'button_lg': (120, 48),
        'input': (200, 40),
        'card': (300, 250),
    }

    @staticmethod
    def create_font(style='body'):
        """建立設計系統字體"""
        config = DesignSystem.TYPOGRAPHY.get(style, DesignSystem.TYPOGRAPHY['body'])
        font = QFont(config['family'], config['size'])
        if config['weight'] == 'bold':
            font.setBold(True)
        return font
    
    @staticmethod
    def create_button_style(style_type='primary'):
        """建立按鈕樣式 (遵循 frontend-design skill)"""
        colors = DesignSystem.COLORS
        
        styles = {
            'primary': f"""
                QPushButton {{
                    background-color: {colors['primary']};
                    color: white;
                    border: none;
                    border-radius: {DesignSystem.RADIUS['md']}px;
                    padding: 10px 16px;
                    font-weight: bold;
                    font-size: 11px;
                }}
                QPushButton:hover {{
                    background-color: {colors['primary_hover']};
                }}
                QPushButton:pressed {{
                    background-color: {colors['primary_active']};
                }}
                QPushButton:disabled {{
                    background-color: {colors['light_gray']};
                    color: {colors['dark_gray']};
                }}
            """,
            
            'success': f"""
                QPushButton {{
                    background-color: {colors['success']};
                    color: white;
                    border: none;
                    border-radius: {DesignSystem.RADIUS['md']}px;
                    padding: 10px 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #0B6104;
                }}
                QPushButton:pressed {{
                    background-color: #0A5A03;
                }}
            """,
            
            'danger': f"""
                QPushButton {{
                    background-color: {colors['danger']};
                    color: white;
                    border: none;
                    border-radius: {DesignSystem.RADIUS['md']}px;
                    padding: 10px 16px;
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: #A4373A;
                }}
                QPushButton:pressed {{
                    background-color: #7A2A2D;
                }}
            """,
            
            'secondary': f"""
                QPushButton {{
                    background-color: {colors['light']};
                    color: {colors['dark']};
                    border: 1px solid {colors['border']};
                    border-radius: {DesignSystem.RADIUS['md']}px;
                    padding: 10px 16px;
                    font-weight: normal;
                }}
                QPushButton:hover {{
                    background-color: {colors['light_gray']};
                    border: 1px solid {colors['dark_gray']};
                }}
                QPushButton:pressed {{
                    background-color: {colors['light_gray']};
                }}
            """,
        }
        
        return styles.get(style_type, styles['primary'])
    
    @staticmethod
    def create_input_style():
        """建立輸入框樣式"""
        colors = DesignSystem.COLORS
        return f"""
            QLineEdit {{
                border: 1px solid {colors['border']};
                border-radius: {DesignSystem.RADIUS['md']}px;
                padding: 8px 12px;
                background-color: {colors['background']};
                selection-background-color: {colors['primary']};
                font-size: 11px;
            }}
            QLineEdit:focus {{
                border: 2px solid {colors['primary']};
                padding: 7px 11px;
            }}
            QLineEdit:disabled {{
                background-color: {colors['background_alt']};
                color: {colors['dark_gray']};
            }}
        """
    
    @staticmethod
    def create_card_style():
        """建立卡片容器樣式"""
        colors = DesignSystem.COLORS
        return f"""
            QFrame {{
                background-color: {colors['background']};
                border: 1px solid {colors['border']};
                border-radius: {DesignSystem.RADIUS['lg']}px;
                padding: {DesignSystem.SPACING['md']}px;
            }}
        """


class ColorStatus:
    """
    狀態顏色映射 (遵循 frontend-design 的視覺層級)
    Color Status Mapping - Visual Hierarchy
    """
    
    # 過期狀態顏色
    EXPIRY_COLORS = {
        'normal': DesignSystem.COLORS['success'],      # 正常 - 綠色
        'warning': DesignSystem.COLORS['warning'],     # 警示 - 黃色
        'critical': DesignSystem.COLORS['danger'],     # 警急 - 紅色
        'expired': DesignSystem.COLORS['danger_dark'], # 已過期 - 深紅
    }
    
    # 操作狀態顏色
    ACTION_COLORS = {
        'create': DesignSystem.COLORS['success'],
        'update': DesignSystem.COLORS['info'],
        'delete': DesignSystem.COLORS['danger'],
        'warning': DesignSystem.COLORS['warning'],
        'error': DesignSystem.COLORS['danger'],
        'success': DesignSystem.COLORS['success'],
    }


class AccessibilityHelper:
    """
    無障礙訪問助手
    Accessibility Helper - A11y Support
    """
    
    @staticmethod
    def create_accessible_button(text, tooltip='', shortcut=''):
        """建立可訪問的按鈕"""
        btn = QPushButton(text)
        if tooltip:
            btn.setToolTip(tooltip)
        if shortcut:
            btn.setShortcut(shortcut)
        btn.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        return btn
    
    @staticmethod
    def create_accessible_label(text, for_widget=None):
        """建立可訪問的標籤"""
        label = QLabel(text)
        if for_widget:
            label.setBuddy(for_widget)
        return label
    
    @staticmethod
    def enhance_contrast(widget, foreground, background):
        """增強對比度"""
        palette = widget.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(background))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(foreground))
        widget.setPalette(palette)


class ResponsiveLayout:
    """
    響應式佈局
    Responsive Layout - Mobile/Desktop friendly
    """
    
    @staticmethod
    def create_responsive_grid(items, columns_desktop=4, columns_tablet=2, columns_mobile=1):
        """建立響應式網格"""
        # 實現響應式佈局的邏輯
        # 實際應用中需要檢測螢幕寬度並動態調整
        layout = QHBoxLayout()
        
        for i, item in enumerate(items):
            layout.addWidget(item)
            if (i + 1) % columns_desktop == 0:
                layout.addStretch()
        
        return layout


class EnhancedUIComponent:
    """
    增強的 UI 組件
    Enhanced UI Components with Design System
    """
    
    @staticmethod
    def create_stat_card(label, value, color=None, icon=None):
        """建立統計卡片"""
        if color is None:
            color = DesignSystem.COLORS['primary']
        
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
                padding: 20px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        # 標籤
        label_widget = QLabel(label)
        label_widget.setFont(DesignSystem.create_font('label'))
        label_widget.setStyleSheet("color: white;")
        layout.addWidget(label_widget)
        
        # 值
        value_widget = QLabel(str(value))
        value_widget.setFont(DesignSystem.create_font('h1'))
        value_widget.setStyleSheet("color: white;")
        layout.addWidget(value_widget)
        
        card.setLayout(layout)
        return card
    
    @staticmethod
    def create_status_badge(text, status='normal'):
        """建立狀態徽章"""
        colors = ColorStatus.EXPIRY_COLORS
        color = colors.get(status, colors['normal'])
        
        badge = QLabel(text)
        badge.setStyleSheet(f"""
            QLabel {{
                background-color: {color};
                color: white;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 10px;
                font-weight: bold;
            }}
        """)
        badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return badge
    
    @staticmethod
    def create_alert(message, alert_type='info'):
        """建立警示框"""
        colors = ColorStatus.ACTION_COLORS
        bg_color = colors.get(alert_type, colors['info'])
        
        # 淡色背景
        light_bg = {
            'success': DesignSystem.COLORS['success_light'],
            'warning': DesignSystem.COLORS['warning_light'],
            'danger': DesignSystem.COLORS['danger_light'],
            'info': DesignSystem.COLORS['info_light'],
        }
        
        alert = QFrame()
        alert.setStyleSheet(f"""
            QFrame {{
                background-color: {light_bg.get(alert_type, light_bg['info'])};
                border-left: 4px solid {bg_color};
                border-radius: 4px;
                padding: 12px 16px;
            }}
        """)
        
        layout = QVBoxLayout()
        
        message_label = QLabel(message)
        message_label.setStyleSheet(f"color: {bg_color}; font-weight: bold;")
        layout.addWidget(message_label)
        
        alert.setLayout(layout)
        return alert


# 使用示例
if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    # 建立測試窗口
    window = QWidget()
    window.setWindowTitle("設計系統演示")
    window.setGeometry(100, 100, 600, 400)
    
    layout = QVBoxLayout()
    
    # 統計卡片
    card1 = EnhancedUIComponent.create_stat_card("庫存總數", "250", DesignSystem.COLORS['primary'])
    card2 = EnhancedUIComponent.create_stat_card("今日入庫", "15", DesignSystem.COLORS['success'])
    card3 = EnhancedUIComponent.create_stat_card("快過期", "5", DesignSystem.COLORS['warning'])
    
    cards_layout = QHBoxLayout()
    cards_layout.addWidget(card1)
    cards_layout.addWidget(card2)
    cards_layout.addWidget(card3)
    
    layout.addLayout(cards_layout)
    
    # 狀態徽章
    badges_layout = QHBoxLayout()
    badges_layout.addWidget(EnhancedUIComponent.create_status_badge("正常", "normal"))
    badges_layout.addWidget(EnhancedUIComponent.create_status_badge("警示", "warning"))
    badges_layout.addWidget(EnhancedUIComponent.create_status_badge("警急", "critical"))
    badges_layout.addWidget(EnhancedUIComponent.create_status_badge("過期", "expired"))
    
    layout.addLayout(badges_layout)
    
    # 警示框
    layout.addWidget(EnhancedUIComponent.create_alert("操作成功!", "success"))
    layout.addWidget(EnhancedUIComponent.create_alert("請注意", "warning"))
    layout.addWidget(EnhancedUIComponent.create_alert("發生錯誤", "danger"))
    
    window.setLayout(layout)
    window.show()
    
    sys.exit(app.exec())
