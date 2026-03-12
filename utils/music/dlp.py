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


if load_dotenv():
    OUT_PATH=os.getenv("OUT_PATH")
    if os.path.isdir(OUT_PATH):
        pass
    else:
        os.mkdir(OUT_PATH)

else:
    OUT_PATH="./out"
    if os.path.isdir(OUT_PATH):
        pass
    else:
        os.mkdir(OUT_PATH)



class Player():
    def __init__(self):
        self.ydl_opt: dict = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(OUT_PATH, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'download_archive': os.path.join(OUT_PATH, 'download.txt'),
            'noplaylist': True,
            'quiet': False,
            'default_search': 'ytsearch1'
        }
        pass

    def download(self, music_list: list[str]): # List of musics, need to be incrementable
        for music in music_list:
            with YoutubeDL(self.ydl_opt) as ydl:
                try:
                    ydl.download(f"{music}")
                except Exception as err:
                    print(f"A Generic error occuried: {err}")
                    logging.error(f"A Generic error occuried: {err}")
                    continue