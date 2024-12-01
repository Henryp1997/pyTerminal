import sys
import re
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Commands():
    def __init__(self) -> None:
        pass

    def initTerminalText(self, text_edit):
        text_edit.setPlainText("")
        text_edit.updateText("PyTerminal v0.0" + "\n\n")
        text_edit.returnToDefaultInput(move_to_end=True)
        return ""

    def pwd(self, _):
        # Windows specific
        result = subprocess.run(["cd"], capture_output=True, shell=True, text=True).stdout.strip("\n")
        return result
    
    def dir(self, _):
        # Windows specfic
        result = subprocess.run(["dir"], capture_output=True, shell=True, text=True).stdout.strip("\n")
        return result

    def echo(self, text):
        if text is None:
            return ""
        result = subprocess.run(f"echo {text}", capture_output=True, shell=True, text=True).stdout.strip("\n")
        if result[0] in ("'", '"'):
            result = result[1:]
        if result[-1] in ("'", '"'):
            result = result[:-1]
        
        return result
    
    def empty(self):
        return ""
    
    def nonExistent(self, _, cmdstr):
        err = subprocess.run([cmdstr], capture_output=True, shell=True, text=True).stderr.strip("\n")
        return err
    

class TerminalInput(QTextEdit):
    def __init__(self):
        super().__init__()
        self.cmd = Commands()
        self.setStyleSheet("color: white;")
        self.setFont(QFont("Consolas", 12))
        self.cmd_dict = {
            "clear": self.cmd.initTerminalText,
            "pwd":   self.cmd.pwd,
            "echo":  self.cmd.echo,
        }

        self.cmd.initTerminalText(self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            cmd = self.currentInput()
            self.updateText("\n")
            self.updateText(self.executeCommand(cmd))
        
            if cmd != "clear":
                self.updateText("\n")
                self.returnToDefaultInput()
        else:
            # Only call super method if not enter or return. If we use the super method for these keys,
            # they add a newline character to the end of the text which messes up formatting
            super().keyPressEvent(event)

    def returnToDefaultInput(self, move_to_end=True):
        self.updateText(self.executeCommand("pwd"))
        self.updateText("> ", move_to_end=move_to_end)

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

        return self.cmd_dict[cmdstr](args)

    def updateText(self, text, move_to_end=True):
        full_text = (self.toPlainText() + text)
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
