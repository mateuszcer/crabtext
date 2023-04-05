import builtins
import importlib.util
import inspect
import keyword
import multiprocessing
import pkgutil
import re
import sys
import types
import os
from pathlib import Path

from PyQt6.Qsci import QsciLexerCustom, QsciScintilla
from PyQt6.QtGui import QFont, QColor


class PyLexer(QsciLexerCustom):
    Default = 0
    Comment = 1
    Number = 2
    SingleQuotedString = 3
    Identifier = 4
    Keyword = 5
    FunctionMethodName = 6
    ClassName = 7
    Decorator = 8
    Type = 9
    FunctionDefinition = 10
    Bracket = 11
    Constant = 12
    MultiLineComment = 13
    DoubleQuotedString = 14
    # shared among all instances
    Classes = set()
    Keywords = keyword.kwlist + ['self']
    ModulesIncluded = set()
    BuiltinFunctionNames = [
        name
        for name, obj in vars(builtins).items()
        if isinstance(obj, types.BuiltinFunctionType)
    ]
    Visited = set()

    class_finding_pattern = re.compile(r"class\s[a-zA-Z0-9]+:|class\s[a-zA-Z0-9]+\(")

    def __init__(self, parent: QsciScintilla):
        super(PyLexer, self).__init__(parent)
        self.editor: QsciScintilla = parent
        self.pattern = re.compile(r"[*]\/|\/[*]|\s+|\w+|\W")

        if self.editor.filepath:
            self.import_project_files()
            parent_filepath_dir = self.editor.filepath.parents[0]
            for dirpath, dirs, files in os.walk(parent_filepath_dir):
                for filename in files:
                    fname = os.path.join(dirpath, filename)
                    if Path(filename).suffix == '.py' and filename not in PyLexer.Visited:
                        with open(fname) as myfile:
                            content = myfile.read()
                            for classname in re.findall(PyLexer.class_finding_pattern, content):
                                PyLexer.Classes.add(classname.split(" ")[1][:-1])
                            PyLexer.Visited.add(filename)

        # Default text settings
        # ----------------------
        self.setDefaultColor(QColor("#ABB2BF"))
        self.setDefaultPaper(QColor("#282c34"))
        self.setDefaultFont(QFont("JetBrains Mono", 14, QFont.Weight.Normal))

        # Initialize colors per style
        # ----------------------------
        self.setColor(QColor('#61AFEF'), PyLexer.FunctionMethodName)  # 98c379
        self.setColor(QColor('#c678dd'), PyLexer.Keyword)
        self.setColor(QColor('#e5c07b'), PyLexer.ClassName)
        self.setColor(QColor('#ABB2BF'), PyLexer.Identifier)  # #FF69B4
        self.setColor(QColor('#98c379'), PyLexer.SingleQuotedString)
        self.setColor(QColor('#98c379'), PyLexer.DoubleQuotedString)
        self.setColor(QColor('#fffa83'), PyLexer.Decorator)
        self.setColor(QColor('#6b6e75'), PyLexer.Comment)
        self.setColor(QColor('#ABB2BF'), PyLexer.Bracket)
        self.setColor(QColor('#F2A777'), PyLexer.Number)
        self.setColor(QColor('#98c379'), PyLexer.MultiLineComment)

    @staticmethod
    def update_module_classes(module_name: str) -> None:
        try:
            importlib.import_module(module_name)
        except ModuleNotFoundError:
            pass
        try:
            for name, obj in inspect.getmembers(sys.modules[module_name]):
                if inspect.isclass(obj):
                    PyLexer.Classes.add(name)
            PyLexer.ModulesIncluded.add(module_name)
        except KeyError:
            pass

    def import_python_file(self, child):
        spec = importlib.util.spec_from_file_location(str(child.stem), str(child))
        foo = importlib.util.module_from_spec(spec)
        sys.modules[str(child.stem)] = foo
        #spec.loader.exec_module(foo)

    def import_project_files(self):
        parent_filepath_dir = self.editor.filepath.parents[0]
        if parent_filepath_dir not in sys.path:
            sys.path.append(parent_filepath_dir)
            for child in parent_filepath_dir.iterdir():
                try:
                    if child.is_dir():
                        importlib.import_module(str(child.stem), str(parent_filepath_dir))
                        pass
                    elif child.suffix == '.py':
                        p = multiprocessing.Process(target=lambda: self.import_python_file(child))
                        p.start()
                        p.join(1)
                        if p.is_alive():
                            print("Importing terminated")
                            p.terminate()
                            p.join()

                except ModuleNotFoundError:
                    pass

    def language(self):
        return "PythonCustom"

    def description(self, style):
        if style == PyLexer.Default:
            return "Default"
        elif style == PyLexer.Keyword:
            return "Keyword"
        elif style == PyLexer.Type:
            return "Type"
        elif style == PyLexer.SingleQuotedString:
            return "Single quoted string"
        elif style == PyLexer.DoubleQuotedString:
            return "Double quoted string"
        elif style == PyLexer.Bracket:
            return "Bracket"
        elif style == PyLexer.Comment:
            return "Comment"
        elif style == PyLexer.Constant:
            return "Constant"
        elif style == PyLexer.FunctionMethodName:
            return "FunctionMethodName"
        elif style == PyLexer.ClassName:
            return "ClassName"
        elif style == PyLexer.FunctionDefinition:
            return "FunctionDefinition"
        elif style == PyLexer.Identifier:
            return "Identifier"
        elif style == PyLexer.Number:
            return "Number"
        elif style == PyLexer.MultiLineComment:
            return "MultiLineComment"
        return ""

    def last_style(self, current):
        return self.editor.SendScintilla(self.editor.SCI_GETSTYLEAT, current - 1)

    def get_next_token(self, token_list: list[tuple], index: int) -> tuple[str, int]:
        while token_list[index + 1][0].isspace():
            index += 1
        return token_list[index + 1]

    def has_next_token(self, token_list: list[tuple], index: int) -> bool:
        try:
            while token_list[index + 1][0].isspace():
                index += 1
            return True
        except IndexError:
            return False

    def get_module_name(self, token_list: list[tuple], index: int):
        while index+1 < len(token_list) and token_list[index + 1][0].isspace():
            index += 1
        if index + 3 < len(token_list) and token_list[index + 2][0] == '.':
            return (token_list[index + 1][0]+'.'+token_list[index+3][0],
                    token_list[index + 1][1]+token_list[index + 1][1]+token_list[index+3][1])
        return token_list[index + 1]

    def styleText(self, start, end):
        self.startStyling(start)

        text = self.editor.text()[start:end]
        token_list = [(token, len(bytearray(token, "utf-8"))) for token in self.pattern.findall(text)]
        multiline_comm_flag = False
        double_quoted_string_flag = False
        single_quoted_string_flag = False
        comm_flag = False

        if start > 0:
            if self.last_style(start) == PyLexer.MultiLineComment:
                multiline_comm_flag = True
            elif self.last_style(start) == PyLexer.SingleQuotedString:
                single_quoted_string_flag = True
            elif self.last_style(start) == PyLexer.DoubleQuotedString:
                double_quoted_string_flag = True
            # 4.
        # 4.2 Style the text in a loop

        for i, token in enumerate(token_list):
            if double_quoted_string_flag:
                self.setStyling(token[1], PyLexer.DoubleQuotedString)
                if token[0] == '"':
                    double_quoted_string_flag = False
            elif single_quoted_string_flag:
                self.setStyling(token[1], PyLexer.SingleQuotedString)
                if token[0] == "'":
                    single_quoted_string_flag = False
            elif multiline_comm_flag:
                self.setStyling(token[1], PyLexer.Comment)
                if token[0] == "*/":
                    multiline_comm_flag = False

            elif comm_flag:
                self.setStyling(token[1], PyLexer.Comment)
                if '\n' in token[0]:
                    comm_flag = False
            else:

                if token[0] == '"':
                    double_quoted_string_flag = True
                    self.setStyling(token[1], PyLexer.DoubleQuotedString)
                elif token[0] == "'":
                    single_quoted_string_flag = True
                    self.setStyling(token[1], PyLexer.SingleQuotedString)

                elif token[0] == "/*":
                    multiline_comm_flag = True
                    self.setStyling(token[1], PyLexer.Comment)

                elif token[0] == "#":
                    comm_flag = True
                    self.setStyling(token[1], PyLexer.Comment)

                elif self.has_next_token(token_list, i) and (token[0] == 'from' or token[0] == 'import'):
                    module_name = self.get_module_name(token_list, i)[0]
                    if module_name not in PyLexer.ModulesIncluded:
                        PyLexer.update_module_classes(module_name)
                    self.setStyling(token[1], PyLexer.Keyword)

                elif token[0] in PyLexer.Classes:
                    self.setStyling(token[1], PyLexer.ClassName)

                elif token[0] == 'class':
                    if self.has_next_token(token_list, i):
                        new_class_name_token = self.get_next_token(token_list, i)
                        PyLexer.Classes.add(new_class_name_token[0])
                    self.setStyling(token[1], PyLexer.Keyword)

                elif i + 1 < len(token_list) and token_list[i + 1][0] == '(':
                    self.setStyling(token[1], PyLexer.FunctionMethodName)

                elif token[0] in PyLexer.Keywords:
                    self.setStyling(token[1], PyLexer.Keyword)

                elif token[0] in PyLexer.BuiltinFunctionNames:
                    self.setStyling(token[1], PyLexer.FunctionMethodName)

                elif token[0] in ["(", ")", "{", "}", "[", "]"]:
                    self.setStyling(token[1], PyLexer.Bracket)

                elif token[0].isnumeric():
                    self.setStyling(token[1], PyLexer.Number)

                else:
                    self.setStyling(token[1], PyLexer.Identifier)
