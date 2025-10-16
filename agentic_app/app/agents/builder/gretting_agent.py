from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from agents.llm_factory import LLMFactory


class GrettingAgent:
        
    @classmethod
    def get_prompt(cls) -> ChatPromptTemplate:
        system_prompt = """
        You are an intelligent CRM assistant specializing in detecting greetings and distinguishing them from CRM-related user queries.

        ### Task Overview
        Your goal is to analyze the user's input and identify whether it is a:
        1. **Greeting message** (e.g., "Hi", "Hello", "Good morning", "How are you", etc.)
        2. **CRM-related query** (e.g., "Show my open leads", "List all accounts", "Get top 10 opportunities grouped by status", etc.)
        3. **Unrecognized/Other message**

        ---

        ### Instructions
        You must always respond **strictly in JSON format** as shown below.

        #### If the input is a greeting message:
        ```json
        {{
        "greeting": "YES",
        "greetingReply": "Hello! I am doing great, thank you. How can I help you today?, I am your CRM Assistent please ask me somthing about CRM"
        }}


        Now, normalize this user query:
        {user_query}
        """
        return ChatPromptTemplate.from_messages([
            ("system", system_prompt)
        ])
    
    @classmethod
    def invoke(cls, user_query: str) -> str:
        prompt = cls.get_prompt()
        
        print("Invoking QueryTranslator with user_query:", user_query)
        chain = prompt | LLMFactory.open_ai() | JsonOutputParser()
        print("Chain created, invoking...")
        
        updated_query = chain.invoke({"user_query": user_query})
        print("QueryTranslator output:", updated_query)
        return updated_query

    
