# Youtube_DL
from yt_dlp import YoutubeDL

# SYS
import os
import logging

# .Env
from dotenv import load_dotenv


# Logging Config
logging.basicConfig(level=logging.INFO, filename='app.log')
logging.info('O programa foi iniciado')



class Downloader():
    def __init__(self):
        self.queue = [str]
        self.current = None
        self.voice_client = None

        if load_dotenv():
            self.OUT_PATH=os.getenv("OUT_PATH")
            if os.path.isdir(self.OUT_PATH):
                pass
            else:
                os.mkdir(self.OUT_PATH)

        else:
            self.OUT_PATH="./out"
            if os.path.isdir(self.OUT_PATH):
                pass
            else:
                os.mkdir(self.OUT_PATH)

        self.ydl_opt: dict = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.OUT_PATH, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'download_archive': os.path.join(self.OUT_PATH, 'download.txt'),
            'noplaylist': True,
            'quiet': False,
            'default_search': 'ytsearch1'
        }
        pass

    def add_to_queue(self, music: str):
        """
        Add a music in the queue
        """
        self.queue.append(music)


    def next_music(self):
        if len(self.queue) > 0:
            # Return the first element
            return self.queue.pop(0)
        else:
            return None


    def download(self, music: str):
        with YoutubeDL(self.ydl_opt) as ydl:
            try:
                ydl.download(f"{music}")

                files = [f for f in os.listdir(self.OUT_PATH) if f.endswith(".mp3")]
                if files:
                    files.sort(key=lambda x: os.path.getmtime(os.path.join(self.OUT_PATH, x)), reverse=True)
                    return os.path.join(self.OUT_PATH, files[0])
            except Exception as err:
                print(f"A Generic error occuried: {err}")
                logging.error(f"A Generic error occuried: {err}")
