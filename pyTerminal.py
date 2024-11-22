import sys
import re
import subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Commands():
    def __init__(self) -> None:
        pass


    def pwd(self):
        # Windows specific
        result = subprocess.run(["cd"], capture_output=True, shell=True, text=True).stdout.strip("\n")
        return result
    

    def dir(self):
        # Windows specfic
        result = subprocess.run(["dir"], capture_output=True, shell=True, text=True).stdout.strip("\n")
        return result


    def echo(self, text):
        if text is None:
            return ""
        result = subprocess.run(f"echo {text}", capture_output=True, shell=True, text=True).stdout.strip("\n")
        if result[0] == '"':
            result = result[1:]
        if result[-1] == '"':
            result = result[:-1]
        return result



class TerminalInput(QTextEdit):
    def __init__(self):
        super().__init__()
        self.cmd = Commands()
        self.setStyleSheet("color: white;")
        self.setFont(QFont("Consolas", 12))
        self.cmd_dict = {
            "pwd":  self.cmd.pwd,
            "echo": self.cmd.echo
        }

        self.updateText("PyTerminal v0.0\n\n")
        self.updateText(f"{self.executeCommand("pwd")}> ")
        

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            text = self.currentText()
            self.updateText(self.executeCommand(text))
            self.updateText(f"{self.executeCommand("pwd")}> ")
            self.returnCursorPos()
        
        super().keyPressEvent(event)


    def executeCommand(self, text):
        if " " not in text:
            # Single word command with no arguments
            return self.cmd_dict[text]()
        cmd, args = text.split(" ", maxsplit=1)

        return self.cmd_dict[cmd](args)


    def updateText(self, text):
        self.append(text)


    def currentText(self):
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
