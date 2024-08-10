from BaseModels import BaseChat
from Templates import master_chat_sys_details
from Tools import GmailTools
from FunctionDeclerations import get_folder_names
from google.generativeai.types import Tool

class MasterChat(BaseChat):
    def __init__(self):
        super().__init__(sys_detail = master_chat_sys_details)
        self.gmail_tools = GmailTools()
        self.tools = Tool(
            function_declarations = [get_folder_names]
        )

    def sendMessage(self, prompt: str):
        response = super().sendMessage(prompt, tools = self.tools)
        return response