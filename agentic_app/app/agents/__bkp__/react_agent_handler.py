"""
ReAct Agent Handler

Handles the creation and execution of ReAct agents for query processing.
"""

from typing import Dict, Any, List

from langchain_core.language_models import BaseLanguageModel
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver

from agents.builder.query_normalizer_tools import QueryNormalizerTools


class ReactAgentHandler:
    """Handles ReAct agent creation and execution"""
    
    def __init__(self, llm: BaseLanguageModel, checkpointer: InMemorySaver):
        """
        Initialize the ReAct agent handler
        
        Args:
            llm: Language model for the agent
            checkpointer: Memory checkpointer for conversation state
        """
        self.llm = llm
        self.checkpointer = checkpointer
        self.tools = QueryNormalizerTools.create_tools()
        self.react_prompt = self._create_react_prompt()
        
    def _create_react_prompt(self) -> str:
        """Create the ReAct prompt template"""
        return """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
    
    def create_agent(self, debug: bool = True):
        """
        Create a ReAct agent with the configured tools
        
        Args:
            debug: Whether to enable debug mode
            
        Returns:
            Configured ReAct agent
        """
        try:
            print(f"🔧 Creating ReAct agent with {len(self.tools)} tools...")
            
            # Log tool information
            QueryNormalizerTools.log_tool_info(print)
            
            agent = create_react_agent(
                model=self.llm,
                tools=self.tools,
                prompt=self.react_prompt,
                checkpointer=self.checkpointer,
                debug=debug
            )
            
            print(f"✅ ReAct agent created successfully")
            return agent
            
        except Exception as agent_error:
            print(f"❌ Error creating ReAct agent: {agent_error}")
            print(f"   Agent Error Type: {type(agent_error)}")
            import traceback
            traceback.print_exc()
            raise agent_error
    
    def invoke_agent(self, user_query: str, thread_id: str = "query_normalizer_thread") -> str:
        """
        Invoke the ReAct agent with a user query
        
        Args:
            user_query: User's query to process
            thread_id: Thread identifier for conversation memory
            
        Returns:
            Agent's response as string
        """
        try:
            print(f"🚀 STARTING REACT AGENT INVOCATION")
            print(f"📝 User Query: '{user_query}'")
            print(f"🧵 Thread ID: '{thread_id}'")
            
            # Create agent
            agent = self.create_agent(debug=True)
            
            # Prepare input data and config
            config = {"configurable": {"thread_id": thread_id}}
            input_data = {"messages": [("user", user_query)]}
            
            print(f"📨 Input Data: {input_data}")
            print(f"⚙️ Config: {config}")
            print(f"\n🤖 INVOKING REACT AGENT...")
            print(f"{'-'*60}")
            
            # Invoke the agent
            result = agent.invoke(input_data, config=config)
            
            print(f"\n{'-'*60}")
            print(f"📊 REACT AGENT EXECUTION COMPLETED")
            
            # Extract and return the response
            return self._extract_response_from_result(result)
            
        except Exception as e:
            print(f"\n❌ ERROR in ReAct agent invocation: {e}")
            print(f"   Error Type: {type(e)}")
            import traceback
            print(f"   Full Traceback:")
            traceback.print_exc()
            print(f"{'='*60}\n")
            return f"Sorry, I encountered an error while processing your query: {str(e)}"
    
    def _extract_response_from_result(self, result: Dict[str, Any]) -> str:
        """
        Extract the final response from the agent's result
        
        Args:
            result: Raw result from agent invocation
            
        Returns:
            Extracted response string
        """
        print(f"📦 Raw Result Type: {type(result)}")
        print(f"📦 Raw Result Keys: {result.keys() if isinstance(result, dict) else 'Not a dict'}")
        
        # Process messages in the result
        if "messages" in result:
            return self._extract_from_messages(result["messages"])
        else:
            print(f"   ⚠️ No messages found in result, using full result")
            return str(result)
    
    def _extract_from_messages(self, messages: List[Any]) -> str:
        """
        Extract response from messages list
        
        Args:
            messages: List of messages from agent result
            
        Returns:
            Extracted response string
        """
        print(f"\n💬 PROCESSING MESSAGES ({len(messages)} total):")
        
        for i, msg in enumerate(messages):
            msg_type = msg.__class__.__name__ if hasattr(msg, '__class__') else type(msg)
            content_preview = str(msg)[:200] + "..." if len(str(msg)) > 200 else str(msg)
            print(f"   Message {i+1} ({msg_type}): {content_preview}")
        
        # Extract from the last message
        if messages:
            last_message = messages[-1]
            print(f"\n🎯 EXTRACTING FROM LAST MESSAGE:")
            print(f"   Message Type: {type(last_message)}")
            
            return self._extract_content_from_message(last_message)
        else:
            return "No response messages found"
    
    def _extract_content_from_message(self, message: Any) -> str:
        """
        Extract content from a single message
        
        Args:
            message: Message object to extract from
            
        Returns:
            Extracted content string
        """
        if hasattr(message, 'content'):
            content = message.content
            print(f"   ✅ Extracted via .content: {content[:100]}...")
            return content
        elif isinstance(message, dict) and 'content' in message:
            content = message['content']
            print(f"   ✅ Extracted via ['content']: {content[:100]}...")
            return content
        else:
            content = str(message)
            print(f"   ⚠️ Fallback to str(): {content[:100]}...")
            return content
    
    def get_tool_info(self) -> Dict[str, Any]:
        """
        Get information about the available tools
        
        Returns:
            Dictionary with tool information
        """
        tool_info = {
            "count": len(self.tools),
            "tools": []
        }
        
        for tool in self.tools:
            tool_data = {
                "name": getattr(tool, 'name', 'Unknown'),
                "description": getattr(tool, 'description', 'No description'),
                "type": type(tool).__name__,
                "args": getattr(tool, 'args', None)
            }
            tool_info["tools"].append(tool_data)
        
        return tool_info
    
    def validate_tools(self) -> bool:
        """
        Validate that all tools are properly configured
        
        Returns:
            bool: True if all tools are valid
        """
        try:
            for tool in self.tools:
                if not hasattr(tool, 'name') or not hasattr(tool, 'description'):
                    print(f"❌ Tool missing required attributes: {tool}")
                    return False
            
            print(f"✅ All {len(self.tools)} tools are properly configured")
            return True
            
        except Exception as e:
            print(f"❌ Error validating tools: {e}")
            return False