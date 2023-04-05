from PyQt6.QtCore import QEvent, Qt, QPoint, QMimeData, QCoreApplication, QRect, pyqtSignal
from PyQt6.QtGui import QAction, QPixmap, QRegion, QDrag, QCursor
from PyQt6.QtWidgets import (QTabWidget, QSizePolicy, QTabBar)

from widgets.texteditor import TextEditor


class TabManager(QTabWidget):
    split_editor = pyqtSignal(TextEditor, str)
    close_widget = pyqtSignal(QTabWidget)
    add_split = pyqtSignal(QPoint, QTabWidget, QTabWidget)
    editor_changed = pyqtSignal(TextEditor)

    def __init__(self, index):
        super().__init__()
        self.index = index
        self.init_parameters()
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

    def init_parameters(self):
        self.setTabPosition(QTabWidget.TabPosition.North)
        self.setMovable(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)
        self.setTabsClosable(True)
        self.setTabsClosable(True)
        self.setStyleSheet(f'border-style: none;')
        self.tabCloseRequested.connect(self.request_close)
        self.setAcceptDrops(True)
        self.tabBar = self.tabBar()
        self.tabBar.setMouseTracking(True)
        self.setDocumentMode(True)

        self.editors = list()
        QCoreApplication.instance().installEventFilter(self)

    def addEditor(self, editor: TextEditor, name, icon=None):
        self.editors.append(editor)
        editor.set_parent_manager(self)
        if icon:
            return self.addTab(editor, icon, name)
        return self.addTab(editor, name)

    def request_close(self, index):
        self.editors.remove(self.widget(index))
        self.removeTab(index)
        if self.count() == 0:
            self.close_widget.emit(self)


    def change_current_text(self, title: str):
        self.setTabText(self.currentIndex(), title)

    def eventFilter(self, obj, event):
        if obj == self.tabBar:
            if event.type() == QEvent.Type.MouseMove:
                self.mouseMoveEvent(event)
                return True
            else:
                return False
        else:
            return False

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.MouseButton.LeftButton:
            return

        globalPos = self.mapToGlobal(e.pos())
        tabBar = self.tabBar
        posInTab = tabBar.mapFromGlobal(globalPos)
        self.indexTab = tabBar.tabAt(e.pos())
        tabRect = tabBar.tabRect(self.indexTab)

        pixmap = QPixmap(tabRect.size())
        tabBar.render(pixmap, QPoint(), QRegion(tabRect))
        mimeData = QMimeData()
        drag = QDrag(tabBar)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        cursor = QCursor(Qt.CursorShape.OpenHandCursor)
        drag.setHotSpot(e.pos() - posInTab)
        drag.setDragCursor(cursor.pixmap(), Qt.DropAction.MoveAction)
        dropAction = drag.exec(Qt.DropAction.MoveAction)

    def dragEnterEvent(self, e):
        e.accept()
        if e.source().parentWidget() != self:
            return

    def dragLeaveEvent(self, e):
        e.accept()

    def dropEvent(self, e):

        src = e.source().parentWidget()
        if not src == self and self.tabBar.rect().contains(e.position().toPoint()):
            editor = src.currentWidget()
            src.editors.remove(editor)
            self.setCurrentIndex(self.addEditor(editor, editor.name, editor.icon))
            return
        to_check = self.count()
        e.setDropAction(Qt.DropAction.MoveAction)
        e.accept()
        self.add_split.emit(e.position().toPoint(), src, self)
        if not to_check == self.count():
            return

        counter = self.count()
        tabBar = self.tabBar
        globalPos = self.mapToGlobal(e.position()).toPoint()
        posInTabBar = tabBar.mapFromGlobal(globalPos)
        tab_index = src.indexOf(src.currentWidget())
        for i in range(tabBar.count()):
            if tabBar.tabRect(i).contains(posInTabBar):
                tab_index = i
                break
        new = 0
        if counter == 0:
            if self.currentWidget().icon:
                new = self.addTab(self.currentWidget(), self.currentWidget().icon, self.tabText(self.currentIndex()))
            else:
                new = self.addTab(self.currentWidget(), self.tabText(self.currentIndex()))
        else:
            if self.currentWidget().icon:
                new = self.insertTab(tab_index, self.currentWidget(), self.currentWidget().icon,
                                     self.tabText(self.currentIndex()))
            else:
                new = self.insertTab(tab_index, self.currentWidget(), self.tabText(self.currentIndex()))
        self.setCurrentIndex(new)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.RightButton:
            print('Right button released')
            self.tabBar.removeEventFilter(self)

        super(TabManager, self).mouseReleaseEvent(e)

    def __repr__(self):
        return self.editors.__repr__()
