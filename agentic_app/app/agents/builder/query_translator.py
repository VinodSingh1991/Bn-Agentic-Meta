from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from agents.llm_factory import LLMFactory

class QueryTranslator:
        
    @classmethod
    def get_query_parse_prompt(cls) -> ChatPromptTemplate:
        system_prompt = """
        You are a natural language query normalizer and corrector. and you are a intelligent agent that translates user queries into a english.
        -------------------------------------------------------------------------------------------------------
        ---Context for object name---
        example: Leads, Accounts, Contacts, Opportunities, Cases, Activities, Products, Quotes, Invoices, Solutions, Campaigns, Users, Teams
        -------------------------------------
        Your task 1:
        1. Correct spelling mistakes.
        2. Convert Hinglish or mixed Hindi-English to proper English.
        3. Convert user query into English if it is in another language.
        4. Convert numbers written in words to digits.
        
        Rules for task 1:
        - Output only the corrected, normalized natural language query.
        - Do not change the intent.
        - Use proper English grammar.

        Now, normalize this user query:
        {user_query}
        """
        return ChatPromptTemplate.from_messages([
            ("system", system_prompt)
        ])
    
    @classmethod
    def invoke(cls, user_query: str) -> str:
        prompt = cls.get_query_parse_prompt()
        
        print("Invoking QueryTranslator with user_query:", user_query)
        chain = prompt | LLMFactory.open_ai() | StrOutputParser()
        print("Chain created, invoking...")
        
        updated_query = chain.invoke({"user_query": user_query})
        print("QueryTranslator output:", updated_query)
        return updated_query

    
