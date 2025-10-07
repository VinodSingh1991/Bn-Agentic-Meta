from agents.rag_builder.vector_store import VectorStore
from files_handler.rag_file_loader import RagFileLoader
import os
import json
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings  # or HuggingFaceEmbeddings


class RagBuilder:
    def __init__(self):
        self.rag_files_loader = RagFileLoader()
        self.vector_store = VectorStore()

    def load_all_rag_files(self):
        return self.rag_files_loader.load_all_rag_files()

    def get_vector_documents(self):
        documents_list = self.load_all_rag_files()

        vector_documents = []

        if documents_list:
            for item in documents_list:
                query_text = item.get("query", "")
                meta_data = item.get("meta_data", {})

                # Clean metadata to ensure all values are scalars
                clean_metadata = self._clean_metadata(meta_data)
                
                # Create document with clean metadata
                doc = Document(page_content=str(query_text), metadata=clean_metadata)
                vector_documents.append(doc)

        return vector_documents
    
    def _clean_metadata(self, metadata):
        """
        Clean metadata to ensure all values are scalar types acceptable by vector stores
        
        Args:
            metadata (dict): Original metadata
            
        Returns:
            dict: Cleaned metadata with scalar values only
        """
        import json
        
        clean_meta = {}
        
        for key, value in metadata.items():
            if isinstance(value, (str, int, float, bool)) or value is None:
                # Already scalar, keep as is
                clean_meta[key] = value
            elif isinstance(value, list):
                if len(value) == 0:
                    clean_meta[key] = ""
                elif len(value) == 1 and isinstance(value[0], dict):
                    # Single dict in list - flatten it
                    for sub_key, sub_value in value[0].items():
                        clean_meta[f"{key}_{sub_key}"] = str(sub_value) if not isinstance(sub_value, (str, int, float, bool)) else sub_value
                else:
                    # Convert list to JSON string
                    clean_meta[key] = json.dumps(value)
            elif isinstance(value, dict):
                # Convert dict to JSON string
                clean_meta[key] = json.dumps(value)
            else:
                # Convert any other type to string
                clean_meta[key] = str(value)
        
        return clean_meta

    def build_documents(self):
        v_documents = self.get_vector_documents()
        db_status = self.vector_store.get_vector_store(v_documents)

        return {"status": f"✅ Loaded {len(v_documents)} documents into Chroma"}
