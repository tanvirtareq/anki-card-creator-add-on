import os
import sys

from .logger import log

# Add the vendor directory to the system path for dependencies
vendor_dir = os.path.join(os.path.dirname(__file__), "vendor")
sys.path.insert(0, vendor_dir)

from aqt import mw
from aqt.qt import *
from aqt.utils import qconnect

from .main_dialog import show_main_dialog

def open_card_creator():
    """Function to open our card creator dialog."""
    log.debug("'Add Card' menu item clicked, opening main dialog.")
    show_main_dialog()

action = QAction("Add Card", mw)
qconnect(action.triggered, open_card_creator)
mw.form.menuTools.addAction(action)
