from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
import os

class LLMFactory:
    @classmethod
    def open_ai(cls):
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=1024,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

    @classmethod
    def open_ai_structured_llm(cls, structured_output=None):
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_tokens=1024,
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            structured_output=structured_output
        )

    @classmethod
    def open_ai_embeddings(cls):
        return OpenAIEmbeddings(
            model="text-embedding-3-large",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        