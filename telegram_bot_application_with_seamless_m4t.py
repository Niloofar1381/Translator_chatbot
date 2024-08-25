# -*- coding: utf-8 -*-

import os
import logging
import langid  # Import langid for language detection
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from transformers import AutoProcessor, SeamlessM4TModel
import torch

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Seamless M4T Model
model_name = "facebook/hf-seamless-m4t-medium"
processor = AutoProcessor.from_pretrained(model_name)
model = SeamlessM4TModel.from_pretrained(model_name)

# Check if CUDA is available, if yes, set the device to "cuda:0", else use the CPU
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# Language codes and names mapping (only supported languages for SeamlessM4T)
languages = {
    "eng": "English",
    "spa": "Spanish",
    "fra": "French",
    "deu": "German",
    "pes": "Persian",  # Updated to the supported "pes" code
    "rus": "Russian"
}

# Define the translation function
def translate_text(text, source_lang, target_lang):
    # Process the input text with source language
    text_inputs = processor(text=text, src_lang=source_lang, return_tensors="pt").to(device)

    # Generate the translated text with the target language
    text_array = model.generate(**text_inputs, tgt_lang=target_lang, generate_speech=False)

    # Decode the output text
    translated_text = processor.decode(text_array[0].tolist()[0], skip_special_tokens=True)
    return translated_text

# Define function to detect the language using langid
def detect_language(text):
    detected_lang_code, _ = langid.classify(text)

    # Map langid detected languages to SeamlessM4T supported languages if necessary
    if detected_lang_code == "fas":  # Langid might return "fas" for Persian, map to "pes"
        detected_lang_code = "pes"

    # Ensure the detected language is in the supported languages, otherwise default to English
    if detected_lang_code not in languages:
        detected_lang_code = "eng"  # Default to English if the detected language isn't supported

    return detected_lang_code

# Define command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"Received /start command from {update.effective_user.username}")
    await update.message.reply_text('Hello! Send me a message and I will translate it.')

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text

    # Detect the language of the input text
    detected_language = detect_language(user_text)

    # Get the human-readable language name
    detected_language_name = languages.get(detected_language, "Unknown")

    # Ask the user to choose the target language
    keyboard = [
        [InlineKeyboardButton("English", callback_data="eng"),
         InlineKeyboardButton("Spanish", callback_data="spa")],
        [InlineKeyboardButton("French", callback_data="fra"),
         InlineKeyboardButton("German", callback_data="deu")],
        [InlineKeyboardButton("Persian", callback_data="pes"),
         InlineKeyboardButton("Russian", callback_data="rus")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Store the user text and detected language in the context for later use
    context.user_data['user_text'] = user_text
    context.user_data['detected_language'] = detected_language

    await update.message.reply_text(
        f"Detected language: {detected_language_name}. Please choose the target language:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    target_lang = query.data

    # Retrieve the stored user text and detected language from the context
    user_text = context.user_data.get('user_text')
    detected_language = context.user_data.get('detected_language')

    # Perform the translation
    translated_text = translate_text(user_text, detected_language, target_lang)

    # Send the translated text back to the user
    await query.edit_message_text(f"Translation: {translated_text}")

# Set up the application
def main():
    # Set the bot token directly
    token = "TELEGRAM_BOT_TOKEN" # set your token API here

    if not token:
        logger.error("TELEGRAM_BOT_TOKEN environment variable is not set.")
        return

    # Create the application
    application = ApplicationBuilder().token(token).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))
    application.add_handler(CallbackQueryHandler(button))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
