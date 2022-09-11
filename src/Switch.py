from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

class Switch(QWidget):
    new_pitch = pyqtSignal(str)

    def __init__(self, page):
        super(Switch, self).__init__()
        self.new_pitch.emit(page)

    def switched(self, page):
        self.new_pitch.emit(page)
        print('WUT')