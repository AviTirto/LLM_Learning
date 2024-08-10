from BaseModels import BaseChat, BaseLLM

from langchain.memory import (
    ConversationSummaryBufferMemory
)

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
)

from langchain.schema import SystemMessage

from langchain.chains.llm import LLMChain

from Templates import master_system_chat_template, master_user_chat_template

# Gmail API Import
from GmailAPI import QueryGmail

class MasterChat(BaseChat):
    def __init__(self):
        super().__init__()
        self.memory = ConversationSummaryBufferMemory(llm=BaseLLM().getModel(), max_token_limit = 2048, memory_key="chat_history", return_messages=True)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=master_system_chat_template
                ),  # The persistent system prompt
                MessagesPlaceholder(
                    variable_name="chat_history"
                ),  # Where the memory will be stored.
                HumanMessagePromptTemplate.from_template(
                    master_user_chat_template
                ),      # Where the human input will be injected
            ]
        )
    
    def chat(self, prompt: str, **kwargs):
        runnable = LLMChain(
            llm=self.getChatModel(),
            prompt=self.prompt,
            verbose=True,
            memory=self.memory,
        )

        response = runnable.predict(prompt=prompt)
        return response