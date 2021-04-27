import logging
import sys

from TikTokApi import TikTokApi
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def link(update, context):
    """Process entered URL."""
    url = update.message.text
    update.message.reply_text(f'TikTok url: {url}')
    # TODO: replace with video downloading and processing
    downloader(url)


def downloader(url):
    """Download the video from the link"""
    video = TikTokApi().get_video_by_url(url)
    with open("video2.mp4", "wb") as out:
         out.write(video)


def help(update, context):
    """Display help."""
    update.message.reply_text('Enter a TikTok URL and get an animated video generated from it.')


def error(update, context):
    """Log errors caused by updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main(token):
    """Start the bot."""

    updater = Updater(token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(MessageHandler(Filters.text, link))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print('Enter TikFake Telegram bot token:')
    token = input()
    main(token)
