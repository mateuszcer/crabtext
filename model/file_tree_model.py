from PyQt6.QtGui import QFileSystemModel


class FileTreeModel(QFileSystemModel):
    def __init__(self):
        super().__init__()

        self.current_path: str
        self.init_parameters()

    def init_parameters(self):
        self.current_path = ''
        self.setRootPath(self.current_path)
        self.setNameFilterDisables(True)

    def change_path(self, path):
        self.setRootPath(path)
        self.current_path = path
