# API Key Imports
import os
from dotenv import load_dotenv

# Gemini Imports
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from google.generativeai import ChatSession 

# gmailAPI Import
import gmailAPI

# Setting up Gemini
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key = api_key)

class BaseLLM():
    def __init__(self, **kwargs):
        self.isChat = kwargs.get('chat', False)

        self.model = genai.GenerativeModel(
            'gemini-1.5-flash',
            generation_config={
                "response_mime_type": "application/json",
                "max_output_tokens": 8192,
                "temperature": 0
            }
        )

        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        }

        if self.isChat:
            self.chat = self.model.start_chat(history = [])
        else:
            self.chat = None

    def getChat(self) -> ChatSession:
        if self.isChat:
            return self.chat
        else:
            print("This LLM does not have chat enabled")
            return None
        
    def newChat(self):
        self.isChat = True
        self.chat = self.model.start_chat(history = [])

    def chat(self, prompt: str) -> str:
        responses = self.chat.send_message(
            prompt,
            safety_settings= self.safety_settings,
            stream=False,
        )

        return responses.candidates[0].content.parts[0]
    
        # response = responses.candidates[0].content.parts[0]
        # params = {}
        # for key, value in response.function_call.args.items():
        #     params[key] = value
    
        # print(params)
        # if response.function_call.name == "get_users":
        #     result, api_response = get_users(**params)
        #     print(result) 
        # else: 
        #     print("function not called")

class QueryLLM(BaseLLM):
    def __init__(self):
        super().__init__(chat = True)
        self.gmail = gmailAPI.BaseGmail()

    def chat(self):
        prompt="Hi my name is Avi. What is your name"
        response = super().chat(prompt)
        print(response)


def main():
    query_bot = QueryLLM()
    query_bot.chat()

if __name__ == "__main__":
    main()