from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QFrame, QHBoxLayout, QStackedWidget, QSizePolicy, \
    QFrame, QVBoxLayout, QGridLayout, QSizePolicy, QStackedWidget, QStackedLayout, QHBoxLayout, QSpacerItem
from PyQt6.QtCore import Qt, QSize, QEvent, QRectF, QPropertyAnimation, pyqtProperty, QEasingCurve, \
    QVariant, QVariantAnimation, pyqtSlot, QEventLoop, QPoint, QAbstractAnimation, QParallelAnimationGroup
from PyQt6.QtGui import QImage, QPalette, QBrush, QPainter, QColor, QPainterPath, QPen
from src.config import get_headline
import random
import os
from src.desktop import current
from src.MainLayout import *
from src.Testwidget1 import Testwidget1
from src.Testwidget2 import Testwidget2
from src.BaseInfo import BaseInfo
from src.MdtVerwaltung import Mandantenverwaltung
from src.variables import today
from src.auftraege import MainFrameAuftraege, DatenAuftraege
from src.Timesheet import Timeframe
from src.Mdt_new import New_Mandant
from src.Auftrag_new import MainFrameAuftraege as AuftragNeu

basedir = os.path.dirname(__file__)


class Pitch(QMainWindow):

    def __init__(self):
        super(Pitch, self).__init__()

        # general appearance and centralwidget
        self.setStyleSheet('background-color:white')

        self.setObjectName('Arvensteyn_Pitch')
        self.setWindowTitle("Arvensteyn")
        self.grass = QWidget()
        self.grass.setObjectName('green')

        self.main_stack = SlidingStackedWidget()
        self.setCentralWidget(self.grass)
        # customwidgets to inherit
        self.spacerV = QSpacerItem(10, 10, hPolicy=QSizePolicy.Policy.Minimum,
                                   vPolicy=QSizePolicy.Policy.Expanding)
        self.spacerH = QSpacerItem(10, 10, hPolicy=QSizePolicy.Policy.Expanding,
                                   vPolicy=QSizePolicy.Policy.Minimum)

        # Main Layouts
        self.topdown = QVBoxLayout()
        self.topdown.setContentsMargins(0, 35, 40, 0)
        self.topdown.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.grass.setLayout(self.topdown)

        self.across1 = QHBoxLayout()
        self.topdown.addLayout(self.across1)

        self.baseinfo = QVBoxLayout()
        self.across1.addLayout(self.baseinfo)
        self.baseinfo.setContentsMargins(40, 0, 0, 0)
        self.baseinfo.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.across1.addSpacerItem(self.spacerH)

        # create logo
        self.labellogo = QLabel()
        logo = QtGui.QPixmap(os.path.join(basedir, "media/Arvensteyn_Logo.svg"))
       # logo = logo.scaled(509, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        self.labellogo.setPixmap(logo)
        self.labellogo.installEventFilter(self)

        self.across1.addWidget(self.labellogo)

        self.setBaseInfo()
        self.center()

        self.topdown.addWidget(self.main_stack)

        self.stack_zero = Desktop()
        for i in self.stack_zero.findChildren(ColorButton):
            i.installEventFilter(self)
        self.stack_one = BaseInfo()

        self.main_stack.addWidget(self.stack_zero)
        self.main_stack.addWidget(self.stack_one)

        ##signal



    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())




    def setBaseInfo(self):
        self.user_label = ArveLabel('header', get_headline())
        self.baseinfo.addWidget(self.user_label)
        self.datum = ArveLabel('notice', today)
        self.baseinfo.addWidget(self.datum)

    def eventFilter(self, obj, event):

        if event.type() == QEvent.Type.MouseButtonPress:
            if self.labellogo is obj:
                if self.main_stack.currentIndex() == 0:
                    pass
                elif self.main_stack.currentIndex() == 1:
                    self.main_stack.slideInIdx(0)
                else:
                    self.old = self.main_stack.currentWidget()
                    print(self.old)
                    self.main_stack.removeWidget(self.old)
                    self.old.deleteLater()
                    self.main_stack.slideInIdx(0)
                    self.user_label.setText(get_headline())

            if isinstance(obj, ColorButton):
                if obj.text() == 'Benutzer verwalten':
                    idx = self.main_stack.indexOf(self.stack_one)
                    self.main_stack.slideInIdx(idx)

                if obj.text() == 'Mandanten verwalten':
                    self.new = Mandantenverwaltung()
                    self.main_stack.addWidget(self.new)
                    idx = self.main_stack.indexOf(self.new)
                    self.main_stack.slideInIdx(idx)

                if obj.text() == 'Aufträge verwalten':
                    self.new = MainFrameAuftraege()
                    self.main_stack.addWidget(self.new)
                    idx = self.main_stack.indexOf(self.new)
                    self.main_stack.slideInIdx(idx)

                if obj.text() == 'Neue Leistung':
                    self.new = Timeframe()
                    self.main_stack.addWidget(self.new)
                    idx = self.main_stack.indexOf(self.new)
                    self.main_stack.slideInIdx(idx)

                if obj.text() == 'Neuer Mandant':
                    self.new = New_Mandant()
                    self.main_stack.addWidget(self.new)
                    idx = self.main_stack.indexOf(self.new)
                    self.main_stack.slideInIdx(idx)
                    self.new.getmehome.connect(self.slideInHome)

                if obj.text() == 'Neuer Auftrag':
                    self.new = AuftragNeu()
                    self.main_stack.addWidget(self.new)
                    idx = self.main_stack.indexOf(self.new)
                    self.main_stack.slideInIdx(idx)

        return QWidget.eventFilter(self, obj, event)


    @pyqtSlot()
    def slideInHome(self):
        if self.main_stack.currentIndex() == 0:
            pass
        elif self.main_stack.currentIndex() == 1:
            self.main_stack.slideInIdx(0)
        else:
            self.old = self.main_stack.currentWidget()
            print(self.old)
            self.main_stack.removeWidget(self.old)
            self.old.deleteLater()
            self.main_stack.slideInIdx(0)
            self.user_label.setText(get_headline())


