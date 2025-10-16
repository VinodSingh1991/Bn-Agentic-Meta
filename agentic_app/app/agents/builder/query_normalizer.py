from agents.controllers.structured_output import AgentSchema, OutputSchema, DataField, Order
from langchain_core.prompts import ChatPromptTemplate
from agents.llm_factory import LLMFactory
from langgraph.prebuilt import create_react_agent
import os   
import json
from langgraph.checkpoint.memory import InMemorySaver
from agents.tools.base_tool import create_tools


class QueryNormalizerAgent:
    def __init__(self):
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        self.checkpointer = InMemorySaver()
        self.llm = LLMFactory().open_ai()
        self.structured_llm = self.llm.with_structured_output(AgentSchema)
    
    def agent_invoker(self, user_query: str) -> str:
        try:
            # Use the classic ReAct prompt format
            react_prompt = """Answer the following questions as best you can. You have access to the following tools:

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
            
            tools = self.create_tools()
                
            try:
                agent = create_react_agent(
                    model=self.llm,
                    tools=tools,
                    prompt=react_prompt,
                    checkpointer=self.checkpointer,
                    debug=False
                    
                )
            except Exception as agent_error:
                import traceback
                traceback.print_exc()
                raise agent_error
            
            # Create proper input format for the agent
            config = {"configurable": {"thread_id": "query_normalizer_thread"}}
            input_data = {"messages": [("user", user_query)]}
            
            # Invoke the agent with proper input format
            result = agent.invoke(input_data, config=config)
            
            # Extract the response from the agent's output
            final_response = ""
            if "messages" in result and len(result["messages"]) > 0:
                last_message = result["messages"][-1]
                
                if hasattr(last_message, 'content'):
                    final_response = last_message.content
                elif isinstance(last_message, dict) and 'content' in last_message:
                    final_response = last_message['content']
                else:
                    final_response = str(last_message)
            else:
                final_response = str(result)
            
            return final_response
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"Sorry, I encountered an error while processing your query: {str(e)}"
            
    
    def invoke(self, user_query: str) -> AgentSchema:
        """
        Main entry point to invoke the query normalizer agent
        
        Args:
            user_query (str): The user's query to be processed
            
        Returns:
            AgentSchema: Structured response with welcome message, output schemas, and open-end message
        """
        try:
            
            # Get the agent's text response
            agent_response = self.agent_invoker(user_query)
            
            # Convert to structured output
            
            return agent_response
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            
            error_response = self._create_fallback_structured_response(
                user_query, 
                f"Error occurred: {str(e)}"
            )
            return error_response
    