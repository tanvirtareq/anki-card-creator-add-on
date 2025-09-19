
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

# --- Logging Setup ---
# Create a logger instance that can be imported by other modules
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Define the log file path within the add-on's folder
log_file = os.path.join(os.path.dirname(__file__), 'addon.log')

# Create a handler to write to the log file, with rotation
handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

# --- Add-on Main Code ---

# Add the vendor directory to the system path for dependencies
vendor_dir = os.path.join(os.path.dirname(__file__), "vendor")
sys.path.insert(0, vendor_dir)

from aqt import mw
from aqt.qt import QAction
from aqt import gui_hooks

# Import the main dialog function from our new file
from .main_dialog import show_main_dialog

def open_card_creator():
    """Function to open our card creator dialog."""
    log.debug("'Add Card' button clicked, opening main dialog.")
    show_main_dialog()


# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

# create a new menu item, "Add Card"
action = QAction("Add Card", mw)
# set it to call open_card_creator when it's clicked
qconnect(action.triggered, open_card_creator)
# and add it to the tools menu
mw.form.menuTools.addAction(action)

