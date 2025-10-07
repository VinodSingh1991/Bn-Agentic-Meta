from agents.controllers.structured_output import AgentSchema
from langchain_core.prompts import ChatPromptTemplate
from agents.llm_factory import LLMFactory
from langchain_core.output_parsers import StrOutputParser

class UserQueryNormalizer:
    def __init__(self):
        # Don't instantiate AgentSchema here since it requires parameters
        # We'll create it when needed in the methods
        self.llm = LLMFactory().open_ai()
        
    
    def get_query_parse_prompt(self) -> ChatPromptTemplate:
        system_prompt = """
        You are a natural language query normalizer and corrector. and you are a intelligent agent that translates user queries into a english.
        -------------------------------------------------------------------------------------------------------
        ---Context for object name---
        example: Leads, Accounts, Contacts, Opportunities, Cases, Activities, Products, Quotes, Invoices, Solutions, Campaigns, Users, Teams
        -------------------------------------
        Your task:
        1. Correct spelling mistakes.
        2. Convert Hinglish or mixed Hindi-English to proper English.
        3. Convert user query into English if it is in another language.
        4. Convert numbers written in words to digits.

        Rules:
        - Output only the corrected, normalized natural language query.
        - Do not change the intent.
        - Use proper English grammar.

        Now, normalize this user query:
        {user_query}
        """
        return ChatPromptTemplate.from_messages([
            ("system", system_prompt)
        ])
    
    
    def invoke(self, user_query: str) -> str:
        prompt = self.get_query_parse_prompt()
        
        chain = prompt | self.llm | StrOutputParser()
        updated_query = chain.invoke({"user_query": user_query})
        return updated_query

    
