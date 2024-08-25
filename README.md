# Translator_chatbot

## Overview
This is a Python-based Telegram bot that translates text messages between various languages using the **Seamless M4T Model** by Facebook AI. The bot can automatically detect the input language, and allows users to select their desired target language for translation. It leverages the `transformers` library for translation tasks and uses `langid` for language detection.Here is the bot username: https://t.me/Ars_gooyesh_intern_bot

## Key Features

- **Automatic Language Detection**: The bot can identify the input language using the `langid` library.
- **Seamless Translation**: Powered by Facebook's Seamless M4T model, the bot supports translation between multiple languages.
- **Interactive Language Selection**: Users can choose their target language via an interactive button interface.
- **Multi-Language Support**: Currently supports translations between English, Spanish, French, German, Persian (Farsi), and Russian.

## Supported Languages

The bot supports the following languages:

- English (eng)
- Spanish (spa)
- French (fra)
- German (deu)
- Persian (pes)
- Russian (rus)

## How It Works

1. **Start the Bot**: Users can start interacting with the bot by sending the `/start` command.
2. **Send a Message**: After the bot is initiated, users can send any text message to the bot.
3. **Language Detection**: The bot automatically detects the language of the input text.
4. **Target Language Selection**: The bot prompts the user to select a target language from an interactive menu.
5. **Translation**: After the user selects a target language, the bot translates the input text and sends the translated message back to the user.

## Installation and Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/Niloofar1381/Translator_chatbot.git
   cd Translator_chatbot
   ```

2. Install the required Python packages:
   ```bash
   pip install python-telegram-bot transformers torch langid
   ```

3. Replace the `token` variable in the code with your actual Telegram bot token, or set it as an environment variable `TELEGRAM_BOT_TOKEN`.You can get a
   token from https://t.me/BotFather

5. Run the bot:
   ```bash
   python telegram_bot_application_with_seamless_m4t.py
   ```

## Dependencies

This bot relies on several Python libraries:

- `telegram`: For interacting with the Telegram Bot API.
- `transformers`: To load and utilize the Seamless M4T Model.
- `torch`: For handling tensor operations and model computations.
- `langid`: For detecting the language of the input text.

## Future Enhancements

- **More Language Support**: Expand the list of supported languages for translation.
- **Improved Language Detection**: Enhance the accuracy of language detection.
- **Speech-to-Text Integration**: Incorporate speech input and output capabilities for a more comprehensive translation experience.


This README file provides a clear and concise overview of the bot, its functionality, and how to set it up. You can adjust any specific details like the repository link or token management based on your preferences.
