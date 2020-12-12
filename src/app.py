import logging
import os
from decouple import config
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    InlineQueryHandler,
    Filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN") or config("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL") or config("WEBHOOK_URL")
PORT = int(os.getenv("PORT", "8443"))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def calculate(text):
    try:
        return eval(text)
    except:
        return None


def echo(update: Update, context):
    text = update.message.text

    result = calculate(text)
    if result:
        update.message.reply_text(f"Il risultato è: {result}")
    else:
        update.message.reply_text("Non sono riuscito a calcolare il risultato :(")


def inline_query_handler(update, context):
    query = update.inline_query.query
    if not query:
        return

    result = calculate(query)
    if result:
        query_result = [
            InlineQueryResultArticle(
                id=8329480,
                title=f"Risultato: {result}",
                url=None,
                input_message_content=InputTextMessageContent(
                    f"Il risultato è: {result}"
                ),
            ),
        ]
    else:
        query_result = []

    update.inline_query.answer(query_result)


def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text, echo))
    dispatcher.add_handler(InlineQueryHandler(inline_query_handler))

    print(WEBHOOK_URL, PORT)

    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=BOT_TOKEN)
    updater.bot.set_webhook(f"{WEBHOOK_URL}/{BOT_TOKEN}")
    updater.idle()


if __name__ == "__main__":
    main()