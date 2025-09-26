import json
import requests
from src.utility.call_llm import call_llm

def intent_json_to_payload(intent_json: dict, nl_query: str = ""):
    """
    Convert intent JSON to query payload using LLM with context from get_entities_context
    
    Args:
        intent_json: The intent JSON from Pipeline_1
        nl_query: Original natural language query to get context for
    
    Returns:
        dict: The generated query payload
    """
    # Get context data from the API endpoint
    context_data = ""
    if nl_query:
        try:
            # Call the get_entities_context endpoint
            response = requests.get(f"http://localhost:8000/api/get_context?nl_query={nl_query}")
            if response.status_code == 200:
                context_response = response.json()
                context_data = json.dumps(context_response.get("context", {}), indent=2)
            else:
                print(f"Warning: Failed to get context data. Status code: {response.status_code}")
                context_data = "{}"
        except Exception as e:
            print(f"Warning: Failed to call get_entities_context: {e}")
            context_data = "{}"
    
    # Load payload schema
    with open("src/LLM_Implementaion/Pipeline_2/Schema/payLoadSchema.json", "r", encoding="utf-8") as f:
        payload_schema = json.load(f)

    # Load instructions
    with open("src/LLM_Implementaion/Pipeline_2/Instructions/payLoadInstructions_FINAL.txt", "r", encoding="utf-8") as f:
        payload_instructions = f.read()

    # Prepare the user message with intent JSON and context
    user_content = f"""Transform the following intent into a query payload using the provided context.

INTENT JSON:
{json.dumps(intent_json, indent=2)}

AVAILABLE ENTITIES CONTEXT:
{context_data}

TASK: Generate a comprehensive query payload that:
1. Validates all entities and fields against the provided context
2. Transforms the intent into the required payloadSchema format
3. Applies all transformation rules from the instructions
4. Do not invent or hallucinate any fields or entities not present in the context

Generate the query payload now."""

    payload_messages = [
        {"role": "system", "content": payload_instructions},
        {"role": "user", "content": user_content}
    ]

    payload_json = call_llm(payload_messages, payload_schema)

    return payload_json