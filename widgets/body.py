from PyQt6.QtCore import Qt, QSize, QCoreApplication, QEvent
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import (QSplitter, QPushButton, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QApplication)
from widgets.explorer import Explorer
from widgets.tab_manager import TabManager
from widgets.texteditor import TextEditor
from slots import file_slots


class Body(QSplitter):
    def __init__(self):
        super().__init__()

        self.init_side_tab_manager()

        self.explorer: Explorer
        self.init_explorer()
        
        self.__current_tab_manager: TabManager
        self.tab_container: QSplitter
        self.tab_managers: list[TabManager]
        self.init_tabs()

        self.init_parameters()

    def get_current_tab_manager(self):
        return self.__current_tab_manager

    def set_current_tab_manager(self, tab_manager=None):
        self.__current_tab_manager = tab_manager or self.tab_managers[0]

    def get_current_editor(self):
        return self.get_current_tab_manager().currentWidget()

    def add_tab_manager(self, index, editor: TextEditor = None):
        new_manager = TabManager(index)
        new_manager.close_widget.connect(lambda manager: manager.hide())
        self.tab_managers.append(new_manager)
        self.tab_container.insertWidget(index, new_manager)
        self.set_current_tab_manager(new_manager)
        if editor:
            if editor.icon:
                new_manager.addEditor(editor, icon=editor.icon, name=editor.name)
            else:
                new_manager.addEditor(editor, name=editor.name)
        return new_manager

    def add_new_editor(self, path, name: str, extension, tab_manager=None):
        dest = tab_manager or self.get_current_tab_manager()
        if extension == '.py':
            py_icon = QIcon('./resources/pythonlogo.png')
            dest.setCurrentIndex(dest.addEditor(
                TextEditor(path, extension, name=name, icon=py_icon), icon=py_icon, name=name))
        else:
            dest.setCurrentIndex(
                dest.addEditor(TextEditor(path, extension, name=name), name=name))

    def add_editor(self, editor: TextEditor, tab_manager=None):
        dest_manager = tab_manager or self.get_current_tab_manager()
        dest_manager.setCurrentIndex(dest_manager.addEditor(editor, editor.name, editor.icon))

    def init_side_tab_manager(self):
        self.side_tab_manager = QWidget()
        self.side_tab_manager.setFixedWidth(45)
        self.side_tab_manager.setStyleSheet("background-color: #282c34;")
        self.explorer_button = QPushButton()
        self.explorer_button.clicked.connect(lambda e: self.change_explorer_visibility())
        self.explorer_button.setIcon(QIcon('./resources/pngwing.com.png'))
        self.explorer_button.setIconSize(QSize(28, 28))
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.explorer_button, Qt.AlignmentFlag.AlignCenter, Qt.AlignmentFlag.AlignTop)
        self.side_tab_manager.setLayout(self.layout)
        self.addWidget(self.side_tab_manager)

        self.setCollapsible(0, False)

    def init_parameters(self):
        self.setHandleWidth(0)
        self.setStretchFactor(0, 1)
        self.setStretchFactor(1, 20)
        self.setSizes([0, 50, 1620])

    def init_explorer(self):
        self.explorer = Explorer()
        self.addWidget(self.explorer)
        self.explorer.file_tree_view.opened_file_signal.connect(lambda filepath:
                                                                file_slots.open_file(self, filepath))

    def change_explorer_visibility(self):
        if self.explorer.isVisible():
            self.explorer.hide()
        else:
            self.explorer.show()

    def init_tabs(self):
        self.tab_container: QSplitter = QSplitter()
        self.tab_container.setHandleWidth(0)
        self.tab_managers = list()
        self.addWidget(self.tab_container)
        self.add_tab_manager(0)
