from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QFrame, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QSize, QEvent, QRectF
from PyQt6.QtGui import QImage, QPalette, QBrush, QPainter, QColor, QPainterPath, QPen
import os


class PlayinCard(QWidget):
    def __init__(self, Function:str, subfunction1 = None, subfunction2 = None, subfunction3 = None, subfunction4 = None):
        super(PlayinCard, self).__init__()
        self.setObjectName("PlayinCard")

        # todo:  necessary, if PlayingCard is not top line widget (Window)?
        self.setAutoFillBackground(True)

        self.pc_layout = QVBoxLayout()
        self.setLayout(self.pc_layout)

        #todo use less opacity, svg, relative path
        BackgroundArve = QImage('media/g2045-3t.png')
        BackgroundArve = BackgroundArve.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)

        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(BackgroundArve))
        self.setPalette(palette)

        #self.label = QLabel('Test', self)  # test, if it's really backgroundimage
        #self.label.setGeometry(50, 50, 200, 50)

        self.pc_mainfunction = QPushButton()
        self.pc_mainfunction.setObjectName('PC_main')
        self.pc_mainfunction.setText(Function)

        self.pc_subfunction1 = QPushButton()
        self.pc_subfunction1.setObjectName('PC_sub1')
        self.pc_subfunction1.setText(subfunction1)
        self.pc_subfunction2 = QPushButton()
        self.pc_subfunction2.setObjectName('PC_sub2')
        self.pc_subfunction2.setText(subfunction2)
        self.pc_subfunction3 = QPushButton()
        self.pc_subfunction3.setObjectName('PC_sub3')
        self.pc_subfunction3.setText(subfunction3)
        self.pc_subfunction4 = QPushButton()
        self.pc_subfunction4.setObjectName('PC_sub4')
        self.pc_subfunction4.setText(subfunction4)

        self.pc_layout.addWidget(self.pc_mainfunction)
        self.pc_layout.addWidget(self.pc_subfunction1)
        self.pc_layout.addWidget(self.pc_subfunction2)
        self.pc_layout.addWidget(self.pc_subfunction3)
        self.pc_layout.addWidget(self.pc_subfunction4)


class TestCard(QWidget):
    BorderColor = QColor(9, 58, 112, 255)
    BackgroundColor = QColor(255, 255, 255, 180)
    def __init__(self, Function:str, subfunction1 = None, subfunction2 = None, subfunction3 = None, subfunction4 = None):
        super(TestCard, self).__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.setMinimumWidth(200)
        self.setMinimumHeight(300)
      
        policy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setSizePolicy(policy)
        self.setObjectName('PlayingCard')
       
        #self.setStyleSheet("background-image: url(media/g2045-3t.png); background-repeat:no-repeat; background-origin: content; background-position: bottom ")

        self.base_layout = QVBoxLayout()
        self.setLayout(self.base_layout)
        self.base_layout.setContentsMargins(0, 10, 0, 0)
        self.base_button = QPushButton(Function)
        basebutton_style = """color : rgb(9, 58, 112); border-width:0px; border-style:none; background-color:transparent; font:18pt;"""
        self.base_button.setStyleSheet(basebutton_style)
        self.base_button.installEventFilter(self)

        self.base_layout.addWidget(self.base_button)
        self.base_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.secondaryWidget = SubControls()
        self.base_layout.addWidget(self.secondaryWidget)

        #self.secondary_layout = QVBoxLayout(self.secondary_widget)
        #self.tertiary_widget1 = QPushButton("test1")
        #self.tertiary_widget2 = QPushButton("test2")
        #
        #self.secondary_layout.addWidget(self.tertiary_widget1)
        #self.secondary_layout.addWidget(self.tertiary_widget2)
        #

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Enter:
            if self.base_button is obj:
                self.focus_buttons_in()
        elif event.type() == QEvent.Type.Leave:
            self.focus_buttons_out()

        return QWidget.eventFilter(self, obj, event)

    def focus_buttons_in(self):
        print("button1 on")

    def focus_buttons_out(self):
        print("button1 off")

    def paintEvent(self, event):
        super(TestCard, self).paintEvent(event)

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
    def __init__(self, subcontrol1:str = None, subcontrol2:str = None, subcontrol3:str = None, subcontrol4:str = None):
        super(SubControls, self).__init__()
        self.setFixedSize(QSize(300,200))

        self.setObjectName("subcontrols")
        self.setAutoFillBackground(True)

        # todo vectorgraphic, relative path
        oImage = QImage("media/g2045-3t.png")
        sImage = oImage.scaled(QSize(300,200))                   # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(sImage))
        self.setPalette(palette)

        self.secondary_layout = QVBoxLayout()
        self.setLayout(self.secondary_layout)
        # todo create tertiarywidget only if subcontrol is not none
        self.tertiary_widget1 = QPushButton("test1")
        self.tertiary_widget2 = QPushButton("test2")
        
        self.secondary_layout.addWidget(self.tertiary_widget1)
        self.secondary_layout.addWidget(self.tertiary_widget2)

        top = QRectF()
        self.setFrameShape(QFrame.rect())







class HLine(QFrame):
    def __init__(self):
        super(HLine, self).__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setFixedWidth(4)

