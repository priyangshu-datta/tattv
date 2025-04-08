import queue
from gui.scrape_process import scrape_url_with_logs
from gui.widgets.log_output import LogOutput
from gui.widgets.results_table import ResultsTable
from gui.widgets.top_header import HeaderBar
from gui.widgets.url_input_table import URLInputTable
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTabWidget, QCheckBox
)
from PySide6.QtCore import QTimer

from multiprocessing import Process, Queue as MPQueue
from utils.logger import logger

class TattvApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tattv")
        self.setMinimumSize(900, 600)
        self.resize(300, 100)

        self.header_layout = HeaderBar()
       
        self.tabs = QTabWidget()

        self.init_input_tab()
        self.init_log_tab()

        layout = QVBoxLayout()
        layout.addWidget(self.header_layout)
        layout.addWidget(self.tabs)
        self.setLayout(layout)

        self.log_queue = MPQueue()
        self.result_queue = MPQueue()
        self.log_timer = QTimer()
        self.log_timer.timeout.connect(self.check_queues)
        self.log_timer.start(100)

        self.results_data = []
        self.llm_client = None
        self.model_name = None

    def init_input_tab(self):
        self.input_tab = QWidget()
        layout = QVBoxLayout()

        self.url_table = URLInputTable()

        btn_layout_1 = QHBoxLayout()
        btn_layout_2 = QHBoxLayout()
        self.scrape_btn = QPushButton("Start Scraping")
        self.scrape_btn.clicked.connect(self.start_scraping)

        self.stop_btn = QPushButton("Stop Scraping")
        self.stop_btn.clicked.connect(self.stop_scraping)
        self.stop_btn.setDisabled(True)  # Disabled until scraping starts

        self.add_row_btn = QPushButton("Add Row")
        self.add_row_btn.clicked.connect(self.url_table.add_row)

        self.upload_csv_btn = QPushButton("Upload CSV")
        self.upload_csv_btn.clicked.connect(self.url_table.load_csv_to_table)

        btn_layout_1.addWidget(self.scrape_btn)
        btn_layout_1.addWidget(self.stop_btn)
        btn_layout_2.addWidget(self.add_row_btn)
        btn_layout_2.addWidget(self.upload_csv_btn) 

        self.result_table = ResultsTable(self.log)

        self.save_results_btn = QPushButton("Save Results")
        self.save_results_btn.clicked.connect(self.result_table.save_results)

        layout.addLayout(btn_layout_1)
        layout.addWidget(QLabel("Input URLs"))
        layout.addLayout(btn_layout_2)
        layout.addWidget(self.url_table)
        layout.addWidget(QLabel("Scraped Results"))
        layout.addWidget(self.result_table)
        layout.addWidget(self.save_results_btn)

        self.input_tab.setLayout(layout)
        self.tabs.addTab(self.input_tab, "Scraper")

    def init_log_tab(self):
        self.log_tab = QWidget()
        layout = QVBoxLayout()

        btn_layout = QHBoxLayout()

        self.log_output = LogOutput()
        self.log_output.setup_logging()

        self.save_logs_btn = QPushButton("Save Logs")
        self.save_logs_btn.clicked.connect(self.log_output.save_logs)

        btn_layout.addWidget(self.save_logs_btn)

        layout.addWidget(QLabel("Log Output"))
        layout.addLayout(btn_layout)
        layout.addWidget(self.log_output)

        self.log_tab.setLayout(layout)
        self.tabs.addTab(self.log_tab, "Log")

    def log(self, message):
        logger.info(message)

    def start_scraping(self):
        self.scrape_btn.setDisabled(True)
        self.stop_btn.setDisabled(False)

        self.header_layout.set_status("busy")

        self.processes = []
        urls = []
        force_llm_flags = []

        for row in range(self.url_table.rowCount()):
            url_item = self.url_table.item(row, 0)
            checkbox_widget = self.url_table.cellWidget(row, 1)
            checkbox = checkbox_widget.findChild(QCheckBox) if checkbox_widget else None

            if url_item and url_item.text().strip():
                urls.append(url_item.text().strip())
                force_llm_flags.append(checkbox.isChecked() if checkbox else False)

        if not urls:
            self.log("No URLs provided.")
            self.scrape_btn.setDisabled(False)
            return
        
        llm_client, model_name = self.header_layout.llm_settings()

        for url, force_llm in zip(urls, force_llm_flags):
            p = Process(
                target=scrape_url_with_logs,
                args=(url, self.log_queue, self.result_queue, llm_client, model_name, force_llm)
            )
            p.start()
            self.processes.append(p)

    def stop_scraping(self):
        self.log("Stopping all scraping processes...")
        for p in getattr(self, 'processes', []):
            if p.is_alive():
                p.terminate()
                p.join()
                self.log(f"Process {p.pid} terminated.")
        self.processes.clear()
        self.scrape_btn.setDisabled(False)
        self.stop_btn.setDisabled(True)
        self.header_layout.set_status("idle")

    def check_queues(self):
        while not self.log_queue.empty():
            try:
                log = self.log_queue.get_nowait()
                self.log(log)
            except queue.Empty:
                break

        while not self.result_queue.empty():
            try:
                result = self.result_queue.get_nowait()
                self.result_table.append_result(result)
            except queue.Empty:
                break

        if all([not p.is_alive() for p in getattr(self, 'processes', [])]):
            self.scrape_btn.setDisabled(False)
            self.stop_btn.setDisabled(True)
            self.header_layout.set_status("idle")

