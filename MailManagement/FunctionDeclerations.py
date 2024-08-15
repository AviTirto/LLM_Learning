from google.generativeai.types import FunctionDeclaration

get_folder_names = FunctionDeclaration(
    name="getFolderNames",
    description="Gets list of folders names in Gmail",
)

get_emails = FunctionDeclaration(
    name="getEmails",
    description="Gets emails in Gmail",
    parameters={
        "type": "object",
        "properties": {
            "older_than": {
                "type": "integer",
                "description": "The number of days the emails will be older than ex. 3 means that the emails will be from 3 days ago."
            },
            "newer_than": {
                "type": "integer",
                "description": "The number of days the emails will be newer than ex. 2 means that the emails will be from the last 2 days"
            }
        }
    }
)