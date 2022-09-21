from PyQt6.QtCore import pyqtSignal, pyqtSlot, QEvent, QObject, QPoint, pyqtProperty, QSize, Qt, QRect, QAbstractItemModel, QModelIndex
from PyQt6.QtGui import QPixmap, QMouseEvent, QPainter
from PyQt6.QtWidgets import QApplication, QStyle, QProxyStyle, QStyleOptionViewItem, QItemDelegate, QWidget, QHBoxLayout, QCheckBox, QStyledItemDelegate, QStyleOptionButton

class EmptyDelegate(QItemDelegate):
    def __init__(self):
        super(EmptyDelegate, self).__init__()

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


class CheckBoxDelegateQt(QStyledItemDelegate):
    ###Delegate for editing bool values via a checkbox with no label centered in its cell.
    #Does not actually create a QCheckBox, but instead overrides the paint() method to draw the checkbox directly.
    #Mouse events are handled by the editorEvent() method which updates the model's bool value.

    def __init__(self, parent=None):
        QStyledItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        ###Important, otherwise an editor is created if the user clicks in this cell.

        return None

    def paint(self, painter, option, index):
        ###Paint a checkbox without the label.

        checked = bool(index.model().data(index, Qt.ItemDataRole.DisplayRole))
        opts = QStyleOptionButton()
        opts.state |= QStyle.StateFlag.State_Active
        if index.flags() & Qt.ItemFlag.ItemIsEditable:
            opts.state |= QStyle.StateFlag.State_Enabled
        else:
            opts.state |= QStyle.StateFlag.State_ReadOnly
        if checked:
            opts.state |= QStyle.StateFlag.State_On
        else:
            opts.state |= QStyle.StateFlag.State_Off
        #opts.rect = self.getCheckBoxRect(option)
        QApplication.style().drawControl(QStyle.ControlElement.CE_CheckBox, opts, painter)

    def editorEvent(self, event, model, option, index):
        ###Change the data in the model and the state of the checkbox if the
        #user presses the left mouse button and this cell is editable. Otherwise do nothing.

        if not (index.flags() & Qt.ItemFlag.ItemIsEditable):
            return False
        if event.button() == Qt.MouseButton.LeftButton:
            if event.type() == QEvent.Type.MouseButtonRelease:
               # if self.getCheckBoxRect(option).contains(event.pos()):
                self.setModelData(None, model, index)
                return True
            elif event.type() == QEvent.Type.MouseButtonDblClick:
                #if self.getCheckBoxRect(option).contains(event.pos()):
                return True
        return False

    def setModelData(self, editor, model, index):
        ###Toggle the boolean state in the model.

        checked = not bool(index.model().data(index, Qt.ItemDataRole.DisplayRole))
        model.setData(index, checked, Qt.ItemDataRole.EditRole)

    #def getCheckBoxRect(self, option):
    #    ###Get rect for checkbox centered in option.rect.
    #
    #    ### Get size of a standard checkbox.
    #    opts = QStyleOptionButton()
    #    checkBoxRect = QApplication.style().subElementRect(QStyle.SubElement.SE_CheckBoxIndicator, opts, None)
    #    ### Center checkbox in option.rect.
    #    x = option.rect.x()
    #    y = option.rect.y()
    #    w = option.rect.width()
    #    h = option.rect.height()
    #    checkBoxTopLeftCorner = QPoint(x + w / 2 - checkBoxRect.width() / 2, y + h / 2 - checkBoxRect.height() / 2)
    #    return QRect(checkBoxTopLeftCorner, checkBoxRect.size())
    #


class BooleanDelegate(QItemDelegate):

    def __init__(self, *args, **kwargs):
        super(BooleanDelegate, self).__init__(*args, **kwargs)

    def paint(self, painter, option, index):
        # Depends on how the data function of your table model is implemented
        # 'value' should recive a bool indicate if the checked value.
        value = index.data(Qt.ItemDataRole.CheckStateRole)
        self.drawCheck(painter, option, option.rect, value)
        self.drawFocus(painter, option, option.rect)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.Type.MouseButtonRelease:
            value = bool(model.data(index, Qt.ItemDataRole.CheckStateRole))
            model.setData(index, not value)
            event.accept()
        return super(BooleanDelegate, self).editorEvent(event, model, option, index)


class CheckBoxDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        '''
        Important, otherwise an editor is created if the user clicks in this cell.
        '''
        return None

    def paint(self, painter, option, index):
        '''
        Paint a checkbox without the label.
        '''
        checked = bool(index.model().data(index, Qt.ItemDataRole.DisplayRole))
        check_box_style_option = QStyleOptionButton()

        if (index.flags() & Qt.ItemFlag.ItemIsEditable) is True:
            check_box_style_option.state |= QStyle.StateFlag.State_Enabled
        else:
            check_box_style_option.state |= QStyle.StateFlag.State_ReadOnly

        if checked:
            check_box_style_option.state |= QStyle.StateFlag.State_On
        else:
            check_box_style_option.state |= QStyle.StateFlag.State_Off

        check_box_style_option.rect = self.getCheckBoxRect(option)
        if not index.model().hasFlag(index, Qt.ItemFlag.ItemIsEditable):
            check_box_style_option.state |= QStyle.StateFlag.State_ReadOnly

        QApplication.style().drawControl(QStyle.ControlElement.CE_CheckBox, check_box_style_option, painter)


    def editorEvent(self, event, model, option, index):
        '''
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton or presses
        Key_Space or Key_Select and this cell is editable. Otherwise do nothing.
        '''
        if not (index.flags() & Qt.ItemFlag.ItemIsEditable) > 0:
            return False

        # Do not change the checkbox-state
        if event.type() == QEvent.Type.MouseButtonRelease or event.type() == QEvent.Type.MouseButtonDblClick:
            if event.button() != Qt.MouseButton.LeftButton or not self.getCheckBoxRect(option).contains(event.pos()):
                return False
            if event.type() == QEvent.Type.MouseButtonDblClick:
                return True
        elif event.type() == QEvent.Type.KeyPress:
            if event.key() != Qt.Key.Key_Space and event.key() != Qt.Key.Key_Select:
                return False
        else:
            return False

        # Change the checkbox-state
        self.setModelData(None, model, index)
        return True

    def setModelData(self, editor, model, index):
        '''
        The user wanted to change the old state in the opposite.
        '''
        newValue = not bool(index.model().data(index, Qt.ItemDataRole.DisplayRole))
        model.setData(index, newValue, Qt.ItemDataRole.EditRole)


    def getCheckBoxRect(self, option):
        check_box_style_option = QStyleOptionButton()
        check_box_rect = QApplication.style().subElementRect(QStyle.SubElement.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QPoint (option.rect.x() +
                             option.rect.width() / 2 -
                             check_box_rect.width() / 2,
                             option.rect.y() +
                             option.rect.height() / 2 -
                             check_box_rect.height() / 2)
        return QRect(check_box_point, check_box_rect.size())


class BooleanDelegateII(QItemDelegate):
    def __init__(self, *args, **kwargs):
        super(BooleanDelegateII, self).__init__(*args, **kwargs)

    def paint(self, painter, option, index):
        # Depends on how the data function of your table model is implemented
        # 'value' should recive a bool indicate if the checked value.
        value = index.data(Qt.ItemDataRole.CheckStateRole)
        self.drawCheck(painter, option, option.rect, value)
        self.drawFocus(painter, option, option.rect)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.Type.MouseButtonRelease:
            value = bool(model.data(index, Qt.ItemDataRole.CheckStateRole))
            model.setData(index, not value)
            event.accept()
        return super(BooleanDelegateII, self).editorEvent(event, model, option, index)

class QTableviewEditableDelegate(QStyledItemDelegate):
    def __init__(self, alignment: Qt.AlignmentFlag, parent = None):
        super().__init__(parent)
        self.alignment: Qt.AlignmentFlag = alignment
        self.parent = parent

        if self.parent:
            self.style = self.parent.style()
        else:
            self.style = QApplication.style()

    def editorEvent(self, event: QMouseEvent, model: QAbstractItemModel, option: QStyleOptionViewItem,
                    index: QModelIndex) -> bool:
        checkbox_data = index.data(Qt.ItemDataRole.CheckStateRole)
        flags = index.flags()
        if not (flags & Qt.ItemFlag.ItemIsUserCheckable) or not (flags & Qt.ItemFlag.ItemIsEnabled) or checkbox_data is None:
            return False
        else:
            if event.type() == QEvent.Type.MouseButtonRelease:
                mouseover_checkbox: bool = self.get_checkbox_rect(option).contains(event.pos())
                if not mouseover_checkbox:
                    return False
            elif event.type() == QEvent.Type.KeyPress and event.key() != Qt.Key.Key_Space:
                return False
            else:
                return False
            if checkbox_data == Qt.CheckState.Checked:
                checkbox_toggled = Qt.CheckState.Unchecked
            else:
                checkbox_toggled = Qt.CheckState.Checked
            return model.setData(index, checkbox_toggled, Qt.ItemDataRole.CheckStateRole)

    def get_checkbox_rect(self, option: QStyleOptionViewItem) -> QRect:
        widget = option.widget
        if widget:
            style = widget.style()
        else:
            style = self.style()
        checkbox_size: QSize = style.subElementRect(QStyle.SubElement.SE_CheckBoxIndicator, option, widget).size()
        return QStyle.alignedRect(option.direction, Qt.AlignmentFlag.AlignCenter, checkbox_size, option.rect)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        try:
            self.initStyleOption(option, index)
            painter.save()

            flags = index.model().flags(index)
            widget = option.widget()
            checkbox_data = index.data(Qt.ItemDataRole.CheckStateRole)
            if widget:
                style = widget.style()
            else:
                style = self.style()

            if checkbox_data is not None:
                option_checkbox = option
                self.initStyleOption(option_checkbox, index)
                option_checkbox.state = option_checkbox.state & ~QStyle.StateFlag.State_HasFocus
                option_checkbox.features = option_checkbox.features & ~QStyleOptionViewItem.ViewItemFeature.HasDisplay
                option_checkbox.features = option_checkbox.features & ~QStyleOptionViewItem.ViewItemFeature.HasDecoration
                option_checkbox.features = option_checkbox.features & ~QStyleOptionViewItem.ViewItemFeature.HasCheckIndicator
                style.drawControl(QStyle.ControlElement.CE_ItemViewItem, option_checkbox, painter, widget)

                # Then just draw the a checkbox centred in the cell
                option_checkbox.rect = self.get_checkbox_rect(option_checkbox)
                if option_checkbox.checkState == Qt.CheckState.Checked:
                    state_flag = QStyle.StateFlag.State_On
                else:
                    state_flag = QStyle.StateFlag.State_Off

                option_checkbox.state = option_checkbox.state | state_flag
                style.drawPrimitive(QStyle.PrimitiveElement.PE_IndicatorItemViewItemCheck, option_checkbox, painter, widget)

            else:
                QStyledItemDelegate.paint(self, painter, option, index)

            painter.restore()

        except Exception as e:
            print(repr(e))


class ProxyStyle(QProxyStyle):
    def subElementRect(self, element, opt, widget=None):
        if element == self.SubElement.SE_ItemViewItemCheckIndicator and not opt.text:
            rect = super().subElementRect(element, opt, widget)
            rect.moveCenter(opt.rect.center())
            return rect
        return super().subElementRect(element, opt, widget)

class MyCheckBox(QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        # create a centered checkbox
        self.cb = QCheckBox(parent)
        cbLayout = QHBoxLayout(self)
        cbLayout.addWidget(self.cb, 0, Qt.AlignmentFlag.AlignCenter)
        self.cb.clicked.connect(self.amClicked)

    clicked = pyqtSignal()

    def amClicked(self):
        self.clicked.emit()

class CheckBoxDelegate(QItemDelegate):
    """
    A delegate that places a fully functioning QCheckBox in every
    cell of the column to which it's applied
    """
    def __init__(self, parent):
        super(CheckBoxDelegate, self).__init__()

    def createEditor(self, parent, option, index):
        if not (Qt.ItemFlag.ItemIsEditable & index.flags()):
            return None
        cb = MyCheckBox(parent)
        cb.clicked.connect(self.stateChanged)
        return cb

    def setEditorData(self, editor, index):
        """ Update the value of the editor """
        editor.blockSignals(True)
        editor.setChecked(index.data())
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        """ Send data to the model """
        model.setData(index, editor.isChecked(), Qt.ItemDataRole.EditRole)

    def paint(self, painter, option, index):
        value = index.data()
        if value == 1:
            value = Qt.CheckState.Checked
        else:
            value = Qt.CheckState.Unchecked
        self.drawCheck(painter, option, option.rect, value)
        self.drawFocus(painter, option, option.rect)

    @pyqtSlot()
    def stateChanged(self):
        print("sender", self.sender())
        self.commitData.emit(self.sender())