# __init__.py

import os
import sys

# Add the vendor directory to the system path
vendor_dir = os.path.join(os.path.dirname(__file__), "vendor")
sys.path.insert(0, vendor_dir)

from aqt import mw
from aqt.qt import QAction

# Handle changing hook location in different Anki versions
try:
    # Anki 2.1.50+ (and development versions)
    from anki.hooks import deck_browser_toolbar_did_init
except ImportError:
    # Older Anki versions
    from aqt.hooks import deck_browser_toolbar_did_init

# Import the main dialog function from our new file
from .main_dialog import show_main_dialog

def open_card_creator():
    """Function to open our card creator dialog."""
    show_main_dialog()

def setup_button(deck_browser):
    """Add a button to the Deck Browser toolbar."""
    action = QAction("Add Card", deck_browser)
    action.triggered.connect(open_card_creator)
    # Add it to the right of the existing buttons
    deck_browser.toolbar.addSeparator()
    deck_browser.toolbar.addAction(action)

# Use the official hook to add the button
deck_browser_toolbar_did_init.append(setup_button)
