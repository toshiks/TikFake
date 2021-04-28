import logging
import pathlib

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from tikfake.animation_pipeline import AnimationPipeline
from tikfake.app import downloader_video_with_audio, downloader_video_from_link

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def link(update: Updater, context: CallbackContext):
    """Process entered URL."""
    url = update.message.text
    update.message.reply_text(f'TikTok url: {url}')

    # download video in "video.mp4"
    downloader_video_from_link(url)

    # ml
    animation_pipeline = AnimationPipeline()
    animation_pipeline.process(pathlib.Path("video.mp4"), pathlib.Path("output.mp4"))

    # download in "movie.mp4"
    downloader_video_with_audio("video.mp4", "output.mp4")

    # send "movie.mp4" to the user
    context.bot.sendVideo(update.message.chat_id, video=open('movie.mp4', 'rb'), supports_streaming=True)


def help(update: Updater, context: CallbackContext):
    """Display help."""
    update.message.reply_text('Enter a TikTok URL and get an animated video generated from it.')


def error(update: Updater, context: CallbackContext):
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
