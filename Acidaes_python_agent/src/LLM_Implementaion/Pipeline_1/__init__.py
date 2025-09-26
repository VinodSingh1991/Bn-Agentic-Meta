import json
from datetime import datetime
from src.utility.call_llm import call_llm

def prompt_to_intent_payload(user_prompt: str):
    """
    Convert user prompt to intent JSON using LLM
    
    Args:
        user_prompt: The user's natural language query
    
    Returns:
        dict: The intent JSON object
    """
    # Load intent schema
    with open("src/LLM_Implementaion/Pipeline_1/Schema/intentSchema.json", "r", encoding="utf-8") as f:
        intent_schema = json.load(f)

    # Load instructions
    with open("src/LLM_Implementaion/Pipeline_1/Instructions/intentInstructions.txt", "r", encoding="utf-8") as f:
        intent_instructions = f.read()
    
    # Add current date context
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_year = datetime.now().year
    current_month = datetime.now().month
    
    date_context = f"""
IMPORTANT DATE CONTEXT:
- Current Date: {current_date}
- Current Year: {current_year}
- Current Month: {current_month}

When processing date-related queries:
- "today" = {current_date}
- "this year" = {current_year}
- "this month" = {current_year}-{current_month:02d}
- "last month" = {current_year}-{current_month-1:02d} (or previous year if January)
- Always use {current_year} as the base year for date calculations
"""
    
    # Combine instructions with date context
    full_instructions = intent_instructions + "\n" + date_context

    intent_messages = [
        {"role": "system", "content": full_instructions},
        {"role": "user", "content": user_prompt}
    ]

    intent_json = call_llm(intent_messages, intent_schema)

    return intent_json
