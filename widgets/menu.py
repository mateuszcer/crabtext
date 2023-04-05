from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenuBar

class MenuBar(QMenuBar):
    def __init__(self):
        super().__init__()

        self.save_as_action = None
        self.open_action = None
        self.save_action = None
        self.open_folder_action = None

        self.file_menu = None
        self.init_file_menu()

        self.edit_menu = None
        self.init_edit_menu()

        self.view_menu = None
        self.init_view_menu()

        self.run_menu = None
        self.init_run_menu()

        self.setStyleSheet(" border-style: solid; border-width: 0px 3px;")

    def init_file_menu(self):
        self.file_menu = self.addMenu('&File')

        self.new_text_file_action = QAction("New Text File", self)
        self.new_text_file_action.setShortcut("Ctrl+N")
        self.file_menu.addAction(self.new_text_file_action)

        self.save_action = QAction("Save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.file_menu.addAction(self.save_action)

        self.save_as_action = QAction("Save as", self)
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        self.file_menu.addAction(self.save_as_action)

        self.open_action = QAction("Open File", self)
        self.open_action.setShortcut("Ctrl+O")
        self.file_menu.addAction(self.open_action)

        self.open_folder_action = QAction("Open Folder", self)
        self.open_folder_action.setShortcut("Ctrl+K")
        self.file_menu.addAction(self.open_folder_action)



        self.file_menu.addSeparator()

    def init_edit_menu(self):
        self.edit_menu = self.addMenu('&Edit')

    def init_view_menu(self):
        self.view_menu = self.addMenu('&View')

    def init_run_menu(self):
        self.run_menu = self.addMenu('R&un')

