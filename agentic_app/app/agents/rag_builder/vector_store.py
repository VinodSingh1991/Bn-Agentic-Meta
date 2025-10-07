import os
import json
from langchain_chroma import Chroma
from langchain.schema import Document
from agents.llm_factory import LLMFactory


class VectorStore:
    def __init__(self):
        self.embeddings = LLMFactory().open_ai_embeddings()
        self.store_directory = self._get_vector_db_path()
        self.vector_store_instance = None
        
    def _get_vector_db_path(self):
        """Get the absolute path for the local vector database"""
        # Get the current working directory or app directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Go up to the app directory (assuming this file is in app/agents/rag_builder/)
        app_dir = os.path.dirname(os.path.dirname(current_dir))
        # Create the local_vector_db path
        vector_db_path = os.path.join(app_dir, "local_vector_db")
        
        # Ensure the directory exists
        os.makedirs(vector_db_path, exist_ok=True)
        
        print(f"Vector DB path: {vector_db_path}")
        return vector_db_path
    
    def get_vector_store_instance(self):
        return self.vector_store_instance
    
    def get_vector_store(self, documents, persist_directory=None):
        """
        Create or load a vector store with documents
        
        Args:
            documents: List of documents to add to the vector store
            persist_directory: Optional custom directory path. If None, uses default path
            
        Returns:
            Chroma vector store instance
        """
        if persist_directory is None:
            persist_directory = self.store_directory
        
        # Ensure the persist directory exists
        os.makedirs(persist_directory, exist_ok=True)
        
        print(f"Creating/Loading vector store at: {persist_directory}")
        
        try:
            self.vector_store_instance = Chroma.from_documents(
                documents,
                self.embeddings,
                collection_name="worknext_agent",
                persist_directory=persist_directory
            )
            
            # Try to persist if method exists (for backward compatibility)
            if hasattr(self.vector_store_instance, 'persist'):
                self.vector_store_instance.persist()
                print("Vector store persisted successfully")
            else:
                print("Vector store auto-persisted (no explicit persist needed)")

            return self.vector_store_instance
            
        except Exception as e:
            print(f"Error creating vector store: {e}")
            raise
    
    def build_vector_store(self, documents, persist_directory=None):
        """
        Build vector store with better error handling and options
        
        Args:
            documents: List of documents to add
            persist_directory: Optional directory path
            
        Returns:
            Chroma vector store instance
        """
        if persist_directory is None:
            persist_directory = self.store_directory
        
        os.makedirs(persist_directory, exist_ok=True)
        print(f"Building vector store at: {persist_directory}")
        
        try:
            # Check if vector store already exists
            existing_store = self.load_existing_vector_store(persist_directory)
            
            if existing_store is not None:
                print("Existing vector store found. Adding documents to existing store.")
                # Add documents to existing store
                existing_store.add_documents(documents)
                return existing_store
            else:
                print("Creating new vector store.")
                # Create new vector store
                return self.get_vector_store(documents, persist_directory)
                
        except Exception as e:
            print(f"Error in build_vector_store: {e}")
            # Fallback: try to create new store
            return self.get_vector_store(documents, persist_directory)
        
    def load_existing_vector_store(self, persist_directory=None):
        """
        Load an existing vector store without adding new documents
        
        Args:
            persist_directory: Optional custom directory path. If None, uses default path
            
        Returns:
            Chroma vector store instance or None if not found
        """
        if persist_directory is None:
            persist_directory = self.store_directory
            
        if not os.path.exists(persist_directory):
            print(f"Vector store directory not found: {persist_directory}")
            return None
            
        try:
            vector_store = Chroma(
                embedding_function=self.embeddings,
                collection_name="worknext_agent",
                persist_directory=persist_directory
            )
            print(f"Loaded existing vector store from: {persist_directory}")
            return vector_store
        except Exception as e:
            print(f"Error loading vector store: {e}")
            return None
        
    def delete_vector_store(self, persist_directory=None, force=False):
        """
        Delete the entire vector store and its persisted files.
        
        Args:
            persist_directory (str, optional): Path of the vector DB to delete. Defaults to self.store_directory.
            force (bool, optional): If True, deletes without confirmation. Defaults to False.
        
        Returns:
            bool: True if deleted successfully, False otherwise.
        """
        import shutil

        if persist_directory is None:
            persist_directory = self.store_directory

        # Safety confirmation if not forced
        if not force:
            confirm = input(f"⚠️ Are you sure you want to delete vector DB at '{persist_directory}'? (yes/no): ")
            if confirm.lower() != "yes":
                print("❌ Deletion cancelled.")
                return False

        # Try deleting persisted Chroma data
        try:
            # Step 1: Delete Chroma collection data
            if self.vector_store_instance is not None:
                try:
                    self.vector_store_instance.delete_collection()
                    print("✅ Deleted Chroma collection from memory.")
                except Exception as e:
                    print(f"⚠️ Warning: Failed to delete collection in memory: {e}")

            # Step 2: Delete persisted files
            if os.path.exists(persist_directory):
                shutil.rmtree(persist_directory)
                print(f"🧹 Deleted vector DB folder: {persist_directory}")
            else:
                print("⚠️ Persist directory not found — skipping file deletion.")

            # Step 3: Clear in-memory instance
            self.vector_store_instance = None
            print("🧠 Cleared vector store instance reference.")

            return True

        except Exception as e:
            print(f"❌ Error deleting vector store: {e}")
            return False
