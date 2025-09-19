# Anki Card Creator Add-on

This is an Anki add-on that lets you quickly create feature-rich flashcards from within the Anki application.

## Features

-   **Integrated UI:** A new "Add Card" button appears in the Deck Browser for quick access.
-   **Adds to Current Deck:** Automatically adds the newly created card to the deck you are currently viewing.
-   **Two Card Types:**
    -   **Simple Audio:** A basic card with audio on the front and the word/phonetics on the back.
    -   **Spelling Rescue:** An interactive card with audio and a text box on the front. The back includes the answer, definitions, synonyms, and an example sentence, all with Bangla translations.
-   **Automatic Model Creation:** The required Anki Note Types ("Simple Audio Model" and "Spelling Rescue Model") are created automatically if they don't exist.
-   **Automatic Data Fetching & Translation:** For Spelling Rescue cards, it automatically fetches data from a dictionary and translates it to Bangla.
-   **Seamless Media Handling:** Audio files are automatically added to your Anki collection's media folder.

## Requirements

-   Anki Desktop application (version 2.1.20+ recommended).
-   An active internet connection (for dictionary lookup and translation).

## Installation

1.  **Close Anki:** Make sure Anki is not running.

2.  **Find Your Add-ons Folder:**
    -   Open Anki, go to `Tools > Add-ons`.
    -   Click the `View Files` button. This will open your Anki add-ons folder in your file explorer.
    -   The path is usually something like `Documents/Anki2/addons21` or `~/Library/Application Support/Anki2/addons21`.

3.  **Copy the Add-on:**
    -   Copy the entire `AnkiCardCreatorAddon` folder from this project into the add-ons folder you just opened.

4.  **Install Dependencies:**
    -   This add-on requires external Python libraries. You need to install them directly into the add-on's `vendor` folder.
    -   Open your terminal or command prompt and run the following commands:
    ```bash
    # Navigate to the add-on folder you just copied
    cd "/path/to/your/Anki2/addons21/AnkiCardCreatorAddon"

    # Install the dependencies from requirements.txt into the 'vendor' subfolder
    pip install -r requirements.txt -t ./vendor
    ```
    - The add-on is configured to automatically load these libraries from the `vendor` folder upon startup.

5.  **Start Anki:** Start the Anki application. The add-on will now be active.

## How to Use

1.  **Open Anki:** Start the Anki application.
2.  **Go to Deck Browser:** The main screen showing all your decks.
3.  **Click "Add Card":** A new "Add Card" button will be visible on the bottom toolbar. Click it.
4.  **Create Your Card:** The Card Creator window will open. Enter a word, select the card type, and click "Create Card".
5.  **Done:** The card will be automatically added to the deck you were viewing.

## Project Files

- `AnkiCardCreatorAddon/`
  - `__init__.py`: The main entry point that loads the add-on and its dependencies.
  - `main_dialog.py`: Contains all the UI and logic for the card creator window.
  - `requirements.txt`: A list of the Python libraries the add-on needs.
  - `vendor/`: The folder where the dependencies are installed.