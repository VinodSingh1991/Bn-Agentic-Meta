"""
Structured Output Parser

Handles parsing and conversion of agent responses to structured AgentSchema format.
"""

import json
from typing import Any, Dict

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseLanguageModel

from agents.controllers.structured_output import AgentSchema, OutputSchema, DataField, Order


class StructuredOutputParser:
    """Handles parsing of agent responses to structured format"""
    
    def __init__(self, structured_llm: BaseLanguageModel):
        """
        Initialize the parser with a structured LLM
        
        Args:
            structured_llm: LLM configured for structured output
        """
        self.structured_llm = structured_llm
        
    def parse_agent_response_to_structured(self, agent_response: str, user_query: str) -> AgentSchema:
        """
        Parse agent response and convert to structured AgentSchema format
        
        Args:
            agent_response: Raw response from the ReAct agent
            user_query: Original user query
            
        Returns:
            AgentSchema: Structured response
        """
        try:
            print(f"\n🔄 PARSING RESPONSE TO STRUCTURED FORMAT")
            print(f"📝 Original Query: {user_query}")
            print(f"🤖 Agent Response Length: {len(agent_response)}")
            
            # Create prompt for structured output generation
            structured_prompt = self._create_structured_prompt()
            
            print(f"🧠 Calling structured LLM...")
            prompt_messages = structured_prompt.format_messages(
                user_query=user_query,
                agent_response=agent_response
            )
            
            structured_response = self.structured_llm.invoke(prompt_messages)
            
            print(f"✅ Structured Response Generated")
            print(f"📦 Response Type: {type(structured_response)}")
            
            if isinstance(structured_response, AgentSchema):
                print(f"🎯 Direct AgentSchema object received")
                return structured_response
            else:
                print(f"⚠️ Non-AgentSchema response, attempting to parse...")
                return self._handle_non_schema_response(structured_response, user_query, agent_response)
                
        except Exception as e:
            print(f"❌ Error in structured parsing: {e}")
            import traceback
            traceback.print_exc()
            return self.create_fallback_structured_response(user_query, agent_response)
    
    def _create_structured_prompt(self) -> ChatPromptTemplate:
        """Create the prompt template for structured output generation"""
        return ChatPromptTemplate.from_messages([
            ("system", """You are a data analyst that converts natural language queries and field information into structured JSON format.

Based on the user query and the field information found, create a structured response with:
1. A welcome message addressing the user's query
2. Output schema with identified fields, filters, and metadata
3. An open-end message suggesting related queries

Guidelines:
- Extract object names (Account, Contact, Lead, etc.)
- Identify field names and types from the agent response
- Determine appropriate intent (GET, SUMMARIZE, AGGREGATE, etc.)
- Set reasonable limits and output formats
- Create meaningful welcome and open-end messages

Return a valid JSON structure matching the AgentSchema format."""),
            ("user", """
User Query: {user_query}

Agent Response with Field Information:
{agent_response}

Convert this into a structured AgentSchema JSON format with:
- welcome_message: A personalized greeting based on the query
- output_schemas: Array with the main OutputSchema containing:
  - object_name: Primary object being queried
  - role_id: Default to 1
  - intent: Query intent (GET, SUMMARIZE, etc.)
  - output_format: Appropriate format (TABLE, CARD, LIST, etc.)
  - data_fields: Fields found by the agent
  - filters: Any filtering fields identified
  - limit: Reasonable limit or 'ALL'
  - order: Default ordering
  - groupBy: Grouping fields if applicable
- open_end_message: Suggest related queries
""")
        ])
    
    def _handle_non_schema_response(self, structured_response: Any, user_query: str, agent_response: str) -> AgentSchema:
        """Handle non-AgentSchema responses by attempting to parse them"""
        # If it's a string, try to parse as JSON and create AgentSchema
        if isinstance(structured_response, str):
            try:
                data = json.loads(structured_response)
                return AgentSchema(**data)
            except Exception as parse_error:
                print(f"❌ Failed to parse JSON from string response: {parse_error}")
        
        # If it's a dict, try to create AgentSchema
        elif isinstance(structured_response, dict):
            try:
                return AgentSchema(**structured_response)
            except Exception as schema_error:
                print(f"❌ Failed to create AgentSchema from dict: {schema_error}")
        
        # Fallback: create a basic structured response
        return self.create_fallback_structured_response(user_query, agent_response)
    
    def create_fallback_structured_response(self, user_query: str, agent_response: str) -> AgentSchema:
        """
        Create a fallback structured response when parsing fails
        
        Args:
            user_query: Original user query
            agent_response: Agent's response (can be error message)
            
        Returns:
            AgentSchema: Basic fallback response
        """
        print(f"🔄 Creating fallback structured response")
        
        # Create a basic DataField for fallback
        fallback_field = DataField(
            roleid=1,
            object_name="Unknown",
            field_id=0,
            name="Unknown Field",
            FieldName="unknown_field",
            field_type="String"
        )
        
        # Create basic order
        fallback_order = Order(
            field=fallback_field,
            direction="ASC"
        )
        
        # Create output schema
        output_schema = OutputSchema(
            object_name="Unknown",
            role_id=1,
            intent="GET",
            output_format="TEXT",
            data_fields=[fallback_field],
            filters=[],
            limit=10,
            order=fallback_order,
            groupBy=[]
        )
        
        # Determine welcome message based on whether there was an error
        if "error" in agent_response.lower() or "sorry" in agent_response.lower():
            welcome_message = f"I encountered some difficulties processing your query: '{user_query}'"
        else:
            welcome_message = f"I found some information related to your query: '{user_query}'"
        
        return AgentSchema(
            welcome_message=welcome_message,
            output_schemas=[output_schema],
            open_end_message="Would you like to know more about specific fields or objects?"
        )
    
    def validate_structured_response(self, response: AgentSchema) -> bool:
        """
        Validate that a structured response has the required components
        
        Args:
            response: AgentSchema to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Check required fields
            if not response.welcome_message or not response.open_end_message:
                return False
                
            if not response.output_schemas or len(response.output_schemas) == 0:
                return False
                
            # Check each output schema
            for schema in response.output_schemas:
                if not schema.object_name or not schema.intent:
                    return False
                    
                if not schema.data_fields or len(schema.data_fields) == 0:
                    return False
                    
            return True
            
        except Exception:
            return False
    
    def enhance_structured_response(self, response: AgentSchema, user_query: str) -> AgentSchema:
        """
        Enhance a structured response with additional context if needed
        
        Args:
            response: Original structured response
            user_query: Original user query
            
        Returns:
            AgentSchema: Enhanced response
        """
        # Add query context to welcome message if it's too generic
        if len(response.welcome_message) < 50:
            response.welcome_message = f"Based on your query '{user_query}', {response.welcome_message.lower()}"
        
        # Enhance open-end message with query-specific suggestions
        if "would you like to know" in response.open_end_message.lower():
            if any(word in user_query.lower() for word in ['contact', 'lead', 'account']):
                response.open_end_message += " I can also help you explore relationships between these objects."
        
        return response