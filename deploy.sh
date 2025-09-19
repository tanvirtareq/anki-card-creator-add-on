#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
# The name of the main Anki application.
ANKI_APP_NAME="Anki"

# The name of your add-on folder.
ADDON_FOLDER_NAME="AnkiCardCreatorAddon"

# --- Paths ---
# The full path to your Anki add-ons directory.
ADDONS_DIR="${HOME}/Library/Application Support/Anki2/addons21"

# The path to the source code of your add-on in your project.
SOURCE_DIR="$(pwd)/${ADDON_FOLDER_NAME}"

# The full path to the destination where the add-on will be installed.
DEST_DIR="${ADDONS_DIR}/${ADDON_FOLDER_NAME}"

# --- Script Start ---

echo "Starting Anki add-on deployment..."

# 1. Quit Anki
echo "Attempting to quit Anki..."
# Use pkill to find and kill the process. The `|| true` prevents the script from failing if Anki isn't running.
pkill -f "${ANKI_APP_NAME}" || true
# Wait a moment for the process to terminate completely.
sleep 1

# 2. Remove old add-on version
if [ -d "${DEST_DIR}" ]; then
    echo "Removing old add-on version from: ${DEST_DIR}"
    rm -rf "${DEST_DIR}"
else
    echo "No old version to remove."
fi

# 3. Copy new add-on version
echo "Copying add-on from ${SOURCE_DIR} to ${ADDONS_DIR}"
cp -R "${SOURCE_DIR}" "${ADDONS_DIR}/"

# 4. Install dependencies
echo "Installing dependencies into the new add-on's vendor folder..."
# Important: Change directory to the *destination* to run pip
cd "${DEST_DIR}"

if [ -f "requirements.txt" ]; then
    # Ensure the vendor directory exists
    mkdir -p vendor
    pip3 install -r requirements.txt -t ./vendor > /dev/null 2>&1
    echo "Dependencies installed."
else
    echo "Warning: requirements.txt not found. Skipping dependency installation."
fi

# 5. Restart Anki
echo "Restarting Anki..."
open "/Applications/${ANKI_APP_NAME}.app"

echo "Deployment complete!"

# 6. Tail the log file
LOG_FILE="${DEST_DIR}/addon.log"
echo "
--- Tailing log file: ${LOG_FILE} ---
Press Ctrl+C to stop.
"

# Ensure log file exists before tailing
touch "${LOG_FILE}"
tail -f "${LOG_FILE}"
