import os
import logging
from logging.handlers import RotatingFileHandler


log = logging.getLogger(__package__)
log.setLevel(logging.DEBUG)

# Define the log file path within the add-on's folder
log_file = os.path.join(os.path.dirname(__file__), 'addon.log')

# Create a handler to write to the log file, with rotation
# 1MB max size, keep 3 backups
handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=3, encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
handler.setFormatter(formatter)

# Clear existing handlers to avoid duplicate logs
if log.hasHandlers():
    log.handlers.clear()

log.addHandler(handler)
