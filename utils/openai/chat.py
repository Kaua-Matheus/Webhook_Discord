# SYS
import os
import json

# .Env
from dotenv import load_dotenv

# Groq
from groq import Groq


class Llama:
    def __init__(self, file_name: str = "./utils/openai/history.json"):
        if load_dotenv():
            try:

                api_key = os.getenv("GROQ_API_KEY")
                if api_key == None:
                    raise EnvironmentError("API_KEY not found in Environment")
                
                self.client = Groq(api_key=api_key)
                
            except Exception as e:
                print(e)

        else:
            print("Couldn't load openai key")


        self.file_name = file_name
        self.history: list = self._load_history()


    def send_message(self, message: str, user: str = "user") -> str:
        """
            Send a message and get a response from the AI
        """

        self.history.append(
            {
                "role": "user",
                "content": f"{user}: {message}"
            }
        )

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=self.history,
            max_tokens=1024,
        )

        ai_response = response.choices[0].message.content

        self.history.append(
            {
                "role": "assistant",
                "content": f"{ai_response}"
            }
        )

        self._save_history()

        return ai_response
    

    def _load_history(self) -> list:
        """
            Get the history.json file and load it
        """

        try:

            if not os.path.isfile(self.file_name):

                with open(self.file_name, "w"):
                    print("File created")
                    pass


            with open(self.file_name, "r") as f:
                    data = f.read()
                    if data != "":
                        json_data = json.loads(data)
                    else:
                        json_data = []

            # Return a list of dicts
            return json_data

        except Exception as e:
            print("Error: _load_history")
            raise e
        

    def _save_history(self) -> None:
        try:
            with open(self.file_name, "w") as f:
                data = json.dumps(self.history)
                f.write(data)

            return None

        except Exception as e:
            print("Error: _save_history")
            raise e