# Build-in Packages
import os

# .Env
from dotenv import load_dotenv

# Client
from utils.client import Bot

if load_dotenv():
    print(".env file loaded successfully")

    try:

        # Bot Token Definition
        TOKEN: str = os.getenv("TOKEN")

        # Bot instance
        bot = Bot()

        bot.run(TOKEN)
        
    
    except Exception as err:
        print(f"Generic error: {err}")
else:
    print("Couldn't load .env file")