import json
import os
import hashlib
from typing import Dict, Any, List
from jsonschema import validate, ValidationError

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MAX_RETRIES = 3

# Simple in-memory cache for deterministic results
_llm_cache = {}

def _generate_cache_key(messages: List[Dict], schema: Dict) -> str:
    """Generate a cache key for the LLM call"""
    # Create a stable string representation of the input
    cache_data = {
        'messages': messages,
        'schema': schema
    }
    cache_string = json.dumps(cache_data, sort_keys=True)
    return hashlib.md5(cache_string.encode()).hexdigest()

def call_llm(messages, schema, max_tokens=500, temperature=0.0):
    """
    LangChain-based LLM wrapper for calling OpenAI with JSON schema validation and caching.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        schema: JSON schema for validation
        max_tokens: Maximum tokens in response
        temperature: Temperature for response generation (0.0 for deterministic)
        
    Returns:
        Dict: Validated JSON response
        
    Raises:
        ValueError: If no valid response after retries
    """
    # Check cache first for deterministic queries
    if temperature == 0.0:
        cache_key = _generate_cache_key(messages, schema)
        if cache_key in _llm_cache:
            print(f"[CACHE HIT] Returning cached result for query")
            return _llm_cache[cache_key]
    
    # Initialize ChatOpenAI with enhanced deterministic configuration
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=temperature,
        max_tokens=max_tokens,
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        max_retries=MAX_RETRIES,
        # Enhanced deterministic settings
        seed=42,  # Fixed seed for reproducibility
        top_p=1.0,  # Use full probability distribution
        frequency_penalty=0.0,  # No frequency penalty
        presence_penalty=0.0,   # No presence penalty
    )
    
    # Initialize JSON output parser
    json_parser = JsonOutputParser()
    
    # Convert messages to LangChain format
    langchain_messages = []
    for msg in messages:
        if msg["role"] == "system":
            langchain_messages.append(SystemMessage(content=msg["content"]))
        elif msg["role"] == "user":
            langchain_messages.append(HumanMessage(content=msg["content"]))
    
    # Add JSON formatting instruction to the last message
    json_instruction = f"""

Please respond with a valid JSON object that matches this schema:
{json.dumps(schema, indent=2)}

Ensure your response is valid JSON and follows the schema exactly.
"""
    
    if langchain_messages and isinstance(langchain_messages[-1], HumanMessage):
        langchain_messages[-1].content += json_instruction
    else:
        langchain_messages.append(HumanMessage(content=json_instruction))
    
    # Create the chain: LLM -> JSON Parser
    chain = llm | json_parser
    
    # Retry logic with schema validation
    for attempt in range(MAX_RETRIES):
        try:
            # Execute the chain
            result = chain.invoke(langchain_messages)
            
            # Validate against schema
            validate(instance=result, schema=schema)
            
            # Cache the successful result for deterministic queries
            if temperature == 0.0:
                _llm_cache[cache_key] = result
                print(f"[CACHE SET] Cached result for future use")
            
            return result  # ✅ valid output
            
        except (OutputParserException, json.JSONDecodeError, ValidationError) as e:
            print(f"[Retry {attempt+1}] Schema validation failed: {e}")
            if attempt == MAX_RETRIES - 1:
                raise ValueError(f"Failed to get valid response after {MAX_RETRIES} retries. Last error: {e}")
            continue
        except Exception as e:
            print(f"[Retry {attempt+1}] Unexpected error: {e}")
            if attempt == MAX_RETRIES - 1:
                raise ValueError(f"Failed to get valid response after {MAX_RETRIES} retries. Last error: {e}")
            continue
    
    raise ValueError("Failed to get valid response after retries.")
