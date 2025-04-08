from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox)
import os

class LLMSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("LLM Settings")
        self.setModal(True)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # API Key input
        api_layout = QHBoxLayout()
        api_layout.addWidget(QLabel("API Key:"))
        self.api_key_input = QLineEdit(os.environ.get("LLM_API_KEY", ""))
        api_layout.addWidget(self.api_key_input)
        layout.addLayout(api_layout)

        # Provider selection
        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("LLM Provider:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["Groq", "OpenAI", "Transformers"])
        self.provider_combo.currentIndexChanged.connect(self.on_provider_changed)
        provider_layout.addWidget(self.provider_combo)
        layout.addLayout(provider_layout)

        # Model selection/input
        self.model_layout = QHBoxLayout()
        self.model_label = QLabel("Model:")
        self.model_layout.addWidget(self.model_label)
        self.model_input = QComboBox()
        self.model_layout.addWidget(self.model_input)
        layout.addLayout(self.model_layout)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)

        self.setLayout(layout)
        self.resize(400, 120)
        self.on_provider_changed(0)  # Set initial state

    def on_provider_changed(self, index):
        provider = self.provider_combo.currentText()
        if provider == "Transformers":
            self.model_input.clear()
            self.model_input.addItems(["mistralai/Mixtral-8x7B-Instruct-v0.1", "meta-llama/Llama-2-70b-chat-hf", "tiiuae/falcon-180B-chat"])
        elif provider == "OpenAI":
            self.model_input.clear()
            self.model_input.addItems(["gpt-3.5-turbo", "gpt-4-turbo", "gpt-4o"])
        else:
            self.model_input.clear()
            self.model_input.addItems(["llama-3.3-70b-versatile", "mistral-saba-24b", "gemma2-9b-it"])

    def get_settings(self):
        return {
            "api_key": self.api_key_input.text().strip(),
            "provider": self.provider_combo.currentText(),
            "model": self.model_input.currentText()
        }
