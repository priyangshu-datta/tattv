import logging
from utils.logger import QTextEditLoggerHandler, logger, formatter
from PySide6.QtWidgets import (
    QFileDialog, QTextEdit
)

class LogOutput(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)

    def setup_logging(self):
        qt_handler = QTextEditLoggerHandler(self)
        console_handler = logging.StreamHandler()

        qt_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.handlers.clear()
        logger.addHandler(qt_handler)
        logger.addHandler(console_handler)

    def save_logs(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Logs", "", "Text Files (*.txt)")
        if path:
            with open(path, mode='w', encoding='utf-8') as file:
                file.write(self.log_output.toPlainText())
            self.log(f"Logs saved to {path}")