class SlidingStackedWidget(QStackedWidget):
    def __init__(self, parent=None):
        super(SlidingStackedWidget, self).__init__(parent)

        self.m_direction = Qt.Orientation.Vertical
        self.m_speed = 200
        self.m_animationType = QEasingCurve.Type.InElastic
        self.m_now = 0
        self.m_next = 0
        self.m_wrap = False
        self.m_pnow = QPoint(0, 0)
        self.m_active = False


    def setDirection(self, direction):
        self.m_direction = direction

    def setSpeed(self, speed):
        self.m_speed = speed

    def setAnimation(self, animation_type):
        self.m_animationType = animation_type

    def setWrap(self, wrap):
        self.m_wrap = wrap

    @pyqtSlot()
    def slideInPrev(self):
        now = self.currentIndex()
        if self.m_wrap or now > 0:
            self.slideInIdx(now - 1)

    @pyqtSlot()
    def slideInNext(self):
        now = self.currentIndex()
        if self.m_wrap or now < (self.count() - 1):
            self.slideInIdx(now + 1)

    def slideInIdx(self, idx):
        if idx > (self.count() - 1):
            idx = idx % self.count()
        elif idx < 0:
            idx = (idx + self.count()) % self.count()
        self.slideInWgt(self.widget(idx))



    def slideInWgt(self, new_widget):
        if self.m_active:
            return

        self.m_active = True

        _now = self.currentIndex()
        _next = self.indexOf(new_widget)

        if _now == _next:
            self.m_active = False
            return

        offset_X, offset_Y = self.frameRect().width(), self.frameRect().height()
        self.widget(_next).setGeometry(self.frameRect())

        if not self.m_direction == Qt.Orientation.Horizontal:
            if _now < _next:
                offset_X, offset_Y = 0, -offset_Y
            else:
                offset_X = 0
        else:
            if _now < _next:
                offset_X, offset_Y = -offset_X, 0
            else:
                offset_Y = 0

        page_next = self.widget(_next).pos()
        pnow = self.widget(_now).pos()
        self.m_pnow = pnow

        offset = QPoint(offset_X, offset_Y)
        self.widget(_next).move(page_next - offset)
        self.widget(_next).show()
        self.widget(_next).raise_()

        anim_group = QParallelAnimationGroup(self)
        anim_group.finished.connect(self.animationDoneSlot)

        for index, start, end in zip(
            (_now, _next), (pnow, page_next - offset), (pnow + offset, page_next)
        ):
            animation = QPropertyAnimation(self.widget(index), b'pos')
            animation.setEasingCurve(self.m_animationType)
            animation.setDuration(self.m_speed)
            animation.setStartValue(start)
            animation.setEndValue(end)
            anim_group.addAnimation(animation)

        self.m_next = _next
        self.m_now = _now
        self.m_active = True
        anim_group.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)

    @pyqtSlot()
    def animationDoneSlot(self):
        self.setCurrentIndex(self.m_next)
        self.widget(self.m_now).hide()
        self.widget(self.m_now).move(self.m_pnow)
        self.m_active = False


