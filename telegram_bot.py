# -*- coding: utf-8 -*-
"""Telegram_bot.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Y9BHZH6lbZZyNYmrxui5io_CIiMTPyk9
"""

import os
import logging
import langid
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from transformers import AutoProcessor, SeamlessM4TModel
import torch
import asyncio

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
    "pes": "Persian",
    "rus": "Russian"
}

# Define the translation function
async def translate_text(text, source_lang, target_lang):
    text_inputs = processor(text=text, src_lang=source_lang, return_tensors="pt").to(device)
    text_array = model.generate(**text_inputs, tgt_lang=target_lang, generate_speech=False)
    translated_text = processor.decode(text_array[0].tolist()[0], skip_special_tokens=True)
    return translated_text

# Detect the language using langid
def detect_language(text):
    detected_lang_code, _ = langid.classify(text)
    if detected_lang_code == "fas":  # Langid might return "fas" for Persian, map to "pes"
        detected_lang_code = "pes"
    if detected_lang_code not in languages:
        detected_lang_code = "eng"  # Default to English if the detected language isn't supported
    return detected_lang_code

# Command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Send me a message and I will translate it.')

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_text = update.message.text
    detected_language = detect_language(user_text)
    detected_language_name = languages.get(detected_language, "Unknown")

    keyboard = [
        [InlineKeyboardButton("English", callback_data="lang_eng"),
         InlineKeyboardButton("Spanish", callback_data="lang_spa")],
        [InlineKeyboardButton("French", callback_data="lang_fra"),
         InlineKeyboardButton("German", callback_data="lang_deu")],
        [InlineKeyboardButton("Persian", callback_data="lang_pes"),
         InlineKeyboardButton("Russian", callback_data="lang_rus")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.user_data['user_text'] = user_text
    context.user_data['detected_language'] = detected_language

    await update.message.reply_text(
        f"Detected language: {detected_language_name}. Please choose the target language:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    target_lang = query.data.split('_')[1]  # Extract the language code after "lang_"

    user_text = context.user_data.get('user_text')
    detected_language = context.user_data.get('detected_language')

    await query.answer()  # Acknowledge the button press

    asyncio.create_task(handle_translation(query, user_text, detected_language, target_lang, context))

async def handle_translation(query, user_text, detected_language, target_lang, context):
    try:
        translated_text = await translate_text(user_text, detected_language, target_lang)
        context.user_data['translated_text'] = translated_text

        feedback_keyboard = [
            [InlineKeyboardButton("Good", callback_data="feedback_good"),
             InlineKeyboardButton("Bad", callback_data="feedback_bad")],
            [InlineKeyboardButton("Add Comment", callback_data="feedback_comment")]
        ]
        feedback_reply_markup = InlineKeyboardMarkup(feedback_keyboard)

        await query.edit_message_text(f"Translation: {translated_text}\n\nIs this translation good?",
                                      reply_markup=feedback_reply_markup)
    except Exception as e:
        logger.error(f"Error during translation: {e}")
        await query.edit_message_text("Sorry, something went wrong during the translation. Please try again.")

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    feedback_type = query.data

    if feedback_type == "feedback_good":
        feedback_message = "Thank you for your feedback! We're glad you liked the translation."
    elif feedback_type == "feedback_bad":
        feedback_message = "Sorry to hear that the translation wasn't up to your expectations. We'll work to improve!"
    elif feedback_type == "feedback_comment":
        await query.edit_message_text("Please send your comments about the translation:")
        return  # Wait for user to send comment

    await query.edit_message_text(feedback_message)

async def handle_comment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_comment = update.message.text
    context.user_data['comment'] = user_comment
    await update.message.reply_text("Thank you for your comment!")

def main():
    token = "TELEGRAM_BOT_TOKEN"  # Replace with your actual token

    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))
    application.add_handler(CallbackQueryHandler(button, pattern="^lang_"))
    application.add_handler(CallbackQueryHandler(feedback, pattern="^feedback_"))
    application.add_handler(MessageHandler(filters.TEXT & filters.UpdateType.MESSAGE, handle_comment))

    application.run_polling()

if __name__ == '__main__':
    main()