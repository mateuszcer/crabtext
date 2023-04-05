from PyQt6.QtWidgets import QApplication, QTabBar
from widgets.mainwindow import MainWindow
import sys

from widgets.tab_manager import TabManager
from widgets.texteditor import TextEditor


class CrapText(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.window = MainWindow()
        self.focusChanged.connect(self.set_tab_manager)

    def set_tab_manager(self, old, new):
        try:
            if isinstance(new, QTabBar):
                self.window.body.set_current_tab_manager(new.parentWidget())
            elif isinstance(new, TextEditor):
                self.window.body.set_current_tab_manager(new.get_parent_manager())
            # elif isinstance(old, TextEditor):
            #     self.window.body.set_current_tab_manager(old.get_parent_manager())
            # elif isinstance(old, QTabBar):
            #     self.window.body.set_current_tab_manager(old.parentWidget())
        except AttributeError:
            pass

    def run(self):
        self.window.show()
        sys.exit(self.exec())
