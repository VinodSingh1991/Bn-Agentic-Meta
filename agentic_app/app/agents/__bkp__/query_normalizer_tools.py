"""
Query Normalizer Tools

Contains all LangChain tools used by the QueryNormalizerAgent for field discovery and information retrieval.
"""

from typing import List
from langchain_core.tools import tool

from agents.tools.get_field_by_field_name import (
    get_field_by_field_name_and_object, 
    get_field_by_object_name, 
    get_field_by_object_name_and_label
)


class QueryNormalizerTools:
    """Factory class for creating query normalizer tools"""
    
    @staticmethod
    def create_tools() -> List:
        """
        Create and return all tools for the QueryNormalizerAgent
        
        Returns:
            List of LangChain tools
        """
        
        @tool
        def get_field_by_name_and_object_tool(field_name: str, object_name: str) -> str:
            """Get field information by field name and object name.
            
            Args:
                field_name: The name of the field to search for
                object_name: The name of the object (e.g., Lead, Contact, Account)
                
            Returns:
                Field information as a string
            """
            try:
                result = get_field_by_field_name_and_object(field_name, object_name)
                return str(result) if result else f"No field found with name '{field_name}' in object '{object_name}'"
            except Exception as e:
                return f"Error searching for field: {str(e)}"
        
        @tool
        def get_fields_by_object_tool(object_name: str) -> str:
            """Get all fields for a specific object.
            
            Args:
                object_name: The name of the object (e.g., Lead, Contact, Account)
                
            Returns:
                List of fields for the object as a string
            """
            try:
                result = get_field_by_object_name(object_name)
                if result:
                    return f"Found {len(result)} fields for {object_name}: " + str(result)
                else:
                    return f"No fields found for object '{object_name}'"
            except Exception as e:
                return f"Error getting fields for object: {str(e)}"
        
        @tool
        def get_field_by_object_and_label_tool(object_name: str, label: str) -> str:
            """Get field information by object name and field label.
            
            Args:
                object_name: The name of the object (e.g., Lead, Contact, Account)
                label: The display label of the field
                
            Returns:
                Field information as a string
            """
            try:
                result = get_field_by_object_name_and_label(object_name, label)
                return str(result) if result else f"No field found with label '{label}' in object '{object_name}'"
            except Exception as e:
                return f"Error searching for field by label: {str(e)}"
        
        return [
            get_field_by_name_and_object_tool, 
            get_fields_by_object_tool, 
            get_field_by_object_and_label_tool
        ]
    
    @staticmethod
    def get_tool_descriptions() -> List[str]:
        """
        Get descriptions of all available tools
        
        Returns:
            List of tool descriptions
        """
        tools = QueryNormalizerTools.create_tools()
        descriptions = []
        
        for tool in tools:
            name = getattr(tool, 'name', 'Unknown')
            description = getattr(tool, 'description', 'No description')
            descriptions.append(f"{name}: {description}")
            
        return descriptions
    
    @staticmethod
    def log_tool_info(logger_func=print):
        """
        Log information about all available tools
        
        Args:
            logger_func: Function to use for logging (default: print)
        """
        tools = QueryNormalizerTools.create_tools()
        
        logger_func("🔧 Available Query Normalizer Tools:")
        for i, tool in enumerate(tools, 1):
            tool_name = getattr(tool, 'name', 'Unknown')
            tool_desc = getattr(tool, 'description', 'No description')
            tool_type = type(tool).__name__
            
            logger_func(f"   {i}. {tool_name} (Type: {tool_type})")
            logger_func(f"      Description: {tool_desc[:100]}{'...' if len(tool_desc) > 100 else ''}")
            
            # Log additional tool details if available
            if hasattr(tool, 'args'):
                logger_func(f"      Args: {getattr(tool, 'args', 'No args')}")


# Convenience function for backward compatibility
def create_query_normalizer_tools() -> List:
    """
    Convenience function to create query normalizer tools
    
    Returns:
        List of LangChain tools
    """
    return QueryNormalizerTools.create_tools()