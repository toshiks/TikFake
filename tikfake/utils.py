import ffmpeg
from TikTokApi import TikTokApi


def downloader_video_with_audio(video_with_audio, video_without_audio, path_to_save):
    """Function for getting video"""
    with_audio = ffmpeg.input(str(video_with_audio))
    without_audio = ffmpeg.input(str(video_without_audio))

    ffmpeg.concat(without_audio, with_audio, v=1, a=1).output(str(path_to_save)).run(quiet=True)


def downloader_video_from_link(url, path_to_save):
    """Download the video from the link"""
    video = TikTokApi.get_instance().get_video_by_url(url)
    with open(path_to_save, "wb") as out:
        out.write(video)
