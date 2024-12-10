import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from school import Ui_MainWindow  # Импортируй класс из сгенерированного файла

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
