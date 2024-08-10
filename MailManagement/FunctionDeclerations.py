from google.generativeai.types import FunctionDeclaration

get_folder_names = FunctionDeclaration(
    name="getFolderNames",
    description="Gets list of folders names in Gmail",
)
