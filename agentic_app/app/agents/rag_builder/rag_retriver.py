from langchain_core.documents import Document
from typing_extensions import List, TypedDict

from agents.rag_builder.vector_store import VectorStore

class State(TypedDict):
    question: str
    context: List[Document]

class RagRetriever:
    def __init__(self):
        self.vector_store = VectorStore().load_existing_vector_store()  # Initialize with empty list
    
    
    def invoke(self, question: str) -> State:

        retrieved_docs = self.vector_store.similarity_search(question, k=3)
        
        return {
            "user__orignal_query": question,
            "context": retrieved_docs
        }
        
        