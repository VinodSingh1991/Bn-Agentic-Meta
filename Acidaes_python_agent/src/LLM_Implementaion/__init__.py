from src.LLM_Implementaion.Pipeline_1 import prompt_to_intent_payload
from src.LLM_Implementaion.Pipeline_2 import intent_json_to_payload

def llm_implementation(user_prompt: str):
    """
    Complete LLM implementation pipeline
    
    Args:
        user_prompt: The user's natural language query
    
    Returns:
        dict: Complete pipeline result with intent and payload
    """
    # Pipeline 1: Convert user prompt to intent JSON
    intent_json = prompt_to_intent_payload(user_prompt)
    # print("Pipeline 1 - Intent JSON:", intent_json)

    # Pipeline 2: Convert intent JSON to query payload (with context from nl_query)
    payload_json = intent_json_to_payload(intent_json, nl_query=user_prompt)
    # print("Pipeline 2 - Payload JSON:", payload_json)
    
    return {
        "intent": intent_json,
        "payload": payload_json,
        "original_query": user_prompt
    }