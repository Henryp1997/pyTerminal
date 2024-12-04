import os
import subprocess

class Commands():
    def __init__(self) -> None:
        pass

    def initTerminalText(self, text_edit):
        text_edit.setPlainText("")
        text_edit.updateText("PyTerminal v0.0" + "\n\n")
        text_edit.returnToDefaultInput()
        return ""

    def pwd(self, text_edit):
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
