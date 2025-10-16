
from agents.llm_factory import LLMFactory
from agents.builder.query_translator import QueryTranslator
from agents.builder.query_decompositaion import QueryDecomposition
from agents.builder.gretting_agent import GrettingAgent

class AgentRunner:
    def __init__(self):
        # Don't instantiate AgentSchema here since it requires parameters
        # We'll create it when needed in the methods
        self.llm = LLMFactory().open_ai()
    
    @classmethod
    def invoke(cls, user_query: str) -> str:
        normalized_query = GrettingAgent.invoke(user_query)
        #response = QueryDecomposition.invoke(normalized_query)
        
        return {"normalized_query": normalized_query, "decomposed_queries": normalized_query}
    
