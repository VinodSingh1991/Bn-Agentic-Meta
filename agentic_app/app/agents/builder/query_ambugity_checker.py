
from typing import Literal, TypedDict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from agents.llm_factory import LLMFactory

class QueryAmbiguityCheckerState(TypedDict):
    """Type definition for query ambiguity checker output"""
    original_query: str  # The original input query
    normalized_query: str  # The normalized/corrected query
    is_ambiguous: Literal["YES", "NO"]  # Whether clarification is needed
    ai_question: str  # Either the clarifying question or the normalized query

class QueryAmbiguityChecker:

    @classmethod
    def get_query_parse_prompt(cls) -> ChatPromptTemplate:
        system_prompt = """
        You are a natural language query normalizer and corrector. and you are a intelligent agent that translates user queries into a english.
        -------------------------------------------------------------------------------------------------------
        ---Context for object name---
        example: Leads, Accounts, Contacts, Opportunities, Cases, Activities, Products, Quotes, Invoices, Solutions, Campaigns, Users, Teams
        -------------------------------------
        Your task: 
        input: task output
        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of your existing tools
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat N times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question


        Rules for task:
        - If the query is ambiguous, ask a clarifying question to the user to resolve ambiguity.
        - If the query is clear, provide the normalized query as the final answer.
        - Use the above format to reason about the query and decide if it is ambiguous or clear.
        - Do not skip any steps in the reasoning process.
        - Use tools to find field names if needed.
        - Always provide a final answer.
        
        ### Examples for task:
        input: show me my account
        {{
            "original_query": "show me my account",
            "normalized_query": "show me my account with account id  or unique identifier",
            "is_ambiguous": "Yes",
            "ai_question": "Which account do you want to see? Please provide the account ID, email, or name."
        }}
        
        input: show me all the lead
        {{
            "original_query": "show me all the lead",
            "normalized_query": "show me all leads",
            "is_ambiguous": "YES",
            "ai_question": "Which leads do you want to see? All leads, my leads, or top leads? If you want a specific lead, please specify the lead ID, email, or name."
        }}
        
        input: mujhe mere account dikhao
        {{
            "original_query": "mujhe mere account dikhao",
            "normalized_query": "show me my accounts",
            "is_ambiguous": "NO",
            "ai_question": "show me my accounts"
        }}
        
        input: मेरे सभी लीड दिखाओ
        {{
            "original_query": "मेरे सभी लीड दिखाओ",
            "normalized_query": "show me all leads",
            "is_ambiguous": "YES",
            "ai_question": "Which leads do you want to see? All leads, my leads, or top leads? If you want a specific lead, please specify the lead ID, email, or name."
        }}
        
        input: what is the of my case
        {{
            "original_query": "what is the of my case",
            "normalized_query": "what is the status of my case",
            "is_ambiguous": "YES",
            "ai_question": "Which case do you want to check the status for? Please provide the case ID or subject."
        }}
        

        Now, normalize this user query:
        {normalized_query}
        """
        return ChatPromptTemplate.from_messages([
            ("system", system_prompt)
        ])
    
    @classmethod
    def invoke(cls, normalized_query: str) -> QueryAmbiguityCheckerState:
        """
        Invoke the query ambiguity checker with a user query

        Args:
            normalized_query: The query to translate/normalize
            
        Returns:
            QueryAmbiguityCheckerState: The processed query state with normalization and ambiguity check
        """
        prompt = cls.get_query_parse_prompt()
        
        llm = LLMFactory.open_ai()
        structured_llm = llm.with_structured_output(QueryAmbiguityCheckerState)

        print("Invoking QueryAmbiguityChecker with user_query:", normalized_query)
        chain = prompt | structured_llm
        print("Chain created, invoking...")
        
        result = chain.invoke({"normalized_query": normalized_query})
        print("QueryAmbiguityChecker output:", result)

        # Ensure we return the full QueryAmbiguityCheckerState
        return result

    
