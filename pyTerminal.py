import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from commands import Commands

class TerminalInput(QTextEdit):
    def __init__(self):
        super().__init__()
        self.cmd = Commands()
        self.current_dir = os.getcwd()
        self.font = "Cascadia Code"
        self.font_size = 12
        self.cmd_dict = {
            "clear": self.cmd.initTerminalText,
            "cls":   self.cmd.initTerminalText,
            "pwd":   self.cmd.pwd,
            "echo":  self.cmd.echo,
            "dir":   self.cmd.dir,
            "ls":    self.cmd.dir,
            "dana":  self.cmd.dana
        }

        self.setStyleSheet("color: white;")
        self.setFont(QFont(self.font, self.font_size))
        self.cmd.initTerminalText(self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            cmd = self.currentInput()
            self.updateText("\n")
            self.updateText(self.executeCommand(cmd))
        
            if cmd == "":
                # Simple enter press
                self.returnToDefaultInput()
            elif cmd not in ("clear", "cls"):
                self.updateText("\n\n")
                self.returnToDefaultInput()
        else:
            # Only call super method if not enter or return. If we use the super method for these keys,
            # they add a newline character to the end of the text which messes up formatting
            if event.key() == Qt.Key_Backspace:
                print("yes")
            super().keyPressEvent(event)

    def wheelEvent(self, event):
        if event.modifiers() and Qt.ControlModifier:
            self.adjustFontSize(direction=event.angleDelta().y())
        else:
            super().wheelEvent(event)
    
    def adjustFontSize(self, direction):
        if direction < 0:
            self.font_size -= 1
            self.setFont(QFont(self.font, self.font_size))
        elif direction > 0:
            self.font_size += 1
            self.setFont(QFont(self.font, self.font_size))

    def returnToDefaultInput(self):
        self.updateText(self.current_dir)
        self.updateText("> ")

    def executeCommand(self, cmdstr):
        if " " not in cmdstr:
            # Single word command with no arguments
            if cmdstr == "":
                return self.cmd.empty()
            command = self.cmd_dict.get(cmdstr, None)
            if command is None:
                return self.cmd.nonExistent(self, cmdstr)

            return command(self)
        
        # Command with args
        cmdstr, args = cmdstr.split(" ", maxsplit=1)

        command = self.cmd_dict.get(cmdstr, None)
        if command is None:
            return self.cmd.nonExistent(self, cmdstr)

        return self.cmd_dict[cmdstr](args)

    def updateText(self, text):
        full_text = (self.toPlainText() + text)
        self.setPlainText(full_text)

        self.moveCursor(QTextCursor.End)

    def currentInput(self):
        try:
            text = self.toPlainText().splitlines()[-1].split("> ")[1]
        except IndexError:
            text = ""
        return text
    
    def returnCursorPos(self):
        event = QKeyEvent(QEvent.KeyPress, Qt.Key_Up, Qt.NoModifier)
        QApplication.postEvent(self, event)
        event = QKeyEvent(QEvent.KeyPress, Qt.Key_End, Qt.NoModifier)
        QApplication.postEvent(self, event)

    def moveDown(self, ntimes=1):
        for i in range(ntimes):
            event = QKeyEvent(QEvent.KeyPress, Qt.Key_Down, Qt.NoModifier)
            QApplication.postEvent(self, event)


class SyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        self.highlight_rules = []
        self.defineStringColour()
        self.defineKeywordColour()

    def defineStringColour(self):
        # Define a QTextCharFormat for strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#22FF22"))
        self.highlight_rules.append((r'".*?"', string_format))
        self.highlight_rules.append((r"'.*?'", string_format))
        
    def defineKeywordColour(self):
        # Define a QTextCharFormat for keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#34d5eb"))
        keyword_format.setFontWeight(QFont.Bold)

        # Keywords to highlight
        keywords = ["echo"]
        for keyword in keywords:
            pattern = f"\\b{keyword}\\b"
            self.highlight_rules.append((pattern, keyword_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.highlight_rules:
            expression = QRegularExpression(pattern)
            match_iterator = expression.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, fmt)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window properties
        self.setWindowTitle("PyTerminal")
        self.setGeometry(100, 100, 1000, 600)  # x, y, width, height
        self.setStyleSheet("background-color: #0C0C0C; border: none")

        self.text_edit = TerminalInput()
        self.highlighter = SyntaxHighlighter(self.text_edit.document())
        
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(self.text_edit)

    def trigger_rehighlight(self):
        # Force the syntax highlighter to reapply highlighting
        self.highlighter.rehighlight()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create an instance of the window
    window = MainWindow()
    window.show()

    # Execute the application
    sys.exit(app.exec_())
