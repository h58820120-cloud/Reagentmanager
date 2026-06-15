# ui_login.py
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from models import DatabaseManager
from services import UserService


class LoginWindow(QDialog):
    login_success = pyqtSignal(int)

    def __init__(self, db_path='reagent_system.db'):
        super().__init__()
        self.db_path = db_path
        self.db_manager = DatabaseManager(db_path)
        self.db_manager.init_database()
        self.db_manager.create_default_admin()
        self.setWindowTitle("Medical Reagent Management System")
        self.setFixedSize(460, 320)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(48, 40, 48, 40)

        title = QLabel("醫療檢驗試劑管理系統")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        subtitle = QLabel("衛生福利部花蓮醫院")
        subtitle.setFont(QFont("Arial", 11))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #666;")
        layout.addWidget(subtitle)

        layout.addSpacing(8)

        layout.addWidget(QLabel("使用者名稱:"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("請輸入使用者名稱")
        self.username_input.setMinimumHeight(36)
        layout.addWidget(self.username_input)

        layout.addWidget(QLabel("密碼:"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("請輸入密碼")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(36)
        layout.addWidget(self.password_input)

        login_btn = QPushButton("登入")
        login_btn.setMinimumHeight(40)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover { background-color: #005A9E; }
        """)
        login_btn.clicked.connect(self.login)
        layout.addWidget(login_btn)

        hint = QLabel("預設帳號: admin  |  密碼: admin123")
        hint.setStyleSheet("color: #999; font-size: 10px;")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint)

        self.username_input.returnPressed.connect(self.login)
        self.password_input.returnPressed.connect(self.login)
        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "錯誤", "請輸入帳號和密碼")
            return

        session = self.db_manager.get_session()
        user_service = UserService(session)
        user = user_service.authenticate(username, password)

        if user:
            user_id = user.id
            session.close()
            self.login_success.emit(user_id)
            self.accept()
        else:
            session.close()
            QMessageBox.critical(self, "登入失敗", "帳號或密碼錯誤")
            self.password_input.clear()
