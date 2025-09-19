# Anki Card Creator

A simple desktop application to quickly create Anki flashcards with audio, phonetic transcription, definitions, and translations.

## Features

-   **Cross-Platform:** Runs on Windows, macOS, and Linux.
-   **Two Card Types:**
    -   **Simple Audio:** A basic card with audio on the front and the word/phonetics on the back.
    -   **Spelling Rescue:** An interactive card with audio and a text box on the front. The back includes the answer, definitions, synonyms, and an example sentence, all with Bangla translations.
-   **Automatic Data Fetching:** For Spelling Rescue cards, it automatically fetches data from a dictionary API.
-   **Automatic Translation:** Fetched data is translated to Bangla.
-   **Ready-to-Import:** Creates a single `output.apkg` file that you can directly import into your Anki application.

## Requirements

-   [Python 3](https://www.python.org/downloads/)
-   An active internet connection (for audio generation, dictionary lookup, and translation).

## Setup Instructions

1.  **Download or Clone the Code:**
    Make sure you have all the project files in a directory on your computer.

2.  **Create a Virtual Environment:**
    Open your terminal or command prompt, navigate to the project directory, and run the following command to create a virtual environment. This helps manage project-specific dependencies.
    ```bash
    python3 -m venv venv
    ```

3.  **Install Dependencies:**
    Install the required Python libraries into the virtual environment by running:
    ```bash
    # On macOS/Linux
    venv/bin/python3 -m pip install -r requirements.txt

    # On Windows
    venv\Scripts\python -m pip install -r requirements.txt
    ```

## How to Run the Application

Once the setup is complete, you can run the application with the following command from the project's root directory:

```bash
# On macOS/Linux
venv/bin/python3 app.py

# On Windows
venv\Scripts\python app.py
```

A window for the "Anki Card Creator" should appear.

## How to Use

1.  **Enter a Word:** Type the English word you want to create a card for.
2.  **Select Type:** Choose either "Simple Audio" or "Spelling Rescue" from the dropdown menu.
3.  **Click Create:** Press the "Create Card" button.
4.  **Find Your Deck:** A file named `output.apkg` will be created or updated in the project directory.
5.  **Import to Anki:** Open your Anki Desktop application, go to `File > Import...`, and select the `output.apkg` file. Your new card will be added to the corresponding deck ("Generated Simple Cards" or "Generated Spelling Cards").

## Project Files

-   `app.py`: The main Python script containing the application's backend logic.
-   `requirements.txt`: A list of the Python dependencies required for the project.
-   `static/`: This folder contains the frontend files (HTML, CSS, JS) for the user interface.
-   `venv/`: The virtual environment folder (created during setup).
-   `media/`: This folder is automatically created to store the temporary audio files for your cards.
-   `output.apkg`: This is the generated Anki deck file that you can import.
