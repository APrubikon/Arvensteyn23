from src.MainLayout import *
from PyQt6.QtWidgets import QVBoxLayout

class Testwidget2(ArvenWidget):
    def __init__(self):
        super(Testwidget2, self).__init__('not')

        self.laebel = ArveLabel('header','test numero duo')
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.laebel)
