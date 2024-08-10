# API Key Imports
import os
from dotenv import load_dotenv

# Gemini Imports
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configuring Gemini
load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

class BaseLLM():
    def __init__(self, **kwargs):
        self.system_instructions = kwargs.get('sys_detail', "")

        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        }

        self.model = genai.GenerativeModel(
            "gemini-1.5-flash",
            system_instruction = self.system_instructions,
        )

    def getModel(self):
        return self.model
    

class BaseChat(BaseLLM):
    def __init__(self, **kwargs):
        sys_detail = kwargs.get('sys_detail', "")

        super().__init__(sys_detail = sys_detail)

        self.chat = self.getModel().start_chat(history = [])

    def sendMessage(self, prompt:str, **kwargs):
        tools = kwargs.get('tools', [])

        response = self.chat.send_message(
            prompt,
        )

        return response.text