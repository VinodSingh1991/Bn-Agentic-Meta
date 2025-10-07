
from agents.llm_factory import LLMFactory
from agents.builder.query_normalizer import UserQueryNormalizer
from agents.builder.query_decompositaion import QueryDecomposition

class AgentBuilder:
    def __init__(self):
        # Don't instantiate AgentSchema here since it requires parameters
        # We'll create it when needed in the methods
        self.llm = LLMFactory().open_ai()
        self.query_builder = UserQueryNormalizer()
        self.query_decomposer = QueryDecomposition()
            
    def invoke(self, user_query: str) -> str:
        normalized_query = self.query_builder.invoke(user_query)
        response = self.query_decomposer.invoke(normalized_query)
        
        return {"normalized_query": normalized_query, "decomposed_queries": response}
    
