
from typing import Dict, Any, List, TypedDict
from agents.llm_factory import LLMFactory
from agents.builder.query_translator import QueryTranslator
from agents.builder.query_decompositaion import QueryDecomposition
from langgraph.graph import StateGraph, START, END
from agents.rag_builder.rag_retriver import RagRetriever
from agents.builder.gretting_agent import GrettingAgent
from agents.controllers.structured_output import OutputSchema
from agents.builder.main_agent import MainAgent
from agents.builder.query_ambugity_checker import QueryAmbiguityChecker

class AgentState(TypedDict):
    """State schema for the agent workflow"""
    query: str
    normalized_query: str
    decomposed_queries: List[str]
    rag_contexts: List[Dict[str, Any]]
    agent_output: List[OutputSchema]
    isQueryGreeting: bool
    welcomeMessage: str
    open_end_message: str
    is_ambiguous: bool
    ai_question: str
    clarification_needed: bool
    active_query: int

class AgentExecutor:
    def __init__(self):
        self.llm = LLMFactory().open_ai()
        self.workflow = self._build_workflow()
        self.rag_retriever = RagRetriever()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        # Add nodes
        workflow.add_node("normalize_query", self.normalize_query)
        workflow.add_node("greeting_query_checker", self.greeting_query_checker)
        workflow.add_node("response_with_ai_message", self.response_with_ai_message)
        workflow.add_node("decompose_query", self.decompose_query)
        workflow.add_node("get_rag_contexts", self.get_rag_contexts)
        workflow.add_node("finalize_output", self.finalize_output)
        workflow.add_node("get_output", self.get_output)
        # Add edges
        workflow.add_edge(START, "normalize_query")
        workflow.add_edge("normalize_query", "greeting_query_checker")
        workflow.add_conditional_edges("greeting_query_checker", self.greeting_conditional)
        workflow.add_conditional_edges("response_with_ai_message", self.query_ambiguity_checker)
        workflow.add_edge("decompose_query", "get_rag_contexts")
        workflow.add_edge("get_rag_contexts", "get_output")
        workflow.add_edge("get_output", "finalize_output")
        workflow.add_edge("finalize_output", END)
        return workflow.compile()
    
    # Conditional edge: if greeting, go to END; else, go to decompose_query
    def greeting_conditional(self, state: AgentState):
        # Only end if greeting is explicitly YES, otherwise continue to decompose_query
        if state.get("isQueryGreeting") is True:
            return END
        return "response_with_ai_message"
    
    def query_ambiguity_checker(self, state: AgentState) -> AgentState:
        """Check if the query is ambiguous and needs clarification"""
        # Placeholder for ambiguity checking logic
        # For now, we assume all queries are clear
        if state.get("is_ambiguous") is True:
            return "finalize_output"
        
        return "decompose_query"
    
    def normalize_query(self, state: AgentState) -> AgentState:
        """Normalize the user query"""
        try:
            query = state["query"]
            if not query or not query.strip():
                state["normalized_query"] = ""
                return state
                
            normalized_query = QueryTranslator.invoke(query.strip())
            state["normalized_query"] = normalized_query or query.strip()
        except Exception as e:
            # Fallback to original query if normalization fails
            state["normalized_query"] = state["query"]
        return state

    def response_with_ai_message(self, state: AgentState) -> Any:
        """Check the greeting Message"""
        response = QueryAmbiguityChecker().invoke(state["normalized_query"])
        if response.get("is_ambiguous") == "YES":
            state["is_ambiguous"] = True
            state["agent_output"] = {
                "original_query": state["query"],
                "ai_question": response.get("ai_question", ""),
                "clarification_needed": True
            }
        else: 
            state["is_ambiguous"] = False
        return state
   
    def greeting_query_checker(self, state: AgentState) -> Any:
        """Check the greeting Message"""
        is_greeting = GrettingAgent().invoke(state["query"])
        if is_greeting.get("greeting") == "YES":
            state["isQueryGreeting"] = True
            state["welcomeMessage"] = is_greeting.get("greetingReply")
            state["agent_output"] = {
                "original_query": state["query"],
                "welcomeMessage": state["welcomeMessage"],
                "ai_question": "",
                "clarification_needed": False
            }
        else:
            state["isQueryGreeting"] = False
        return state

    def decompose_query(self, state: AgentState) -> AgentState:
        """Decompose the normalized query into smaller queries"""
        try:
            normalized_query = state["normalized_query"]
            if not normalized_query:
                state["decomposed_queries"] = []
                return state
                
            decomposed_queries = QueryDecomposition.invoke(normalized_query)
            # Ensure we always have a list
            if isinstance(decomposed_queries, list):
                state["decomposed_queries"] = decomposed_queries
                
                
            else:
                state["decomposed_queries"] = [str(decomposed_queries)]
        except Exception as e:
            # Fallback to single query if decomposition fails
            state["decomposed_queries"] = [state["normalized_query"]]
        return state
    
    def get_rag_contexts(self, state: AgentState) -> AgentState:
        """Fetch RAG contexts for the decomposed queries"""
        try:
            decomposed_queries = state["decomposed_queries"]
            if not decomposed_queries:
                state["rag_contexts"] = []
                return state
            
            rag_contexts = self.rag_retriever.invoke_list(decomposed_queries)
            state["rag_contexts"] = rag_contexts
        except Exception as e:
            state["rag_contexts"] = []  # Fallback to empty list on error
        return state
    
    def get_output(self, state: AgentState) -> AgentState:
        """Fetch RAG contexts for the decomposed queries"""
        
        agent_output_list = []
        
        try:
            agent_output = state["agent_output"]
            decomposed_queries = state["decomposed_queries"]

            if not agent_output or decomposed_queries.count == 0:
                state["agent_output"] = []

            for decomposed_query in decomposed_queries:
                state["active_query"] = decomposed_query
                print("The active query is:", decomposed_query)
                # Create a new MainAgent instance and invoke with proper state
                main_agent = MainAgent()
                query_result = main_agent.invoke(
                    query=decomposed_query,
                    context=state["rag_contexts"]
                )
                print("Query result:", query_result)
                agent_output_list.append(query_result)
                
            state["agent_output"] = agent_output_list
        except Exception as e:
            state["agent_output"] = []  # Fallback to empty list on error
        return state
    
    def finalize_output(self, state: AgentState) -> AgentState:
        """Finalize the agent output"""
        
        response = {
            "welcomeMessage": state.get("welcomeMessage", "Here is your response"),
            "agent_output": state["agent_output"],
            "end_message": state.get("end_message", "Thank you for your query!"),
            "ai_question": state.get("ai_question", ""),
            "clarification_needed": state.get("clarification_needed", False),
        }
        
        state["agent_output"] = response
        return state
    
    def invoke(self, user_query: str) -> Dict[str, Any]:
        """
        Execute the agent workflow
        
        Args:
            user_query: The user's input query
            
        Returns:
            Dict containing the processed results
        """
        try:
            if not user_query or not user_query.strip():
                return {
                    "original_query": user_query,
                    "normalized_query": "",
                    "decomposed_queries": [],
                    "rag_contexts": [],
                    "error": "Empty query provided"
                }
            
            initial_state = AgentState(
                query=user_query.strip(),
                normalized_query="",
                rag_contexts=[],
                decomposed_queries=[],
                agent_output=""
            )
            
            result = self.workflow.invoke(initial_state)
            return result["agent_output"]
            
        except Exception as e:
            return {
                "original_query": user_query,
                "normalized_query": "",
                "decomposed_queries": [],
                "rag_contexts": [],
                "error": f"Workflow execution failed: {str(e)}"
            }
    
    