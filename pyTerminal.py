import sys
import re
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Commands():
    def __init__(self) -> None:
        pass


    def pwd(self, _):
        # Windows specific
        result = subprocess.run(["cd"], capture_output=True, shell=True, text=True).stdout.strip("\n")
        return result
    

    def dir(self, _):
        # Windows specfic
        result = subprocess.run(["dir"], capture_output=True, shell=True, text=True).stdout.strip("\n")
        return result


    def initTerminalText(self, text_edit, n_newlines=1, pwd=False):
        text_edit.setPlainText("")
        text_edit.updateText("PyTerminal v0.0" + "\n" * n_newlines)
        text_edit.returnToInput(move_to_end=True, pwd=pwd)
        return ""


    def echo(self, text):
        if text is None:
            return ""
        result = subprocess.run(f"echo {text}", capture_output=True, shell=True, text=True).stdout.strip("\n")
        if result[0] in ("'", '"'):
            result = result[1:]
        if result[-1] in ("'", '"'):
            result = result[:-1]
        
        return result


class TerminalInput(QTextEdit):
    def __init__(self):
        super().__init__()
        self.cmd = Commands()
        self.setStyleSheet("color: white;")
        self.setFont(QFont("Consolas", 12))
        self.cmd_dict = {
            "clear": self.cmd.initTerminalText,
            "pwd":   self.cmd.pwd,
            "echo":  self.cmd.echo
        }

        self.cmd.initTerminalText(self, n_newlines=2, pwd=True)


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            cmd = self.currentInput()
            self.updateText("\n")
            self.updateText(self.executeCommand(cmd))
            self.updateText("\n")
            self.returnToInput()
            self.returnCursorPos()
        
        super().keyPressEvent(event)
        print(repr(self.toPlainText()))


    def returnToInput(self, move_to_end=True, pwd=True):
        if pwd:
            self.updateText(self.executeCommand("pwd"))
            self.updateText("> ", move_to_end=move_to_end)


    def executeCommand(self, cmd):
        if " " not in cmd:
            # Single word command with no arguments
            return self.cmd_dict[cmd](self)
        cmd, args = cmd.split(" ", maxsplit=1)

        return self.cmd_dict[cmd](args)


    def updateText(self, text, move_to_end=True):
        full_text = (self.toPlainText() + text).lstrip("\n")
        self.setPlainText(full_text)

        if move_to_end:
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window properties
        self.setWindowTitle("PyTerminal")
        self.setGeometry(100, 100, 800, 400)  # x, y, width, height

        self.setStyleSheet("background-color: black;")

        self.text_edit = TerminalInput()
        

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(self.text_edit)

    

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create an instance of the window
    window = MainWindow()
    window.show()

    # Execute the application
    sys.exit(app.exec_())
