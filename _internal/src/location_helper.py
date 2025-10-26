## NOTE: this is just for pyinstaller fix

import sys
import pathlib

def project_root():
    if getattr(sys, 'frozen', False):
        return pathlib.Path(sys._MEIPASS)
    return pathlib.Path(__file__).resolve().parent.parent
