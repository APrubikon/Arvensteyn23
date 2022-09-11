from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QFrame, QVBoxLayout, QSizePolicy, \
    QFrame, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QSize, QEvent, QRectF, QPropertyAnimation, pyqtProperty, QEasingCurve, \
    QVariant, QVariantAnimation, pyqtSlot, QEventLoop, pyqtSignal, QObject
from PyQt6.QtGui import QImage, QPalette, QBrush, QPainter, QColor, QPainterPath, QPen
import os


class SI(QObject):
    signal = pyqtSignal(str)




    @pyqtSlot(str)
    def testdruck(self, page):

        SI.signal.connect(self.icycke)

        SI.signal.emit(page)
        print(page)

    def icycke(self, s):
        print(s)
    






