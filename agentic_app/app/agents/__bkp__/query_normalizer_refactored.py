"""
QueryNormalizerAgent - Refactored

Simplified main agent class that orchestrates all components for query normalization.
This is the new modular version that replaces the monolithic implementation.
"""

from typing import Dict, Any

from agents.builder.base_agent import BaseAgent
from agents.builder.react_agent_handler import ReactAgentHandler
from agents.builder.structured_output_parser import StructuredOutputParser
from agents.controllers.structured_output import AgentSchema


class QueryNormalizerAgent(BaseAgent):
    """
    Main Query Normalizer Agent that orchestrates all components
    
    This agent uses ReAct reasoning to find relevant fields and metadata,
    then converts the results to structured AgentSchema format.
    """
    
    def __init__(self, thread_id: str = "query_normalizer_thread"):
        """
        Initialize the Query Normalizer Agent
        
        Args:
            thread_id: Thread identifier for conversation memory
        """
        # Initialize base agent functionality
        super().__init__(thread_id)
        
        # Initialize specialized components
        self._initialize_components()
        
        self.log_separator("QueryNormalizerAgent Initialized")
        self.log_success("All components loaded successfully")
    
    def _initialize_components(self):
        """Initialize all specialized components"""
        try:
            # Initialize ReAct agent handler
            self.react_handler = ReactAgentHandler(
                llm=self.llm,
                checkpointer=self.checkpointer
            )
            self.log_success("ReAct agent handler initialized")
            
            # Initialize structured output parser
            self.output_parser = StructuredOutputParser(
                structured_llm=self.structured_llm
            )
            self.log_success("Structured output parser initialized")
            
            # Validate tools
            if self.react_handler.validate_tools():
                self.log_success("All tools validated successfully")
            else:
                self.log_warning("Tool validation failed")
                
        except Exception as e:
            self.log_error("Failed to initialize components", e)
            raise
    
    def invoke(self, user_query: str) -> AgentSchema:
        """
        Main entry point to invoke the query normalizer agent
        
        Args:
            user_query (str): The user's query to be processed
            
        Returns:
            AgentSchema: Structured response with welcome message, output schemas, and open-end message
        """
        self.log_separator("QUERY NORMALIZER INVOCATION")
        self.log_step("Processing query", f"'{user_query}'")
        
        try:
            # Validate and clean the query
            cleaned_query = self.validate_query(user_query)
            self.log_success(f"Query validated: '{cleaned_query}'")
            
            # Get text response from ReAct agent
            self.log_step("Invoking ReAct agent...")
            agent_response = self.react_handler.invoke_agent(cleaned_query, self.thread_id)
            
            self.log_success(f"ReAct agent response received ({len(agent_response)} chars)")
            self.log_debug(f"Response preview: {agent_response[:150]}{'...' if len(agent_response) > 150 else ''}")
            
            # Convert to structured output
            self.log_step("Converting to structured output...")
            structured_response = self.output_parser.parse_agent_response_to_structured(
                agent_response, cleaned_query
            )
            
            # Validate and enhance the structured response
            if self.output_parser.validate_structured_response(structured_response):
                self.log_success("Structured response validated")
                enhanced_response = self.output_parser.enhance_structured_response(
                    structured_response, cleaned_query
                )
            else:
                self.log_warning("Structured response validation failed, using fallback")
                enhanced_response = structured_response
            
            self._log_structured_response_summary(enhanced_response)
            self.log_separator("INVOCATION COMPLETED SUCCESSFULLY")
            
            return enhanced_response
            
        except ValueError as ve:
            self.log_error(f"Validation error: {ve}")
            return self.output_parser.create_fallback_structured_response(
                user_query, f"Validation error: {str(ve)}"
            )
        except Exception as e:
            self.log_error("Error in invoke method", e)
            return self.output_parser.create_fallback_structured_response(
                user_query, f"Error occurred: {str(e)}"
            )
    
    def invoke_text(self, user_query: str) -> str:
        """
        Alternative method to get text response (for backward compatibility)
        
        Args:
            user_query (str): The user's query to be processed
            
        Returns:
            str: The agent's text response
        """
        self.log_separator("TEXT OUTPUT INVOCATION (BACKWARD COMPATIBILITY)")
        self.log_step("Processing query for text output", f"'{user_query}'")
        
        try:
            # Validate and clean the query
            cleaned_query = self.validate_query(user_query)
            
            # Get text response from ReAct agent
            response = self.react_handler.invoke_agent(cleaned_query, self.thread_id)
            
            self.log_success(f"Text response received ({len(response)} chars)")
            self.log_separator("TEXT INVOCATION COMPLETED")
            
            return response
            
        except ValueError as ve:
            error_msg = f"Please provide a valid query. Error: {str(ve)}"
            self.log_error(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"I'm sorry, I couldn't process your query. Please try again. Error: {str(e)}"
            self.log_error("Error in invoke_text method", e)
            return error_msg
    
    def test_structured_output(self, test_query: str = "Show me all contacts with email field") -> Dict[str, Any]:
        """
        Test method to demonstrate structured output
        
        Args:
            test_query (str): Test query to process
            
        Returns:
            Dict[str, Any]: Structured response as dictionary
        """
        self.log_separator("TESTING STRUCTURED OUTPUT")
        self.log_step("Running test", f"Query: '{test_query}'")
        
        try:
            structured_response = self.invoke(test_query)
            
            # Convert to dictionary for display
            response_dict = structured_response.dict()
            
            self._log_test_results(response_dict)
            self.log_separator("TEST COMPLETED SUCCESSFULLY")
            
            return response_dict
            
        except Exception as e:
            self.log_error("Error in test", e)
            return {"error": str(e), "test_query": test_query}
    
    def get_component_status(self) -> Dict[str, Any]:
        """
        Get status information about all components
        
        Returns:
            Dict with component status information
        """
        status = {
            "base_agent": {
                "llm_initialized": hasattr(self, 'llm') and self.llm is not None,
                "structured_llm_initialized": hasattr(self, 'structured_llm') and self.structured_llm is not None,
                "checkpointer_initialized": hasattr(self, 'checkpointer') and self.checkpointer is not None,
                "thread_id": self.thread_id
            },
            "react_handler": {
                "initialized": hasattr(self, 'react_handler') and self.react_handler is not None,
                "tools_count": len(self.react_handler.tools) if hasattr(self, 'react_handler') else 0,
                "tools_valid": self.react_handler.validate_tools() if hasattr(self, 'react_handler') else False
            },
            "output_parser": {
                "initialized": hasattr(self, 'output_parser') and self.output_parser is not None
            }
        }
        
        if hasattr(self, 'react_handler'):
            status["react_handler"]["tool_info"] = self.react_handler.get_tool_info()
        
        return status
    
    def _log_structured_response_summary(self, response: AgentSchema):
        """Log a summary of the structured response"""
        self.log_info("📊 STRUCTURED RESPONSE SUMMARY:")
        self.log_info(f"   Welcome Message: {response.welcome_message[:100]}...")
        self.log_info(f"   Output Schemas: {len(response.output_schemas)}")
        
        for i, schema in enumerate(response.output_schemas):
            self.log_info(f"   Schema {i+1}:")
            self.log_info(f"     Object: {schema.object_name}")
            self.log_info(f"     Intent: {schema.intent}")
            self.log_info(f"     Format: {schema.output_format}")
            self.log_info(f"     Fields: {len(schema.data_fields)}")
            
        self.log_info(f"   Open End Message: {response.open_end_message[:100]}...")
    
    def _log_test_results(self, response_dict: Dict[str, Any]):
        """Log test results"""
        self.log_info("📊 TEST RESULTS:")
        self.log_info(f"   Welcome Message: {response_dict.get('welcome_message', 'N/A')}")
        self.log_info(f"   Output Schemas: {len(response_dict.get('output_schemas', []))}")
        
        for i, schema in enumerate(response_dict.get('output_schemas', [])):
            self.log_info(f"   Schema {i+1}:")
            self.log_info(f"     Object: {schema.get('object_name', 'N/A')}")
            self.log_info(f"     Intent: {schema.get('intent', 'N/A')}")
            self.log_info(f"     Format: {schema.get('output_format', 'N/A')}")
            self.log_info(f"     Fields: {len(schema.get('data_fields', []))}")
            
        self.log_info(f"   Open End Message: {response_dict.get('open_end_message', 'N/A')}")


# Convenience functions for backward compatibility
def create_query_normalizer_agent(thread_id: str = "query_normalizer_thread") -> QueryNormalizerAgent:
    """
    Convenience function to create a QueryNormalizerAgent
    
    Args:
        thread_id: Thread identifier for conversation memory
        
    Returns:
        Initialized QueryNormalizerAgent
    """
    return QueryNormalizerAgent(thread_id)