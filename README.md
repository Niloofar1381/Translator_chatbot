# Telegram Translation Bot

A Telegram bot that detects the language of a user's message and translates it into a target language of choice using the Seamless M4T Model. The bot provides an easy-to-use interface with inline buttons to select target languages and give feedback on the translations.

## Features

- **Automatic Language Detection**: The bot uses `langid` to automatically detect the language of the user's input.
- **Multi-language Translation**: Translates messages between the following languages:
  - English
  - Spanish
  - French
  - German
  - Persian
  - Russian
- **User Feedback**: Users can provide feedback on the translation quality or leave a comment for further improvement.
- **Asynchronous Processing**: Efficiently handles translations using Python's `asyncio` library.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Niloofar1381/telegram-translation-bot.git
   cd telegram-translation-bot
   ```


2. **Install dependencies:**

   ```bash
   pip install python-telegram-bot transformers torch langid
   ```

3. **Replace the placeholder `TELEGRAM_BOT_TOKEN` in the `main()` function with your actual Telegram Bot API token:**

   ```python
   token = "YOUR_TELEGRAM_BOT_TOKEN"
   ```

## Usage

Run the bot with the following command:

```bash
python Telegram_bot.py
```

Once the bot is running, start a conversation with it on Telegram by searching for your bot's username.

### Available Commands

- `/start` - Start interacting with the bot.
- Send any text message to translate it to your desired language.

### How to Translate

1. **Send a message:** Type any text message to the bot.
2. **Choose a target language:** Select the language to which you want to translate the message using the inline buttons.
3. **Receive the translation:** The bot will return the translated text and ask for your feedback.
4. **Provide feedback (optional):** Click on the "Good", "Bad", or "Add Comment" buttons to provide feedback on the translation quality.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any features, improvements, or bug fixes.

## Acknowledgments

- [Hugging Face Transformers](https://huggingface.co/transformers/) for providing state-of-the-art NLP models.
- [PyTorch](https://pytorch.org/) for the deep learning framework.
- [Langid](https://github.com/saffsd/langid.py) for language detection.

## Contact

For any issues or inquiries, please open an issue in this repository or contact the maintainer at [hz93niloufar@gmail.com](mailto:your-email@example.com).

