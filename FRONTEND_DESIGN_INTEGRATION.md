# FRONTEND_DESIGN_INTEGRATION.md
# Frontend Design Skill 整合指南
# Frontend Design Skill Integration Guide

## 📚 概述

本文檔說明如何將 Anthropic 的 **frontend-design skill** 集成到醫療檢驗試劑管理系統中。

來源: https://github.com/anthropics/skills/tree/main/skills/frontend-design

---

## 🎨 設計系統原則

### 1. 設計層級 (Design System)

遵循 frontend-design skill 的完整設計系統實現：

```python
# 色彩系統
Colors: Primary, Success, Warning, Danger, Neutral

# 排版系統
Typography: H1-H3, Body, Label, Caption, Mono

# 間距系統
Spacing: xs (4px) → xxl (48px)

# 圓角系統
Radius: none, sm, md, lg, full

# 陰影系統
Shadows: sm, md, lg, xl

# 尺寸系統
Sizes: Button, Input, Card 預設尺寸
```

### 2. 視覺層級 (Visual Hierarchy)

**優先級順序:**
1. **最重要**: 主操作按鈕 (Primary Blue)
2. **重要**: 成功/警示 (Green/Yellow)
3. **警告**: 危險操作 (Red)
4. **信息**: 次要內容 (Gray)

### 3. 顏色使用指南

```
🔵 藍色 (#0078D4)     → 主要操作、超連結、主題色
🟢 綠色 (#107C10)     → 成功、正常狀態、確認
🟡 黃色 (#FFB900)     → 警示、注意、即將發生
🔴 紅色 (#D13438)     → 錯誤、刪除、危險
⚪ 灰色 (#999999)     → 禁用、中性、次要
```

---

## 🔧 實現要點

### 已集成的功能

#### 1. **設計系統類 (DesignSystem)**
```python
# 中央化配置
COLORS    # 調色板
TYPOGRAPHY  # 字體系統
SPACING   # 間距尺度
RADIUS    # 圓角尺度
SHADOWS   # 陰影效果
SIZES     # 元件尺寸
```

#### 2. **顏色狀態映射 (ColorStatus)**
```python
# 過期狀態
EXPIRY_COLORS = {
    'normal': 綠色,
    'warning': 黃色,
    'critical': 紅色,
    'expired': 深紅
}

# 操作狀態
ACTION_COLORS = {
    'create': 綠色,
    'update': 藍色,
    'delete': 紅色,
    'warning': 黃色,
    'error': 紅色,
    'success': 綠色
}
```

#### 3. **無障礙訪問 (A11y)**
```python
# 可訪問的元件
- create_accessible_button()
- create_accessible_label()
- enhance_contrast()

# 支援功能
- 鍵盤導航
- 螢幕閱讀器友好
- 高對比度模式
```

#### 4. **響應式佈局**
```python
# 自適應設計
create_responsive_grid(
    items,
    columns_desktop=4,
    columns_tablet=2,
    columns_mobile=1
)
```

---

## 📋 UI 組件最佳實踐

### 1. 按鈕樣式

```python
# Primary 按鈕 - 主要操作
btn = QPushButton("入庫")
btn.setStyleSheet(DesignSystem.create_button_style('primary'))

# Success 按鈕 - 成功操作
btn = QPushButton("確認")
btn.setStyleSheet(DesignSystem.create_button_style('success'))

# Danger 按鈕 - 危險操作
btn = QPushButton("刪除")
btn.setStyleSheet(DesignSystem.create_button_style('danger'))

# Secondary 按鈕 - 次要操作
btn = QPushButton("取消")
btn.setStyleSheet(DesignSystem.create_button_style('secondary'))
```

### 2. 輸入框樣式

```python
# 統一的輸入框樣式
input_field = QLineEdit()
input_field.setStyleSheet(DesignSystem.create_input_style())

# 焦點狀態會自動改變邊框顏色
```

### 3. 卡片容器

```python
# 統一的卡片樣式
card = QFrame()
card.setStyleSheet(DesignSystem.create_card_style())
```

### 4. 統計卡片

```python
# 彩色統計卡片
card = EnhancedUIComponent.create_stat_card(
    label="庫存總數",
    value="250",
    color=DesignSystem.COLORS['primary']
)
```

### 5. 狀態徽章

```python
# 顯示狀態的徽章
badge = EnhancedUIComponent.create_status_badge(
    text="正常",
    status="normal"  # normal, warning, critical, expired
)
```

### 6. 警示框

```python
# 不同類型的警示
success_alert = EnhancedUIComponent.create_alert(
    message="操作成功!",
    alert_type="success"  # success, warning, danger, info
)
```

---

## 🎯 整合到現有系統

### 步驟 1: 導入新模組

在 `ui_main.py` 中添加：

```python
from ui_enhanced import (
    DesignSystem,
    ColorStatus,
    AccessibilityHelper,
    ResponsiveLayout,
    EnhancedUIComponent
)
```

### 步驟 2: 替換現有樣式

**之前:**
```python
btn = QPushButton("入庫")
btn.setStyleSheet("""
    QPushButton {
        background-color: #0078D4;
        color: white;
        ...
    }
""")
```

**之後:**
```python
btn = QPushButton("入庫")
btn.setStyleSheet(DesignSystem.create_button_style('primary'))
```

### 步驟 3: 更新首頁儀表板

在 `create_dashboard_tab()` 中使用：

