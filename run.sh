#!/bin/bash
# 醫療檢驗試劑管理系統 - Linux/macOS 執行腳本
# Medical Laboratory Reagent Management System - Linux/macOS Run Script

set -e

# 取得腳本所在目錄
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║   醫療檢驗試劑管理系統                                  ║"
echo "║   Medical Laboratory Reagent Management System         ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# 檢查 Python 是否已安裝
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 錯誤：找不到 Python 3${NC}"
    echo ""
    echo "請先安裝 Python 3.12 或以上版本"
    echo ""
    echo "macOS:"
    echo "  brew install python@3.12"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt-get install python3.12 python3.12-venv"
    echo ""
    exit 1
fi

# 檢查 Python 版本
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION 已安裝"
echo ""

# 檢查虛擬環境
if [ ! -d "venv" ]; then
    echo "📦 建立 Python 虛擬環境..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ 虛擬環境建立失敗${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓${NC} 虛擬環境建立完成"
    echo ""
fi

# 啟用虛擬環境
echo "📦 啟用虛擬環境..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ 啟用虛擬環境失敗${NC}"
    exit 1
fi
echo -e "${GREEN}✓${NC} 虛擬環境已啟用"
echo ""

# 檢查並安裝依賴
echo "📦 檢查依賴套件..."
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo "📦 正在安裝依賴套件..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ 依賴套件安裝失敗${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓${NC} 依賴套件安裝完成"
    echo ""
fi

# 初始化資料庫
if [ ! -f "reagent_system.db" ]; then
    echo "💾 初始化資料庫..."
    python3 init_database.py --init
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ 資料庫初始化失敗${NC}"
        exit 1
    fi
    echo ""
fi

# 執行應用程式
echo -e "${GREEN}✅ 啟動應用程式...${NC}"
echo ""

python3 main.py
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ 應用程式執行出錯${NC}"
    exit 1
fi

deactivate
