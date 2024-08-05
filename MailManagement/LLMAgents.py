# API Key Imports
import os
from dotenv import load_dotenv

# Gemini Imports
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# gmailAPI Import
import gmailAPI

# Setting up Gemini
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key = api_key)

class BaseLLM():
    def __init__(self):
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

    def get_chat_responses(chat: ChatSession, prompt: str) -> str:
        responses = chat.send_message(
            prompt,
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=False,
        )
    
        response = responses.candidates[0].content.parts[0]
        params = {}
        for key, value in response.function_call.args.items():
            params[key] = value
    
        print(params)
        if response.function_call.name == "get_users":
            result, api_response = get_users(**params)
            print(result) 
        else: 
            print("function not called")

class QueryLLM(BaseLLM):
    def __init__(self):
        super().__init__()
        self.gmail = gmailAPI.BaseGmail()


def main():
    print("Hello")

if __name__ == "__main__":
    main()