from widgets.menu import MenuBar
from PyQt6.QtWidgets import (QMainWindow)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QCursor
from constants import constants
from widgets.body import Body
from slots import file_slots


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.menubar: MenuBar
        self.body: Body
        self.init_ui()

        self.init_parameters()

        self.init_slots()

        self.body.get_current_tab_manager().add_split.connect(self.add_split)



    def add_split(self, pos, src_manager, dest_manager):
        tab_bar = dest_manager.tabBar
        editor = src_manager.currentWidget()

        if pos.x() >= dest_manager.rect().center().x() and not tab_bar.rect().contains(pos):
            self.body.add_tab_manager(dest_manager.index + 1, editor)\
                .add_split\
                .connect(self.add_split)
            src_manager.editors.remove(editor)
        elif not tab_bar.rect().contains(pos):
            self.body.add_editor(editor, dest_manager)
            src_manager.editors.remove(editor)

    def init_parameters(self):
        self.setWindowTitle(constants['TITLE'])
        self.showMaximized()
        self.setWindowFlags(Qt.WindowType.Window |
                            Qt.WindowType.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowIcon(QIcon("../resources/logo.png"))

    def init_ui(self):
        self.body = Body()
        self.setCentralWidget(self.body)
        self.init_menu()
        self.init_styling()
        # self.setStyleSheet("background-color: #ffffff")

    def init_menu(self):
        self.menubar = MenuBar()
        self.setMenuBar(self.menubar)

    def init_slots(self):
        self.menubar.save_as_action.triggered.connect(lambda _:
                                                      file_slots.save_file_as(self.body.get_current_tab_manager()))
        self.menubar.open_action.triggered.connect(lambda _:
                                                   file_slots.open_file(self.body))
        self.menubar.save_action.triggered.connect(lambda _: file_slots.save_file(self.body.get_current_editor()))

        self.menubar.open_folder_action.triggered.connect(lambda _:
                                                          file_slots.open_folder(self.body.explorer.file_tree_view))

        self.menubar.new_text_file_action.triggered.connect(lambda _: self.body.add_new_editor(None, "New File", None))

    def init_styling(self):
        self.setStyleSheet(f"background-color: #21252B; border-top-style: none;")
        pass
