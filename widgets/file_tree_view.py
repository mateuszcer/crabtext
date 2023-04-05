from PyQt6.QtWidgets import QTreeView
from model.file_tree_model import FileTreeModel

from PyQt6.QtCore import Qt, pyqtBoundSignal, pyqtSignal




class FileTreeView(QTreeView):
    opened_file_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        self.model: FileTreeModel
        self.init_model()
        self.init_parameters()

    def init_parameters(self):
        self.setHeaderHidden(True)
        self.setWordWrap(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # hide columns
        map(lambda e: self.setColumnHidden(e, True), range(1, self.model.columnCount() + 1))
        for i in range(1, self.model.columnCount()):
            self.header().hideSection(i)

        self.doubleClicked.connect(lambda model_index: self.opened_file_signal.emit(self.model.filePath(model_index)))


    def init_model(self):
        self.model = FileTreeModel()
        self.setModel(self.model)
        self.model.rootPathChanged.connect(lambda path: self.setRootIndex(self.model.index(path)))