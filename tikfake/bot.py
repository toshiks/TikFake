import logging
import pathlib
import threading

import time

from TikTokApi import TikTokApi
from taskqueue import LocalTaskQueue

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from tikfake.animation_pipeline import AnimationPipeline
from tikfake.app import downloader_video_with_audio, downloader_video_from_link

tq = LocalTaskQueue(parallel=1)


def worker(chat_id, context):

    # ml
    animation_pipeline = AnimationPipeline()
    animation_pipeline.process(pathlib.Path(f"data/{chat_id}.mp4"),
                               pathlib.Path(f"data/{chat_id}_output.mp4"))

    # download in "movie.mp4"
    downloader_video_with_audio(f"data/{chat_id}.mp4",
                                f"data/{chat_id}_output.mp4", chat_id)
    context.bot.sendVideo(chat_id, video=open(f"data/{chat_id}_movie.mp4", 'rb'),
                          supports_streaming=True)

class Bot:
    def __init__(self, token, a):
        self.updater = Updater(token, use_context=True)
        self.a = a
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('help', self.help))
        dp.add_handler(MessageHandler(Filters.text, self.link))
        dp.add_error_handler(self.error)

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def link(self, update: Updater, context: CallbackContext):
        """Process entered URL."""
        url = update.message.text
        update.message.reply_text(f'PLease, wait...')
        # download video in "video.mp4"
        downloader_video_from_link(url, str(update.message.chat_id), self.a)

        # tq.insert(worker(update.message.chat_id, context))

        # t = threading.Thread(target=worker)
        # t.daemon = True
        # t.start()

    def help(self, update: Updater, context: CallbackContext):
        """Display help."""
        update.message.reply_text('Enter a TikTok URL and get an animated video generated from it.')

    def error(self, update: Updater, context: CallbackContext):
        """Log errors caused by updates."""
        self.logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Read the token from stdin an start the bot."""
    print('Enter TikFake Telegram bot token:')
    token = input()
    a = TikTokApi()
    Bot(token, a).start()


if __name__ == '__main__':
    main()
