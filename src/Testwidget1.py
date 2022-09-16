from src.MainLayout import *
from PyQt6.QtWidgets import QVBoxLayout

class Testwidget1(ArvenWidget):
    def __init__(self):
        super(Testwidget1, self).__init__('not')

        self.laebel = ArveLabel('header','test numero uno')
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.laebel)
