from creds import telegram_token
from redvid import Downloader
import os
from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from telegram.ext import Application, CommandHandler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Hi!\n"
                                    "Use /on to start the coffee-machine\n"
                                    "Use /off to stop the coffee-machine\n"
                                    "Use /cancel to stop the heatup task, without turning off the machine\n"
                                    "Or user /status to get the current power consumption")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle chat messages."""
    message = update.message.text
    if message.startswith("https://www.reddit.com/r/"):
        reddit = Downloader(max_q=True)
        reddit.url = message
        reddit.overwrite = True
        reddit.path = "./data/"
        video_path = reddit.download()

        await update.message.reply_video(video_path)
        os.remove(video_path)
    else:
        await update.message.reply_text("Please send a valid Reddit link")


def main() -> None:
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(telegram_token).build()

    """
    Bot Menu Config
    start - start the bot
    """
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(["start", "help"], start))
    #application.add_handler(MessageHandler(filters.Text, handle_message))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
