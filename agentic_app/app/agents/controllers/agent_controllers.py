from fastapi import APIRouter
from agents.rag_builder.rag_builder import RagBuilder
#from agents.rag_builder.rag_retriver import RagRetriever
from agents.rag_builder.vector_store import VectorStore
from agents.builder.agent_runner import AgentRunner
#from agents.builder.query_normalizer import QueryNormalizerAgent
from agents.builder.agent_graph import AgentExecutor
from agents.builder.query_translator import QueryTranslator
from agents.builder.main_agent import MainAgent

router = APIRouter()

@router.get("/invoke_agent_executor")
def query_normalize_agent(user_query:str):

    normalized_query = AgentExecutor().invoke(user_query)
    return {"response": normalized_query}   

@router.get("/greeting_agent")
def greeting_agent(user_query:str):

    normalized_query = AgentRunner().invoke(user_query)
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


# @router.get("/get_rag_context")
# def get_rag_context(question: str = "What is the capital of France?"):
#     rag_retriever = RagRetriever()
#     context = rag_retriever.invoke(question)
#     return {"rag_context": context}

# @router.get("/get_query_normalization")
# def get_query_normalization(question: str = "What is the capital of France?", structured: bool = True):
#     """
#     Get query normalization with option for structured or text output
    
#     Args:
#         question: The user query to normalize
#         structured: If True, returns AgentSchema format; if False, returns text
#     """
#     query_normalizer = QueryNormalizerAgent()
    
#     if structured:
#         # Return structured output (AgentSchema)
#         result = query_normalizer.invoke(question)
#         return {"structured_response": result.model_dump() if hasattr(result, 'model_dump') else result.__dict__}
#     else:
#         # Return text output for backward compatibility
#         context = query_normalizer.invoke_text(question)
#         return {"rag_context": context}
