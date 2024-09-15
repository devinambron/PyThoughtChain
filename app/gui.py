# app/gui.py

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QScrollArea, QSizePolicy, QSpacerItem
)
from PySide6.QtGui import QColor, QPalette, QFont, QPixmap
from PySide6.QtCore import Qt, Signal, Slot, QTimer

from app.services.chat_service import ChatService

class MessageBubble(QWidget):
    def __init__(self, sender, message, parent=None):
        super().__init__(parent)
        self.sender = sender
        self.message = message
        self.setup_ui()

    def setup_ui(self):
        print(f"Setting up MessageBubble for {self.sender}")  # Debugging statement
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignLeft if self.sender == "assistant" else Qt.AlignRight)
        layout.setContentsMargins(10, 5, 10, 5)

        if self.sender == "assistant":
            avatar = QLabel()
            try:
                avatar_pixmap = QPixmap("path_to_assistant_avatar.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                if avatar_pixmap.isNull():
                    raise FileNotFoundError("Assistant avatar image not found.")
                avatar.setPixmap(avatar_pixmap)
            except Exception as e:
                print(f"Error loading assistant avatar: {e}")
            avatar.setFixedSize(40, 40)
            layout.addWidget(avatar)

        bubble = QLabel(self.message)
        bubble.setWordWrap(True)
        bubble.setFont(QFont("Helvetica Neue", 14))
        bubble.setStyleSheet(self.get_style())
        bubble.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        bubble.setContentsMargins(10, 10, 10, 10)
        bubble.setMaximumWidth(400)

        layout.addWidget(bubble)

        if self.sender == "user":
            avatar = QLabel()
            try:
                avatar_pixmap = QPixmap("path_to_user_avatar.png").scaled(40, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                if avatar_pixmap.isNull():
                    raise FileNotFoundError("User avatar image not found.")
                avatar.setPixmap(avatar_pixmap)
            except Exception as e:
                print(f"Error loading user avatar: {e}")
            avatar.setFixedSize(40, 40)
            layout.addWidget(avatar)

        self.setLayout(layout)

    def get_style(self):
        if self.sender == "user":
            return """
                QLabel {
                    background-color: #0B93F6;
                    color: white;
                    border-radius: 15px;
                    padding: 10px;
                }
            """
        else:
            return """
                QLabel {
                    background-color: #E5E5EA;
                    color: black;
                    border-radius: 15px;
                    padding: 10px;
                }
            """

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyThoughtChain")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()
        self.chat_service = ChatService()
        self.chat_service.assistant_message.connect(self.add_assistant_message)
        self.chat_service.error_message.connect(self.add_error_message)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Chat display area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        scroll_area_widget = QWidget()
        self.chat_layout = QVBoxLayout(scroll_area_widget)
        self.chat_layout.setAlignment(Qt.AlignTop)
        scroll_area.setWidget(scroll_area_widget)
        main_layout.addWidget(scroll_area)

        # Add a single spacer at the end
        self.chat_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Input area
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type a message")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 20px;
                padding: 10px 15px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #0B93F6;
            }
        """)
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #0B93F6;
                color: white;
                border-radius: 20px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0A84D0;
            }
            QPushButton:pressed {
                background-color: #0A6FBF;
            }
        """)
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.send_button)
        main_layout.addLayout(input_layout)

        # Connect signals
        self.send_button.clicked.connect(self.send_message)
        self.input_field.returnPressed.connect(self.send_message)

        # Set the window's background to a semi-transparent dark color
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1C1C1E;
            }
        """)

    def send_message(self):
        user_message = self.input_field.text().strip()
        if user_message:
            self.add_message("user", user_message)
            self.chat_service.process_user_message(user_message)
            self.input_field.clear()

    def add_message(self, sender, message):
        print(f"Adding message from {sender}: {message}")  # Debugging statement
        message_bubble = MessageBubble(sender, message)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, message_bubble)  # Insert before spacer
        QTimer.singleShot(100, self.scroll_to_bottom)

    @Slot(str)
    def add_assistant_message(self, message):
        self.add_message("assistant", message)

    @Slot(str)
    def add_error_message(self, message):
        error_label = QLabel(message)
        error_label.setStyleSheet("""
            QLabel {
                color: #FF0000;
                font-weight: bold;
            }
        """)
        self.chat_layout.insertWidget(self.chat_layout.count() - 1, error_label)  # Insert before spacer
        QTimer.singleShot(100, self.scroll_to_bottom)

    def scroll_to_bottom(self):
        scroll_area = self.centralWidget().findChild(QScrollArea)
        scroll_bar = scroll_area.verticalScrollBar()
        scroll_bar.setValue(scroll_bar.maximum())

def run_gui():
    app = QApplication([])
    window = ChatWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    run_gui()