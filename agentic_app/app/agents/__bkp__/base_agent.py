"""
Base Agent Class

Provides common functionality for all agents including:
- LLM initialization and configuration
- Environment setup
- Common utilities and logging
"""

import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from agents.llm_factory import LLMFactory
from agents.controllers.structured_output import AgentSchema
from langgraph.checkpoint.memory import InMemorySaver


class BaseAgent(ABC):
    """Base class for all agents with common functionality"""
    
    def __init__(self, thread_id: Optional[str] = None):
        """
        Initialize base agent with common components
        
        Args:
            thread_id: Optional thread identifier for conversation memory
        """
        self._setup_environment()
        self._initialize_llm()
        self._setup_memory(thread_id)
        
    def _setup_environment(self):
        """Setup environment variables"""
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY environment variable is required")
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        
    def _initialize_llm(self):
        """Initialize LLM instances"""
        self.llm = LLMFactory().open_ai()
        self.structured_llm = self.llm.with_structured_output(AgentSchema)
        
    def _setup_memory(self, thread_id: Optional[str] = None):
        """Setup conversation memory"""
        self.checkpointer = InMemorySaver()
        self.thread_id = thread_id or self.__class__.__name__.lower() + "_thread"
        
    def get_config(self) -> Dict[str, Any]:
        """Get agent configuration for LangGraph"""
        return {"configurable": {"thread_id": self.thread_id}}
        
    def log_info(self, message: str, emoji: str = "ℹ️"):
        """Log informational message"""
        print(f"{emoji} {message}")
        
    def log_success(self, message: str):
        """Log success message"""
        self.log_info(message, "✅")
        
    def log_error(self, message: str, exception: Optional[Exception] = None):
        """Log error message with optional exception details"""
        print(f"❌ {message}")
        if exception:
            print(f"   Error Type: {type(exception)}")
            print(f"   Error Details: {str(exception)}")
            import traceback
            traceback.print_exc()
            
    def log_warning(self, message: str):
        """Log warning message"""
        self.log_info(message, "⚠️")
        
    def log_debug(self, message: str):
        """Log debug message"""
        self.log_info(message, "🔍")
        
    def log_step(self, step: str, details: str = ""):
        """Log processing step"""
        print(f"🚀 {step}")
        if details:
            print(f"   {details}")
            
    def log_separator(self, title: str = "", length: int = 60):
        """Log section separator"""
        if title:
            print(f"\n{'='*length}")
            print(f"🌟 {title}")
            print(f"{'='*length}")
        else:
            print(f"{'-'*length}")
            
    @abstractmethod
    def invoke(self, user_query: str) -> Any:
        """
        Main entry point for agent invocation
        Must be implemented by subclasses
        
        Args:
            user_query: User's input query
            
        Returns:
            Agent's response (format depends on implementation)
        """
        pass
        
    def validate_query(self, user_query: str) -> str:
        """
        Validate and clean user query
        
        Args:
            user_query: Raw user input
            
        Returns:
            Cleaned query string
            
        Raises:
            ValueError: If query is empty or invalid
        """
        if not user_query or not user_query.strip():
            raise ValueError("Query cannot be empty")
            
        cleaned_query = user_query.strip()
        
        if len(cleaned_query) > 1000:  # Reasonable limit
            self.log_warning(f"Query length ({len(cleaned_query)}) exceeds recommended limit")
            
        return cleaned_query