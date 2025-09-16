from typing import List, Any
import re
from src.utility.nlp_dict.stop_words import stop_words

def extract_label_from_field(fields_data):
    # Handles dict, list, and nested responseData/data structures
    result = []
    values = []
    if isinstance(fields_data, dict):
        # Check for nested responseData/data
        if "responseData" in fields_data:
            data = fields_data["responseData"]
            if isinstance(data, dict) and "data" in data:
                values = data["data"]
            elif isinstance(data, list):
                values = data
            else:
                values = []
        elif "data" in fields_data:
            values = fields_data["data"]
        else:
            values = list(fields_data.values())
    elif isinstance(fields_data, list):
        values = fields_data
    # Now extract fieldname and fieldLabel
    for field in values:
        if "metaData" in field and isinstance(field["metaData"], dict):
            field = field["metaData"]
        if isinstance(field, dict):
            label = field.get("fieldLabel")
            if label is not None:
                result.append({"fieldLabel": label})
    return result


def get_data_from_response_data(response_data) -> List[Any]:
    """
    Extracts the data list from a response_data object or dict.
    Handles both Pydantic model and dict input.
    """
    if hasattr(response_data, 'responseData'):
        # Pydantic model
        data = response_data.responseData.data
    elif isinstance(response_data, dict):
        if 'responseData' in response_data and 'data' in response_data['responseData']:
            data = response_data['responseData']['data']
        else:
            data = []
    else:
        data = []
    return data

def split_camel_case(word: str):
    """Split camelCase or PascalCase into separate words."""
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', word).split()

def generate_words(text: str):
    # Always convert input to string if it's not already
    if isinstance(text, list):
        text = " ".join(str(item) for item in text)
    elif not isinstance(text, str):
        text = str(text)

    # Step 1: remove prefix before first underscore
    if "_" in text:
        text = text.split("_", 1)[-1]  # keep after first "_"

    # Step 2: split by non-alphanumeric
    parts = re.split(r'[^a-zA-Z0-9]', text)
    parts = [p for p in parts if p]

    results = set()

    for part in parts:
        # Add raw part
        results.add(part)

        # Add camelCase splits
        camel_parts = split_camel_case(part)
        if len(camel_parts) > 1:
            results.update(camel_parts)
            results.add(" ".join(camel_parts))

    # Step 3: add combined phrases
    if len(parts) > 1:
        for i in range(len(parts)):
            for j in range(i+1, len(parts)+1):
                phrase = " ".join(parts[i:j])
                results.add(phrase)

    filtered_words = [word for word in results if word.lower() not in stop_words]

    return filtered_words

def process_array(strings: list[str]):
    final_results = set()
    for s in strings:
        final_results.update(generate_words(s))
    return sorted(final_results)