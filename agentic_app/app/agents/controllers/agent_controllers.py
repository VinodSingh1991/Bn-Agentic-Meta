from fastapi import APIRouter
from agents.rag_builder.rag_builder import RagBuilder
from agents.rag_builder.rag_retriver import RagRetriever
from agents.rag_builder.vector_store import VectorStore
from agents.builder.agent_builder import AgentBuilder

router = APIRouter()

@router.get("/run_normalize_query_agent")
def query_normalize_agent(user_query:str):
    agent_builder = AgentBuilder()
    normalized_query = agent_builder.invoke(user_query)
    return {"normalized_query": normalized_query}   

@router.get("/delete_vector_store")
def delete_vector_store():
    rag_builder = VectorStore()
    success = rag_builder.delete_vector_store(force=True)
    if success:
        return {"message": "Vector store deleted successfully"}
    else:
        return {"message": "Failed to delete vector store"}, 500


@router.get("/create_vector_store")
def create_vector_store():
    rag_builder = RagBuilder()
    docs = rag_builder.build_documents()
    return {"listing": "listing file has been created", "documents": docs}


@router.get("/get_rag_context")
def get_rag_context(question: str = "What is the capital of France?"):
    rag_retriever = RagRetriever()
    context = rag_retriever.invoke(question)
    return {"rag_context": context}