class Desktop(ArvenWidget):
    def __init__(self):
        super(Desktop, self).__init__(framed='not')

        self.desktopgrid = QGridLayout()
        self.desktopgrid.setContentsMargins(80, 80, 80, 80)
        self.desktopgrid.setSpacing(40)
        self.setLayout(self.desktopgrid)
        # self.desktopgrid.setAlignment(Qt.AlignmentFlag.AlignTop)

        # pc Nr. 1
        self.aktenverwaltung = PlayingCard('Aktenverwaltung', 'Neuer Mandant', 'Mandanten verwalten', 'Neuer Auftrag',
                                           'Aufträge verwalten')
        # self.aktenverwaltung.secondaryWidget.a.clicked.connect(self.testsender)
        # PC Nr. 2
        self.leistungserfassung = PlayingCard('Leistungserfassung', 'Neue Leistung', 'Persönliche Auswertung')

        # PC Nr. 3
        self.rechnungslauf = PlayingCard('Abrechnung', 'Rechnungslauf', 'Rechnungen erstellen', 'Offene Rechnungen')

        # PC Nr. 4
        self.einstellungen = PlayingCard('Einstellungen', 'Benutzer verwalten')

        # PC Nr. 5
        self.dokumente = PlayingCard('Dokument erstellen', 'Anschreiben', 'Telefonvermerk', 'Kurzgutachten')

        # PC Nr. 6
        self.auswertungen = PlayingCard('Auswertung', 'Arbeitszeit', 'Umsätze')

        self.desktopgrid.addWidget(self.aktenverwaltung, 0, 0)
        self.desktopgrid.addWidget(self.leistungserfassung, 0, 1)
        self.desktopgrid.addWidget(self.rechnungslauf, 1, 1)
        self.desktopgrid.addWidget(self.einstellungen, 1, 0)
        self.desktopgrid.addWidget(self.dokumente, 0, 2)
        self.desktopgrid.addWidget(self.auswertungen, 1, 2)


class PlayingCard(QWidget):
    BorderColor = QColor(9, 58, 112, 255)
    BackgroundColor = QColor(255, 255, 255, 180)
    print(basedir)

    def __init__(self, Function: str, subfunction1: str = None, subfunction2: str = None, subfunction3: str = None,
                 subfunction4: str = None) -> object:
        super(PlayingCard, self).__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # self.setBaseSize(250, 300)
        # self.setMinimumHeight(300)

        policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setSizePolicy(policy)
        self.setObjectName('PlayingCard')

        # self.setStyleSheet("background-image: url(media/g2045-3t.png); background-repeat:no-repeat; background-origin: content; background-position: bottom ")

        self.base_layout = QVBoxLayout()
        # self.base_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.setLayout(self.base_layout)
        # self.base_layout.setContentsMargins(0, 10, 0, 0)
        self.base_button = QPushButton(Function)
        basebutton_style = """color : rgb(9, 58, 112); border-width:0px; border-style:none; background-color:transparent; font-weight: bold; font: 24pt;"""
        self.base_button.setStyleSheet(basebutton_style)
        self.base_button.installEventFilter(self)

        self.base_layout.addWidget(self.base_button)
        # self.base_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.secondaryWidget = SubControls(subfunction1, subfunction2, subfunction3, subfunction4)
        self.base_layout.addWidget(self.secondaryWidget)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.Enter:
            if self.base_button is obj:
                self.focus_buttons_in()
        elif event.type() == QEvent.Type.Leave:
            self.focus_buttons_out()

        return QWidget.eventFilter(self, obj, event)

    def focus_buttons_in(self):
        for i in self.secondaryWidget.children():
            if isinstance(i, ColorButton):
                i.fade_in()

    def focus_buttons_out(self):
        for i in self.secondaryWidget.children():
            if isinstance(i, ColorButton):
                i.fade_out()

    def paintEvent(self, event):
        super(PlayingCard, self).paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rectPath = QPainterPath()
        height = self.height() - 8
        rectPath.addRoundedRect(QRectF(2, 2, self.width() - 4, height), 15, 15)
        painter.setPen(QPen(self.BorderColor, 2, Qt.PenStyle.SolidLine,
                            Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))

        oImage = QImage(os.path.join(basedir, "media/arve_blau_45a.svg"))

        sImage = oImage.scaled(QSize(220, 300), Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)  # resize Image to widgets size

        painter.drawPath(rectPath)
        painter.setPen(QPen(self.BackgroundColor, 2,
                            Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))

        pal = self.palette()
        pal.setBrush(QPalette.ColorRole.Base, QBrush(sImage))
        self.setPalette(pal)


