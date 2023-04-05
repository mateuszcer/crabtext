import keyword
import pkgutil
from pathlib import Path

from PyQt6.Qsci import QsciScintilla, QsciLexerCPP, QsciLexerPython, QsciAPIs
from PyQt6.QtCore import *
from PyQt6.QtGui import *

from widgets.pylexer import PyLexer

class TextEditor(QsciScintilla):

    def __init__(self, filepath, extension, name: str = None, icon: QIcon = None):
        super().__init__()
        self.filepath = filepath
        self.extension = extension
        self.lexer = None
        self.icon = icon
        self.name = name
        self.__parent_manager = None

        if self.extension == '.py':
            self.lexer = PyLexer(self)
            # Api
            self.__api = QsciAPIs(self.lexer)
            for key in keyword.kwlist + dir(__builtins__):
                self.__api.add(key)

            for _, name, _ in pkgutil.iter_modules():
                self.__api.add(name)

            self.__api.prepare()
            if self.lexer:
                self.lexer.setAPIs(self.__api)

        if self.lexer:
            self.setLexer(self.lexer)
            
        self.setUtf8(True)  # Set encoding to UTF-8
        self.setFont(QFont('JetBrains Mono', 14, QFont.Weight.Normal))
        # brace matching
        self.setMarginType(2, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "1000")
        color = QColor("#6b6e75")
        self.setMarginsForegroundColor(color)
        self.setMarginsBackgroundColor(QColor("#00282c34"))
        self.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
        self.setStyleSheet(f'border-style: none; background-color: #282c34;')
        # indentation
        self.setIndentationGuides(False)
        self.setTabWidth(4)
        self.setIndentationsUseTabs(False)
        self.setAutoIndent(True)
        self.setCaretForegroundColor(QColor("#ffffff"))
        self.setCaretLineBackgroundColor(QColor("#0A99bbff"))
        self.setCaretLineVisible(True)
        self.setCaretWidth(2)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAll)
        self.setAutoCompletionThreshold(1)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionUseSingle(QsciScintilla.AutoCompletionUseSingle.AcusNever)


        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)


    def __repr__(self):
        return f"{self.name}"

    def __str__(self):
        return f"{self.name}"

    def set_parent_manager(self, parent_manager):
        self.__parent_manager = parent_manager

    def get_parent_manager(self):
        return self.__parent_manager


