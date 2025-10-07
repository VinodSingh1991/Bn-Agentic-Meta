from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
import os

class LLMFactory:
    def __init__(self):
        self.open_ai_api_key = os.getenv("OPENAI_API_KEY")

    def open_ai(self):
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=1024,
            openai_api_key=self.open_ai_api_key
        )    
        
    def open_ai_embeddings(self):
        return OpenAIEmbeddings(
            model="text-embedding-3-large",
            openai_api_key=self.open_ai_api_key
        )
        
        