from langchain_core.documents import Document
from typing_extensions import List, TypedDict

from agents.rag_builder.vector_store import VectorStore


class State(TypedDict):
    question: str
    context: List[Document]


class RagRetriever:
    def __init__(self):
        self.vector_store = (
            VectorStore().load_existing_vector_store()
        )  # Initialize with empty list

    def invoke(self, question: str) -> State:

        retrieved_docs = self.vector_store.similarity_search(question, k=3)

        return {"user__orignal_query": question, "context": retrieved_docs}

    def invoke_list(self, decomposed_queries: list[str]) -> List[Document]:

        try:
            if not decomposed_queries:
                return []

            rag_contexts = []
            for query in decomposed_queries:
                contexts = self.vector_store.similarity_search(query, k=2)
                
                if contexts:
                    # Filter contexts to only include documents with valid data_fields
                    filtered_contexts = []
                    for doc in contexts:
                        if "data_fields" in doc.metadata:
                            data_field = doc.metadata["data_fields"]
                            # Check if data_field is valid (not None, not empty list, not empty string)
                            if data_field is not None and data_field != "" and not (isinstance(data_field, list) and len(data_field) == 0):
                                filtered_contexts.append(doc)
                    
                    # Only append if we have valid contexts with data_fields
                    if filtered_contexts:
                        rag_contexts.append({"query": query, "contexts": filtered_contexts})
            
            return rag_contexts
        
        except Exception as e:
            return []
