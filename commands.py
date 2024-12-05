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
    
    def dana(self, text_edit):
        xmas = "".join(
            [
                "\n\nDear Dana,\n\n",
                "       *       ", "\n",
                "     * * *     ", "\n",
                "    * * * *    ", "\n",
                "   * * * * *   ", "\n",
                "  *  MERRY  *  ", "\n",
                " * CHRISTMAS * ", "\n",
                "* * * * * * * *", "\n",
                "     | | |      ", "\n",
                "     | | |      ", "\n\n",
                "I hope you have a lovely time with your family\n",
                "back in Switzerland and don't miss me too much!! ;)\n\n",
                "Love you lots,\n\nHenry (Henery) \u2665\n"
            ]
        )
        text_edit.updateText(xmas)
        return ""
