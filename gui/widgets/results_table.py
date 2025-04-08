from PySide6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView,
    QFileDialog, QTableWidgetItem
)
import csv

class ResultsTable(QTableWidget):
    def __init__(self, log, parent=None):
        super().__init__(0, 0, parent)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.results_data = []
        self.log = log
    
    def append_result(self, result_dict):
        self.results_data.append(result_dict)
        headers = [self.horizontalHeaderItem(i).text() for i in range(self.columnCount())]

        for key in result_dict:
            if key not in headers:
                col = self.columnCount()
                self.insertColumn(col)
                self.setHorizontalHeaderItem(col, QTableWidgetItem(key))
                headers.append(key)

        row = self.rowCount()
        self.insertRow(row)

        for col, key in enumerate(headers):
            item_text = result_dict.get(key, "")
            if isinstance(item_text, list):
                item_text = ", ".join(item_text)
            item = QTableWidgetItem(str(item_text))
            self.setItem(row, col, item)

        self.log(f"Scraped: {result_dict.get('URL', '')}")    
    
    def save_results(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "CSV Files (*.csv)")
        if path:
            with open(path, mode='w', newline='', encoding='utf-8') as file:
                if not self.results_data:
                    return
                writer = csv.DictWriter(file, fieldnames=self.results_data[0].keys())
                writer.writeheader()
                for data in self.results_data:
                    writer.writerow(data)
            self.log(f"Results saved to {path}")
