from google.generativeai.types import FunctionDeclaration

get_folder_names = FunctionDeclaration(
    name="getFolderNames",
    description="Gets existing list of names of folders in Gmail Account",
)
