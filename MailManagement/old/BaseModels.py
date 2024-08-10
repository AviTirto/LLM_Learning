# API Key Imports
import os
from dotenv import load_dotenv

# Langchain Imports
from langchain_google_genai import (
    GoogleGenerativeAI,
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)

from langchain_core.prompts import (
    ChatPromptTemplate,
)

from vertexai.generative_models import (
    Tool
)

# Templates Import
from Templates import base_system_chat_template, base_user_chat_template

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

class BaseLLM():
    def __init__(self, **kwargs):

        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        }

        self.model = GoogleGenerativeAI(
            model='models/gemini-1.5-flash',
            google_api_key = api_key,
            safety_settings = self.safety_settings,
        )

    def getModel(self):
        return self.model

    def llm(self, prompt: str):
        return self.model.invoke(prompt)
    
class BaseChat():
    def __init__(self, **kwargs):

        # Chat Model Setup
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        }

        self.chat_model = ChatGoogleGenerativeAI(
            model='models/gemini-1.5-flash',
            google_api_key = api_key,
            safety_settings = self.safety_settings, 
            temperature=0,
        )
        
        self.default_prompt = ChatPromptTemplate([('system', base_system_chat_template), ('human', base_user_chat_template)])

    def getChatModel(self):
        return self.chat_model

    def chat(self, prompt: str, **kwargs):
        chat_prompt = kwargs.get('prompt', self.default_prompt)
        input_variables = kwargs.get('input', {'prompt': prompt})
        history = kwargs.get('history', None)
        memory = kwargs.get('memory', None)

        runnable = chat_prompt | self.chat_model

        response = runnable.invoke(input_variables)
        return response.content