```python
# 使用增強的統計卡片
card1 = EnhancedUIComponent.create_stat_card(
    "庫存總數", "250", DesignSystem.COLORS['primary']
)
card2 = EnhancedUIComponent.create_stat_card(
    "今日入庫", "15", DesignSystem.COLORS['success']
)
card3 = EnhancedUIComponent.create_stat_card(
    "快過期", "5", DesignSystem.COLORS['warning']
)
card4 = EnhancedUIComponent.create_stat_card(
    "低庫存", "3", DesignSystem.COLORS['danger']
)

stats_layout = QHBoxLayout()
stats_layout.addWidget(card1)
stats_layout.addWidget(card2)
stats_layout.addWidget(card3)
stats_layout.addWidget(card4)
layout.addLayout(stats_layout)
```

### 步驟 4: 更新表格行顏色

在庫存查詢中使用狀態顏色：

```python
# 根據過期狀態著色
status, color = DateHelper.get_expiry_status(item.expiry_date)
status_item = QTableWidgetItem(status)
status_item.setBackground(QColor(ColorStatus.EXPIRY_COLORS[status]))
table.setItem(row, col, status_item)
```

### 步驟 5: 添加警示框

在操作結果後顯示：

```python
# 成功的操作
if success:
    alert = EnhancedUIComponent.create_alert(
        "入庫成功！",
        "success"
    )
    layout.addWidget(alert)

# 失敗的操作
if not success:
    alert = EnhancedUIComponent.create_alert(
        f"入庫失敗: {error_msg}",
        "danger"
    )
    layout.addWidget(alert)
```

---

## 🎨 自訂設計系統

### 修改顏色

```python
# 在 DesignSystem 類中修改
COLORS = {
    'primary': '#YOUR_COLOR',
    'success': '#YOUR_COLOR',
    # ...
}
```

### 修改字體

```python
# 在 TYPOGRAPHY 中修改
TYPOGRAPHY = {
    'h1': {'size': 28, 'weight': 'bold', 'family': '您的字體'},
    # ...
}
```

### 修改間距

```python
# 在 SPACING 中修改
SPACING = {
    'md': 16,  # 改為您喜歡的值
    # ...
}
```

---

## ♿ 無障礙訪問檢查清單

- [x] **鍵盤導航** - 所有功能都可用 Tab 鍵訪問
- [x] **焦點指示** - 清晰的焦點輪廓
- [x] **顏色對比** - 符合 WCAG AA 標準
- [x] **按鈕標籤** - 所有按鈕都有清晰文本
- [x] **表格標題** - 表格有合適的標題
- [x] **錯誤訊息** - 清晰且易於理解
- [x] **字體大小** - 至少 11px，易於閱讀

### 增強對比度

```python
# 如需更高對比度
AccessibilityHelper.enhance_contrast(
    widget=my_label,
    foreground='#000000',  # 黑色
    background='#FFFFFF'   # 白色
)
```

---

## 📱 響應式設計

### 桌面版本 (1920×1080)
- 4 列統計卡片
- 完整的資訊顯示
- 多面板佈局

### 平板版本 (1024×768)
- 2 列統計卡片
- 簡化的資訊顯示

### 手機版本 (480×800)
- 1 列統計卡片
- 堆疊佈局

```python
# 實現響應式佈局
layout = ResponsiveLayout.create_responsive_grid(
    items=[card1, card2, card3, card4],
    columns_desktop=4,
    columns_tablet=2,
    columns_mobile=1
)
```

---

## 🧪 測試設計系統

執行 `ui_enhanced.py` 查看設計系統演示：

```bash
python ui_enhanced.py
```

這會顯示：
- 統計卡片示例
- 狀態徽章示例
- 警示框示例
- 顏色方案演示

---

## 📚 參考資源

### Anthropic Frontend Design Skill
- 來源: https://github.com/anthropics/skills/tree/main/skills/frontend-design
- 原則: 設計系統、視覺層級、可訪問性
- 實踐: 響應式設計、顏色系統、排版

### 相關標準
- WCAG 2.1 (無障礙訪問)
- Material Design (Google)
- Fluent Design (Microsoft)

---

## 💡 最佳實踐總結

### ✅ 做這些事

```python
# ✅ 使用設計系統顏色
color = DesignSystem.COLORS['primary']

# ✅ 使用設計系統字體
font = DesignSystem.create_font('h1')

# ✅ 使用預定義樣式
style = DesignSystem.create_button_style('primary')

# ✅ 遵循視覺層級
# 最重要 → 最不重要

# ✅ 測試無障礙訪問
# 使用鍵盤導航
```

### ❌ 避免這些事

```python
# ❌ 硬編碼顏色
color = '#0078D4'

# ❌ 內聯樣式
setStyleSheet("QPushButton { ... }")

# ❌ 不一致的設計
color1 = '#0078D4'
color2 = '#005A9E'
color3 = '#003E7A'  # 相同的顏色用不同值

# ❌ 忽視對比度
# 淺灰文本在白色背景上
```

---

## 🔄 持續維護

### 當您需要修改設計時

1. **更新 DesignSystem 類** - 單一真實來源
2. **驗證所有組件** - 確保一致性
3. **測試無障礙訪問** - 色盲模式、螢幕閱讀器
4. **檢查響應式** - 不同螢幕尺寸
5. **更新文檔** - 保持同步

### 未來的擴展

```python
# 暗色模式支援
class DarkTheme:
    COLORS = {...}

# 主題切換
def switch_theme(theme='light'):
    # 應用不同的設計系統
```

---

## 📞 支援

如有問題或需要進一步的幫助：

1. 參考 `README.md` 的設計部分
2. 查看 `ui_enhanced.py` 的代碼示例
3. 運行 `python ui_enhanced.py` 查看演示
4. 參考 Anthropic 的原始 frontend-design skill

---

**版本**: 1.0.0  
**日期**: 2024-08-01  
**適用系統**: 醫療檢驗試劑管理系統 v1.0.0
