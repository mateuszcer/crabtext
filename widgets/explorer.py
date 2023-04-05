from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QSizePolicy, QLabel)

from widgets.file_tree_view import FileTreeView
from PyQt6.QtCore import Qt


class Explorer(QWidget):
    def __init__(self):
        super().__init__()

        self.layout: QVBoxLayout
        self.init_layout()

        self.header: QWidget
        self.init_header()

        self.file_tree_view: FileTreeView
        self.init_file_tree_view()

    def init_file_tree_view(self):
        self.file_tree_view = FileTreeView()
        self.layout.addWidget(self.file_tree_view)

    def init_layout(self):
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.setStyleSheet(f"background-color: #21252B")

    def init_header(self):
        self.header = QWidget()
        self.header_layout = QVBoxLayout()
        self.header_layout.setContentsMargins(5, 0, 0, 0)
        # self.header.setStyleSheet(f'background-color: #E0BAFF')
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.header.setFixedHeight(30)
        self.header_label = QLabel('Explorer')
        self.header_layout.addWidget(self.header_label, Qt.AlignmentFlag.AlignCenter)
        self.header_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.header.setLayout(self.header_layout)
        self.layout.addWidget(self.header)
