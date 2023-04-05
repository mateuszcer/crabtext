from pathlib import Path
from PyQt6.QtWidgets import QFileDialog
import sys

def save_file_as(tab_manager):
    filepath, selected_filter = QFileDialog.getSaveFileName()

    filepath = Path(filepath)
    current_editor = tab_manager.currentWidget()
    try:
        with open(filepath, 'w') as f:
            f.write(current_editor.text())
            current_editor.extension = filepath.suffix
            current_editor.filepath = filepath
            tab_manager.change_current_text(filepath.name)
    except FileNotFoundError:
        pass
    except IsADirectoryError:
        pass


def open_file(body, filepath=None):
    retain_focus = body.get_current_tab_manager()
    if not filepath:
        filepath, selected_filter = QFileDialog.getOpenFileName()
    filepath = Path(filepath)
    if filepath.is_dir():
        return
    body.add_new_editor(filepath, filepath.name, filepath.suffix, retain_focus)
    current_editor = retain_focus.currentWidget()

    try:
        with open(filepath, 'r') as f:
            current_editor.insert(f.read())
    except FileNotFoundError:
        pass


def save_file(current_editor):
    if not current_editor.filepath:
        save_file_as(current_editor.parent().parent())
        return
    filepath = Path(current_editor.filepath)
    try:
        with open(filepath, 'w') as f:
            f.write(current_editor.text())
    except FileNotFoundError:
        pass


def open_folder(tree_view):
    filepath = QFileDialog.getExistingDirectory()
    tree_view.model.setRootPath(filepath)

