from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QFrame, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QSize, QEvent, QRectF, QPropertyAnimation, pyqtProperty
from PyQt6.QtGui import QImage, QPalette, QBrush, QPainter, QColor, QPainterPath, QPen
import os


class PlayingCard(QWidget):
    BorderColor = QColor(9, 58, 112, 255)
    BackgroundColor = QColor(255, 255, 255, 180)

    def __init__(self, Function: str, subfunction1=None, subfunction2=None, subfunction3=None, subfunction4=None):
        super(PlayingCard, self).__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)


        self.setMinimumWidth(200)
        self.setMinimumHeight(300)

        policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setSizePolicy(policy)
        self.setObjectName('PlayingCard')

        self.base_layout = QVBoxLayout()
        self.setLayout(self.base_layout)
        self.base_layout.setContentsMargins(0, 10, 0, 0)
        self.base_button = QPushButton(Function)
        basebutton_style = """color : rgb(9, 58, 112); border-width:0px; border-style:none; background-color:transparent; font:18pt;"""
        self.base_button.setStyleSheet(basebutton_style)
        self.base_button.installEventFilter(self)

        self.base_layout.addWidget(self.base_button)
        self.base_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.secondaryWidget = SubControls(subfunction1, subfunction2, subfunction3, subfunction4)
        self.base_layout.addWidget(self.secondaryWidget)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Enter:
            if self.base_button is obj:
                self.focus_buttons_in()
        elif event.type() == QEvent.Type.Leave:
            if self.base_button is obj:
                self.focus_buttons_out()

        return QWidget.eventFilter(self, obj, event)

    def focus_buttons_in(self):
        print("button1 on")

    def focus_buttons_out(self):
        print("button1 off")

    def paintEvent(self, event):
        super(PlayingCard, self).paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rectPath = QPainterPath()
        height = self.height() - 8
        rectPath.addRoundedRect(QRectF(2, 2, self.width() - 4, height), 15, 15)
        painter.setPen(QPen(self.BorderColor, 2, Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
        painter.setBrush(self.BackgroundColor)
        painter.drawPath(rectPath)
        painter.setPen(QPen(self.BackgroundColor, 2,
                            Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))


class SubControls(QFrame):
    BorderColor = QColor(9, 58, 112, 255)
    BackgroundColor = QColor(255, 255, 255, 180)

    def __init__(self, subcontrol1: str = None, subcontrol2: str = None, subcontrol3: str = None,
                 subcontrol4: str = None):
        super(SubControls, self).__init__()
        self.setBaseSize(QSize(300, 200))

        self.subcontrol1 = subcontrol1
        self.subcontrol2 = subcontrol2
        self.subcontrol3 = subcontrol3
        self.subcontrol4 = subcontrol4

        self.setObjectName("subcontrols")
        self.setAutoFillBackground(True)

        # todo vectorgraphic, relative path
        oImage = QImage("media/g2045-3t.png")
        sImage = oImage.scaled(QSize(300, 200))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(sImage))
        self.setPalette(palette)

        self.secondary_layout = QVBoxLayout()
        self.secondary_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.secondary_layout)
        self.secondary_layout.setContentsMargins(2, 10, 2, 2)

        # todo create tertiarywidget only if subcontrol is not none
        self.include_tertiary_widget1()
        self.include_tertiary_widget2()
        self.include_tertiary_widget3()
        self.include_tertiary_widget4()
    def include_tertiary_widget1(self):
        if not self.subcontrol1 is None:
            self.tertiary_widget1 = ColorButton(self.subcontrol1)
            self.secondary_layout.addWidget(self.tertiary_widget1)
    def include_tertiary_widget2(self):
            if not self.subcontrol2 is None:
                self.tertiary_widget2 = ColorButton(self.subcontrol2)
                self.secondary_layout.addWidget(self.tertiary_widget2)

    def include_tertiary_widget3(self):
        if not self.subcontrol3 is None:
            self.tertiary_widget3 = ColorButton(self.subcontrol3)
            self.secondary_layout.addWidget(self.tertiary_widget3)

    def include_tertiary_widget4(self):
        if not self.subcontrol4 is None:
            self.tertiary_widget4 = ColorButton(self.subcontrol4)
            self.secondary_layout.addWidget(self.tertiary_widget4)



class HLine(QFrame):
    def __init__(self):
        super(HLine, self).__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setFixedWidth(4)


class ColorButton(QPushButton):

    @pyqtProperty(QColor)
    def backgroundColor(self):
        return self.palette().color(QPalette.ColorRole.Button)

    @backgroundColor.setter
    def backgroundColor(self, qcolor):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Button, qcolor)
        self.setPalette(palette)
        return self.palette().color(QPalette.ColorRole.ButtonText)
    def _color(self):
        return self.palette().color(QPalette.ColorRole.ButtonText)

    def _setColor(self, qcolor):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.ButtonText, qcolor)
        self.setPalette(palette)
        


    