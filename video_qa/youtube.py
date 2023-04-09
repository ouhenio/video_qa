import os

import yt_dlp


class YouTubeDownloader:
    def __init__(self, output_directory="downloads"):
        self.output_directory = output_directory
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

    def download_video(self, video_url, audio_format="mp3"):
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": audio_format,
                    "preferredquality": "192",
                }
            ],
            "outtmpl": f"{self.output_directory}/%(id)s.%(ext)s",
            "quiet": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            file_path = ydl.prepare_filename(info)

            # Replace the original extension with the desired audio format
            file_path = file_path.rsplit(".", 1)[0] + f".{audio_format}"

            # Check if the audio file already exists
            if not os.path.isfile(file_path):
                ydl.download([video_url])
            else:
                print("Audio file already exists:", file_path)

        return file_path
