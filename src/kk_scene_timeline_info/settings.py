import os
import sys
from typing import List

if getattr(sys, "frozen", False):
    # If the application is run as a bundle, the PyInstaller bootloader
    # sets the sys._MEIPASS attribute to the path of the bundle.
    if os.path.basename(os.path.dirname(sys.executable)) == "bin":
        WORKDIR = os.path.dirname(os.path.dirname(sys.executable))
    else:
        WORKDIR = os.path.dirname(sys.executable)
    IS_DEV = False
else:
    # If the application is run as a script, use the directory of the script.
    WORKDIR = os.path.abspath(os.path.dirname(__file__))
    IS_DEV = True

CONFIG_PATH = os.path.join(WORKDIR, "config.toml")