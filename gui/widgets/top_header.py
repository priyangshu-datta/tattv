import os
from PySide6.QtWidgets import QWidget, QPushButton, QLabel, QHBoxLayout
from PySide6.QtCore import Qt
from gui.app import LLMSettingsDialog

class HeaderBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.status_light = QLabel("●")
        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.clicked.connect(self.open_settings_dialog)
        # Styles
        self.status_light.setStyleSheet("color: green; font-size: 20px;")
        self.settings_btn.setStyleSheet("padding: 1px;")
        self.settings_btn.setToolTip("LLM Settings")
        # Layout
        layout = QHBoxLayout()
        layout.addWidget(self.status_light)
        layout.addStretch()
        layout.addWidget(self.settings_btn, alignment=Qt.AlignRight)
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

    def set_status(self, status):
        color = "red" if status == "busy" else "green"
        self.status_light.setStyleSheet(f"color: {color}; font-size: 20px;")

    def open_settings_dialog(self):
        dialog = LLMSettingsDialog(self)
        if dialog.exec():  # Only get values if user accepted
            settings = dialog.get_settings()
            os.environ["LLM_API_KEY"] = settings["api_key"]
            self.llm_client = settings["provider"]
            self.model_name = settings["model"]

    def llm_settings(self):
        return (self.llm_client, self.model_name)