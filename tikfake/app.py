import moviepy.editor as mpe

from TikTokApi import TikTokApi


def downloader_video_with_audio(video_with_audio, video_without_audio):
    """Function for getting video"""
    audio = get_audio(video_with_audio)
    my_clip = get_video_with_audio(video_without_audio, audio)
    my_clip.write_videofile("movie.mp4")


def get_audio(video):
    """Function for getting audio from video"""
    videoclip = mpe.VideoFileClip(video)
    return videoclip.audio


def get_video_with_audio(video_without_audio, audio):
    """Function for getting audio from video"""
    video_clip = mpe.VideoFileClip(video_without_audio)
    return video_clip.set_audio(audio)


def downloader_video_from_link(url):
    """Download the video from the link"""
    video = TikTokApi().get_video_by_url(url)
    with open("video.mp4", "wb") as out:
         out.write(video)
