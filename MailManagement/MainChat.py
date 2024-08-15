from BaseModels import BaseChat
from Templates import master_chat_sys_details
from Tools import GmailTools
from FunctionDeclerations import get_folder_names, get_emails
from google.generativeai.types import Tool
from google.generativeai.protos import FunctionResponse

class MasterChat(BaseChat):
    def __init__(self):
        super().__init__(sys_detail = master_chat_sys_details)
        self.gmail_tools = GmailTools()
        self.tools = Tool(
            function_declarations = [get_folder_names, get_emails]
        )

    def sendMessage(self, prompt: str):
        response = super().sendMessage(prompt, tools = self.tools)
        if response.parts[0].function_call.name != None:
            params = {}
            for key, value in response.parts[0].function_call.args.items():
                params[key] = value

            if response.parts[0].function_call.name == "getFolderNames":
                folder_names = self.gmail_tools.getFolderNames()
                response = super().sendMessage(
                    FunctionResponse(
                        name = "getFolderNames",
                        response = {
                            'message': folder_names[1],
                            'result': folder_names[0]
                        }
                    ),
                    tools = self.tools
                )
            
            if response.parts[0].function_call.name == "getEmails":
                emails = self.gmail_tools.getEmails(**params)
                # response = super().sendMessage(
                #     FunctionResponse(
                #         name = "getFolderNames",
                #         response = {
                #             'message': folder_names[1],
                #             'result': folder_names[0]
                #         }
                #     ),
                #     tools = self.tools
                # )
                return str(emails)

        return response.text
        