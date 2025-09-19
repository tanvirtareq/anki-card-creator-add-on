import os
import logging
from logging.handlers import RotatingFileHandler

# --- Logging Setup ---

# Get the logger instance. Using __package__ ensures the logger is named after the add-on package.
log = logging.getLogger(__package__)

# Define the log file path within the add-on's folder
log_file = os.path.join(os.path.dirname(__file__), 'addon.log')

# Define the debug flag file path
DEBUG_FLAG_FILE = os.path.join(os.path.dirname(__file__), 'DEBUG_LOGGING_ENABLED')

# Clear existing handlers to avoid duplicate logs
if log.hasHandlers():
    log.handlers.clear()

# Conditionally set logging level and add handler
if os.path.exists(DEBUG_FLAG_FILE):
    log.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=3, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
else:
    # If debug flag is not present, disable logging by setting level to CRITICAL
    # and not adding any handlers.
    log.setLevel(logging.CRITICAL)
