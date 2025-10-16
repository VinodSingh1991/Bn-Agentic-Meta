from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from agents.llm_factory import LLMFactory
from agents.controllers.structured_output import (
    OutputSchema, AgentSchema
)
from typing import Any
from agents.tools.base_tool import create_tools

class MainAgent:
    
    def __init__(self):
        self.llm = LLMFactory().open_ai()

    def get_prompt(self) -> ChatPromptTemplate:
        system_prompt = """
        You are an intelligent CRM assistant specializing in analyzing and processing user queries about CRM data.
        
        ### Available Context
        The following context contains the available CRM data fields and their descriptions:
        {context}

        ### Available Tools
        Use these tools to get field information:
        1. get_field_by_name_and_object_tool(field_name: str, object_name: str)
        2. get_fields_by_object_tool(object_name: str)
        3. get_field_by_object_and_label_tool(object_name: str, label: str)
        
        ### Response Format
        You must return an AgentSchema object with this structure:
        {{
                    "object_name": str,  # e.g., Account, Contact, Lead, Activity
                    "role_id": int,  # default to 1
                    "intent": str,  # GET, SUMMARIZE, AGGREGATE, POST, UPDATE, DELETE
                    "output_format": str,  # TABLE, CARD, LIST, TEXT, SUMMARY
                    "data_fields": [  # List of fields to retrieve
                        {{
                            "roleid": int,  # default to 1
                            "object_name": str,  # same as parent object_name
                            "field_id": int,  # from context
                            "name": str,  # display name from context
                            "FieldName": str,  # API name from context
                            "field_type": str  # data type from context
                        }}
                    ],
                    "filters": [  # Optional list of filter fields
                        {{
                            # Same structure as data_fields
                        }}
                    ],
                    "limit": int | "ALL",  # Number of records or "ALL"
                    "order": {{  # Sorting information
                        "field": {{  # DataField object
                            # Same structure as data_fields
                        }},
                        "direction": "ASC" | "DESC"
                    }},
                    "groupBy": [  # Optional list of grouping fields
                        {{
                            # Same structure as data_fields
                        }}
                    ]
                }}
        }}

        ### Instructions
        1. Analyze the user query to identify:
           - The object(s) they want to query (Lead, Account, etc.)
           - The specific fields they need
           - Any filtering, sorting, or grouping requirements
           - The type of operation (GET, SUMMARIZE, etc.)
           
        2. Use the tools to fetch field information when needed
        
        3. Structure the response exactly as shown above, ensuring:
           - All DataField objects have all required properties
           - Field names and IDs match the context exactly
           - Appropriate welcome and open-end messages
           - Correct intent and output format
        
        Now, analyze this query using the provided context:
        {user_query}
        """
        return ChatPromptTemplate.from_messages([
            ("system", system_prompt)
        ])

    def invoke(self, query: str, context: Any) -> OutputSchema:
        """
        Process a user query to generate structured CRM operation schemas
        
        Args:
            query: The user's CRM query to analyze
            state: Current agent state containing context and history
            
        Returns:
            AgentSchema: Complete response including welcome message, output schemas, and follow-up suggestions
        """
        prompt = self.get_prompt()
        
        # Create the LLM chain with structured output and tools
        # llm = self.llm.with_structured_output(OutputSchema)
        # chain = prompt | llm.bind_tools(create_tools()) | JsonOutputParser()
        
        llm_with_tools = self.llm.bind_tools(create_tools())
        llm_structured = llm_with_tools.with_structured_output(OutputSchema)
        
        chain = prompt | llm_structured
        
        # Execute chain with proper context and query
        result = chain.invoke({
            "user_query": query,
            "context": context
        })
        
        print(f"Main Agent processing query: '{query}'")
        print("Generated response:", result)
        return result

    
