import multiprocessing
import sys
from PySide6.QtWidgets import QApplication, QStyleFactory
from PySide6.QtGui import QIcon
from gui.main_window import TattvApp


if __name__ == '__main__':
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("assets/tattv_icon.png"))
    QApplication.setStyle(QStyleFactory.create("Fusion"))
    window = TattvApp()
    window.show()
    sys.exit(app.exec())
