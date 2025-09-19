# __init__.py

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

def setup_button(deck_browser):
    """Add a button to the Deck Browser toolbar."""
    log.debug(f"Setting up button in Deck Browser: {deck_browser}")
    action = QAction("Add Card", deck_browser.bottom_bar)
    action.triggered.connect(open_card_creator)
    deck_browser.bottom_bar.addSeparator()
    deck_browser.bottom_bar.addAction(action)

# Use the official gui_hooks to add the button.
gui_hooks.deck_browser_did_render.append(setup_button)