class SubControls(QWidget):
    BorderColor = QColor(9, 58, 112, 255)
    BackgroundColor = QColor(255, 255, 255, 180)

    def __init__(self, subcontrol1: str = None, subcontrol2: str = None, subcontrol3: str = None,
                 subcontrol4: str = None):
        super(SubControls, self).__init__()
        # self.setFixedSize(QSize(200,200))
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.subcontrol1 = subcontrol1
        self.subcontrol2 = subcontrol2
        self.subcontrol3 = subcontrol3
        self.subcontrol4 = subcontrol4
        self.secondary_layout = QVBoxLayout()
        self.setLayout(self.secondary_layout)
        self.secondary_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setObjectName("subcontrols")
        self.setAutoFillBackground(True)
        self.addSubButtons()

        # set image size equivalent to that of subwidget
        oImage = QImage(os.path.join(basedir, "media/arve_blau_45a.svg"))

        sImage = oImage.scaled(QSize(220, 300), Qt.AspectRatioMode.KeepAspectRatio,
                               Qt.TransformationMode.SmoothTransformation)  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(sImage))
        self.setPalette(palette)

    def addSubButtons(self):
        sublist = []
        if not self.subcontrol1 is None:
            sublist.append(self.subcontrol1)
        if not self.subcontrol2 is None:
            sublist.append(self.subcontrol2)
        if not self.subcontrol3 is None:
            sublist.append(self.subcontrol3)
        if not self.subcontrol4 is None:
            sublist.append(self.subcontrol4)

        for i in sublist:
            self.a = ColorButton(i)
            self.a.setObjectName(i)
            self.secondary_layout.addWidget(self.a)

            #self.a.clicked.connect(lambda checked=False, a=i: Pitch.change_stack(Pitch(), a))
            #

class HLine(QFrame):
    def __init__(self):
        super(HLine, self).__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setFixedWidth(4)


class ColorButton(QPushButton):
    def __init__(self, title):
        super(ColorButton, self).__init__()
        self.setText(title)
        self.setStyleSheet('background-color:rgba(255, 255, 255, 0);'
                           'border-style:none; border-width:0px; font:18pt;')

        self.make_invisible()

    def _color(self):
        return self.palette().color(QPalette.ColorRole.ButtonText)

    def _setColor(self, qcolor):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.ButtonText, qcolor)
        self.setPalette(palette)

    color = pyqtProperty(QColor, _color, _setColor)

    def make_invisible(self):
        pal = self.palette()
        pal.setColor(QPalette.ColorRole.ButtonText, QColor(9, 58, 112, 0))
        self.setPalette(pal)

    def fade_in(self):
        self.text_color_animation = QPropertyAnimation(self, b'color')
        self.text_color_animation.stop()
        self.text_color_animation.setStartValue(QColor(0, 0, 0, 0))
        self.text_color_animation.setEndValue(QColor(9, 58, 112, 255))
        self.text_color_animation.setDuration(500)
        self.text_color_animation.start()

    def fade_out(self):
        self.text_color_animation = QPropertyAnimation(self, b'color')
        self.text_color_animation.stop()
        self.text_color_animation.setStartValue(QColor(9, 58, 112, 255))
        self.text_color_animation.setEndValue(QColor(0, 0, 0, 0))
        self.text_color_animation.setDuration(6000)
        self.text_color_animation.start()
