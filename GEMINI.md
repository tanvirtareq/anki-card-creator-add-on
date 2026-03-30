# Gemini Playbook - Anki Card Creator Add-on

This file provides context and guidelines for AI agents working on the **Anki Card Creator Add-on** project.

## Project Overview
This is an Anki desktop add-on designed to streamline the creation of flashcards. It features dictionary lookups, automated translations (English to Bangla), and audio generation using gTTS. It also includes a **Gemini-powered** mode for richer content generation.

## Technical Stack
- **Language:** Python 3.13
- **Platform:** Anki Desktop (Qt-based UI)
- **AI Backend:** Google Gemini API (`google-generativeai`)
- **Audio:** gTTS (Google Text-to-Speech)
- **State Management:** `.env` file for API keys and environment variables.

## Project Structure
- `AnkiCardCreatorAddon/`: Core add-on directory.
    - `__init__.py`: Entry point and logging setup.
    - `main_dialog.py`: Main UI dialog for card creation.
    - `card_creator/`: Factory pattern for different card types.
        - `gemini_utils.py`: Logic for Gemini API interactions and prompts.
        - `gemini_card_creator.py`: Base class for AI-driven card creation.
- `deploy.sh`: macOS utility for local development and deployment.

## Coding Standards
- **Logging:** Use the centralized logger from `..logger`. Log debug information for all external API calls.
- **Error Handling:** Wrap UI-triggering actions in `try-except` blocks and use `showWarning` or `tooltip` for user feedback.
- **Dependency Management:** All dependencies must be vendored into the `vendor/` directory using `pip install -r requirements.txt -t ./vendor`.
- **Modularity:** Use the Factory pattern for card creators to ensure new card types can be added easily.

## Gemini Integration
- **Prompts:** Prompts are currently defined in `AnkiCardCreatorAddon/card_creator/gemini_utils.py`.
- **Response Format:** The system expects a strict JSON response from Gemini to ensure reliability.
- **Model:** Currently using `gemini-2.5-flash` (or latest stable flash model).

## Behavioral Rules for AI
- **UI Changes:** When modifying the UI, prioritize user-friendly layouts and clear labels.
- **Anki API:** Refer to [Anki's developer documentation](https://addon-docs.ankiweb.net/) for specific API usages (e.g., `mw.col.new_note`, `mw.col.add_note`).
- **Bangla Support:** Ensure that all Bangla translations and text handling support Unicode properly.
- **No Placeholders:** Avoid using placeholder code; provided solutions should be complete and functional.
