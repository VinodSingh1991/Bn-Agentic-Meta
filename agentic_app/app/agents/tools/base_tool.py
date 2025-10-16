from langchain_core.tools import tool
from agents.tools.get_field_by_field_name import get_field_by_field_name_and_object, get_field_by_object_name, get_field_by_object_name_and_label

def create_tools():
        """Convert functions to proper LangChain tools"""
        
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
        
        return [get_field_by_name_and_object_tool, get_fields_by_object_tool, get_field_by_object_and_label_tool]