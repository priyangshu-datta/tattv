import logging
from PySide6.QtCore import QObject, Signal

class QTextEditLoggerHandler(logging.Handler, QObject):
    log_signal = Signal(str)

    def __init__(self, widget=None):
        QObject.__init__(self)
        logging.Handler.__init__(self)
        self.widget = widget
        self.log_signal.connect(self.append_log)

    def emit(self, record):
        log_entry = self.format(record)
        if self.widget:
            self.log_signal.emit(log_entry)

    def append_log(self, msg):
        if self.widget:
            self.widget.append(msg)

# Main logger setup
logger = logging.getLogger("LeadIQ+")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("[%(asctime)s] %(message)s", "%Y-%m-%d %H:%M:%S")

# File handler
# file_handler = logging.FileHandler("leadiq.log", encoding="utf-8")
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

