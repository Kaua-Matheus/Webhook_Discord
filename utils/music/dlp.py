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
            'noplaylist': True,
            'quiet': False,
            'default_search': 'ytsearch1',
            'ignoreerrors': True
        }
        pass


    def download(self, music: str):
        with YoutubeDL(self.ydl_opt) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch1:{music}", download=False)
                
                if 'entries' in info and info['entries']:
                    video_info = info['entries'][0]
                    video_title = video_info.get('title', 'Unknown')

                    safe_title = "".join(c for c in video_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                    expected_file = os.path.join(self.OUT_PATH, f"{safe_title}.mp3")
                    
                    if os.path.exists(expected_file):
                        print(f"Arquivo já existe: {expected_file}")
                        return expected_file
                    
                    ydl.download([f"ytsearch1:{music}"])
                    
                    files = [f for f in os.listdir(self.OUT_PATH) if f.endswith(".mp3")]
                    if files:
                        files.sort(key=lambda x: os.path.getmtime(os.path.join(self.OUT_PATH, x)), reverse=True)
                        return os.path.join(self.OUT_PATH, files[0])
                    
                    if os.path.exists(expected_file):
                        return expected_file
                        
                return None
                
            except Exception as err:
                print(f"A Generic error occurred: {err}")
                logging.error(f"A Generic error occurred: {err}")
                return None
            
            
    def get_music_info(self, music: str):
        """Extrai informações da música sem baixar"""
        with YoutubeDL({'quiet': True, 'default_search': 'ytsearch1'}) as ydl:
            try:
                info = ydl.extract_info(f"ytsearch1:{music}", download=False)
                if 'entries' in info and info['entries']:
                    video_info = info['entries'][0]
                    return {
                        'title': video_info.get('title', music),
                        'duration': video_info.get('duration', 0),
                        'uploader': video_info.get('uploader', 'Unknown')
                    }
            except Exception as e:
                print(f"Erro ao extrair info: {e}")
                return {'title': music, 'duration': 0, 'uploader': 'Unknown'}
