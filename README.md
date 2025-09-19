# Anki Card Creator Add-on

## 1. What this Add-on Does

This Anki add-on provides a streamlined way to create rich flashcards directly within your Anki application. It supports two distinct card types, automatically fetches dictionary data, translates it to Bangla, and handles media, making card creation efficient and comprehensive.

**Key Features:**

*   **Integrated UI:** A dedicated "Add Card" button appears in Anki's Deck Browser for quick access.
*   **Adds to Current Deck:** New cards are automatically added to the deck you are currently viewing in Anki.
*   **Two Card Types:**
    *   **Simple Audio:** A basic card with audio on the front and the word/phonetic transcription on the back.
    *   **Spelling Rescue:** An interactive card designed for spelling practice. The front features audio and a text input field for the user to type the word. The back displays the correct word, its meaning (English & Bangla), synonyms (English & Bangla), and usage in a sentence (English & Bangla).
*   **Automatic Data Fetching & Translation:** For "Spelling Rescue" cards, the add-on automatically retrieves word definitions, synonyms, and example sentences from a dictionary API and translates them to Bangla.
*   **Automatic Model Creation:** The necessary Anki Note Types ("Simple Audio Model" and "Spelling Rescue Model") are automatically created in your collection if they don't already exist.
*   **Seamless Media Handling:** Generated audio files are automatically added to your Anki collection's media folder, ensuring they work across devices.

## 2. How to Use

1.  **Open Anki:** Launch your Anki Desktop application.
2.  **Navigate to Deck Browser:** Go to the main screen where all your decks are listed.
3.  **Click "Add Card":** A new "Add Card" button will be visible on the bottom toolbar of the Deck Browser. Click it.
4.  **Create Your Card:** A dedicated "Anki Card Creator" window will appear:
    *   Enter the English word or phrase you wish to create a card for.
    *   Select the desired card type from the dropdown menu: "Simple Audio" or "Spelling Rescue".
    *   Click the "Create Card" button.
5.  **Card Added:** The new card will be automatically added to the deck you were viewing when you clicked the "Add Card" button.

## 3. Setup (For Developers/Contributors)

This section is for setting up the project for development or if you wish to manually install the add-on.

**Requirements:**

*   [Python 3](https://www.python.org/downloads/) (3.8+ recommended)
*   Anki Desktop application (version 2.1.20+ recommended, though tested with 25.07.5 development build)
*   An active internet connection (required for audio generation, dictionary lookups, and translations).

**Gemini API Key Setup:**

To use the Gemini-powered features, you need to provide your Gemini API key.

1.  **Create a `.env` file:** In the `AnkiCardCreatorAddon/` directory, create a new file named `.env`.
2.  **Add your API key:** Open the `.env` file and add your Gemini API key in the following format:
    ```
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    ```
    Replace `"YOUR_GEMINI_API_KEY"` with your actual Gemini API key.

**Project Structure:**

```
Anki Card Creator/
├── AnkiCardCreatorAddon/  # The main add-on folder
│   ├── __init__.py        # Add-on entry point and setup
│   ├── main_dialog.py     # UI and core card creation logic
│   ├── logger.py          # Centralized logging configuration
│   ├── requirements.txt   # Python dependencies for the add-on
│   ├── vendor/            # Directory for vendored (bundled) Python libraries
│   └── card_creator/      # Package containing card creation factory and classes
│       ├── __init__.py
│       └── card_creators.py
└── deploy.sh              # Script for easy deployment (macOS)
```

## 4. How to Add this Add-on to Anki

To install this add-on into your Anki application:

1.  **Close Anki:** Ensure your Anki Desktop application is completely closed before proceeding.

2.  **Find Your Anki Add-ons Folder:**
    *   Open Anki (temporarily, if closed).
    *   Go to `Tools > Add-ons`.
    *   Click the `View Files` button at the bottom. This will open your Anki add-ons folder in your system's file explorer.
    *   The typical path is `~/Library/Application Support/Anki2/addons21` on macOS, or similar on other operating systems.

3.  **Copy the Add-on Folder:**
    *   Copy the entire `AnkiCardCreatorAddon` folder (from where you cloned/downloaded this project) into the add-ons folder you just opened in step 2.

4.  **Install Dependencies:**
    *   This add-on bundles its Python dependencies. You need to install them into the add-on's `vendor` subfolder.
    *   Open your terminal or command prompt.
    *   Navigate into the `AnkiCardCreatorAddon` folder that you just copied into Anki's add-ons directory. For example:
        ```bash
        cd "~/Library/Application Support/Anki2/addons21/AnkiCardCreatorAddon"
        ```
    *   Run the following command to install the dependencies:
        ```bash
        pip3 install -r requirements.txt -t ./vendor
        ```
        *(Note: Use `pip` instead of `pip3` if your system's default Python 3 `pip` command is just `pip`.)*

5.  **Start Anki:** Launch the Anki application. The add-on should now be active and the "Add Card" button visible in the Deck Browser.

## 5. How to Use `deploy.sh` (macOS)

The `deploy.sh` script is a convenience tool for macOS users to quickly install, update, and test the add-on during development. It automates quitting Anki, copying the latest code, installing dependencies, and restarting Anki.

1.  **Make Executable:** If you haven't already, make the script executable:
    ```bash
    chmod +x deploy.sh
    ```

2.  **Run the Script:**
    *   **Standard Deployment:** To deploy the add-on without live logging:
        ```bash
        ./deploy.sh
        ```
    *   **Debug Deployment (with Live Log):** To deploy the add-on and see its live log output in your terminal (useful for debugging):
        ```bash
        ./deploy.sh --debug
        ```
        *   When running in debug mode, the terminal will display the `addon.log` file's content live. Press `Ctrl+C` in the terminal to stop tailing the log (this will not close Anki).

**What `deploy.sh` does:**

*   Gracefully quits Anki (force-quits if necessary).
*   Removes any previous installation of the `AnkiCardCreatorAddon` from your Anki add-ons folder.
*   Copies the latest `AnkiCardCreatorAddon` from your project directory to Anki's add-ons folder.
*   Installs all required Python dependencies into the `vendor/` subfolder within the copied add-on.
*   Restarts Anki.
*   If `--debug` is used, it enables detailed logging within the add-on and displays the `addon.log` file's content in your terminal.
