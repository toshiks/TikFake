import logging
import pathlib

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from tikfake.animation_pipeline import AnimationPipeline
from tikfake.utils import downloader_video_with_audio, downloader_video_from_link


class Bot:
    _logger = logging.getLogger(__name__)

    def __init__(self, token: str, storage_path: str, sprite_path: str):
        self.updater = Updater(token, use_context=True)
        self._user_requests = {}
        self._storage_path = storage_path
        self._sprite_path = pathlib.Path(sprite_path)

        self.setup_callbacks()

    def setup_callbacks(self):
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('help', self.help))
        dp.add_handler(MessageHandler(Filters.text, self.link))
        dp.add_error_handler(Bot.error)

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def link(self, update: Updater, context: CallbackContext):
        """Process entered URL."""
        url = update.message.text

        if self._user_requests.get(update.message.chat_id, None) is not None:
            update.message.reply_text(f'Sorry, but I can prepare only one video per user')
            return

        self._user_requests[update.message.chat_id] = url
        update.message.reply_text(f'Please, wait...')

        users_tiktok_path = pathlib.Path(self._storage_path).joinpath(
            f"{update.message.chat_id}_{update.message.message_id}.mp4"
        )
        users_tiktok_path_processed = pathlib.Path(self._storage_path).joinpath(
            f"{update.message.chat_id}_{update.message.message_id}_processed.mp4"
        )
        users_tiktok_path_processed_audio = pathlib.Path(self._storage_path).joinpath(
            f"{update.message.chat_id}_{update.message.message_id}_processed_audio.mp4"
        )

        # download video in "video.mp4"
        try:
            downloader_video_from_link(url, users_tiktok_path)
        except Exception as e:
            self._user_requests.pop(update.message.chat_id)
            update.message.reply_text(f'Sorry, but link is wrong')
            return

        # ml
        animation_pipeline = AnimationPipeline()
        animation_pipeline.process(users_tiktok_path, self._sprite_path, users_tiktok_path_processed)

        # download in "movie.mp4"
        downloader_video_with_audio(users_tiktok_path, users_tiktok_path_processed, users_tiktok_path_processed_audio)

        # send "movie.mp4" to the user
        with open(users_tiktok_path_processed_audio, "rb") as file:
            context.bot.sendVideo(update.message.chat_id, video=file, supports_streaming=False)

        self._user_requests.pop(update.message.chat_id)
        users_tiktok_path_processed.unlink()
        users_tiktok_path_processed_audio.unlink()
        users_tiktok_path.unlink()

    @staticmethod
    def help(update: Updater, context: CallbackContext):
        """Display help."""
        update.message.reply_text('Enter a TikTok URL and get an animated video generated from it.')

    @staticmethod
    def error(update: Updater, context: CallbackContext):
        """Log errors caused by updates."""
        Bot._logger.warning('Update "%s" caused error "%s"', update, context.error)


def setup_logger():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)


def main():
    """Read the token from stdin an start the bot."""
    print('Enter TikFake Telegram bot token:')
    token = input()
    storage_path = ""
    sprite_path = ""
    Bot(token, storage_path, sprite_path).start()


if __name__ == '__main__':
    main()
