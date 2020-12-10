from telegram import Update
from telegram.ext import Updater, CommandHandler


def start(update: Update, context):
    update.message.reply_text(f"Ciao { update.effective_use.first_name }")


def main():
    updater = Updater(
        "1391955683:AAEmdgktI_bIMSAFZFA7ov9wtWk_oyrQ_gw", use_context=True
    )
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()