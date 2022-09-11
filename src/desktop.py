from PyQt6.QtWidgets import QGridLayout, QWidget, QPushButton, QLabel, QFrame, QVBoxLayout, QSizePolicy, \
    QFrame, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import pyqtSlot, Qt, QSize, QEvent, QRectF, QPropertyAnimation, pyqtProperty, QEasingCurve, \
    QVariant, QVariantAnimation, pyqtSlot, QEventLoop, pyqtSignal, QObject
from src.MainLayout import *


from PyQt6.QtGui import QImage, QPalette, QBrush, QPainter, QColor, QPainterPath, QPen
import os
from src.Switch import Switch
basedir = os.path.dirname(__file__)

current = 0

@pyqtSlot(str)
def switch(pagetitle):
    print(pagetitle)


