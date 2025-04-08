from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QAbstractItemView, QHeaderView, QCheckBox, QFileDialog
)
import csv

class URLInputTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(0, 2, parent)
        self.setHorizontalHeaderLabels(["URL", "Force LLM"])
        self.setColumnWidth(1, 100)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

    def add_row(self):
        row_pos = self.rowCount()
        self.insertRow(row_pos)

        # URL cell (editable)
        url_item = QTableWidgetItem()
        url_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEditable | Qt.ItemIsEnabled)
        self.setItem(row_pos, 0, url_item)

        # Force LLM checkbox cell
        checkbox = QCheckBox()
        checkbox.setChecked(False)

        # Embed checkbox into a QWidget so it displays properly centered
        checkbox_widget = QWidget()
        layout = QHBoxLayout(checkbox_widget)
        layout.addWidget(checkbox)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setCellWidget(row_pos, 1, checkbox_widget)

    def load_csv_to_table(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                url = row.get("url") or row.get("URL") or row.get("Url")
                if url:
                    self.add_url_to_table(url.strip())

    def add_url_to_table(self, url: str, force_llm: bool = False):
        row_pos = self.rowCount()
        self.insertRow(row_pos)

        # URL cell
        self.setItem(row_pos, 0, QTableWidgetItem(url))

        # Force LLM cell (checkbox)
        checkbox = QCheckBox()
        checkbox.setChecked(force_llm)
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.addWidget(checkbox)
        layout.setAlignment(checkbox, Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(layout)
        self.setCellWidget(row_pos, 1, widget)
    