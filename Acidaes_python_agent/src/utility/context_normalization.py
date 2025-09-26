from src.utility.query_normalization import QueryNormalization
import re
from src.utility.meta_data import MetaDataUtility

class ContextNormalization:
    def __init__(self, query: str):
        self.meta_data_utility = MetaDataUtility()
        self.query_normalizer = QueryNormalization()
        self.original_query = query
        self.query = query
        self.context = {}

    # get normalized words from query
    def get_normalized_query(self):
        self.query = self.query_normalizer.normalize_query(self.query)
        print(f"Normalized words: {self.query}")
        return self.query

    def get_split_words(self):
        query = self.get_normalized_query()
        query = re.sub(r"[^a-z0-9\s]", "", query)  # remove punctuation
        return query.split()

    def match_query(self):
        split_words = self.get_split_words()
        # Implement your matching logic here
        print(f"Matching query: {split_words}")
        return split_words

    def get_inverted_indexs(self):
        inverted_index_response = self.meta_data_utility.get_fields_from_db(
            "invertedIndex.json"
        )
        return inverted_index_response

    def get_entity_context(self):
        entity_response = self.meta_data_utility.get_fields_from_db("entities.json")
        return entity_response

    def get_inverted_context(self):
        inverted_index = self.get_inverted_indexs()
        matched_words = self.match_query()
        context = {}
        for word in matched_words:
            for key, value in inverted_index.items():
                if word == key:
                    context[value] = key
        self.context = context
        return self.context

    def get_field_from_object(self, object_id: str, entity_context):
        # Safely get layout_fields, defaulting to an empty list if not found
        if object_id not in entity_context:
            return {}
            
        layout_fields = entity_context[object_id].get("layouts_fields", [])
        if not layout_fields:
            return {}
            
        object_data = {}
        # Iterate through all entities to find fields with matching layout_field_id
        for entity_key, entity_data in entity_context.items():
            # Check if this is a field entity
            if entity_data.get("type") == "field":
                # Check if the field's layout_field_id matches any in our layout_fields list
                field_layout_id = entity_data.get("layout_field_id")
                if field_layout_id and field_layout_id in layout_fields:
                    object_data[entity_key] = entity_data
        return object_data

    def get_entity_contexts(self, entity_dict):
        if not entity_dict:
            return []
        
        entity_new_context = []
        entity_context = self.get_entity_context()
        
        for key, value in entity_dict.items():
            # Convert key to string if it's not already
            key_str = str(key)
            
            if key_str in entity_context:
                entity = entity_context[key_str]
                
                typ = entity.get("type", "")
                if typ == "object":
                    entities_fields = self.get_field_from_object(key_str, entity_context)
                    # Only append once with merged data
                    entity_new_context.append({**entity, **entities_fields})
                else:
                    # Only append non-object entities here
                    entity_new_context.append(entity)

        return entity_new_context

    def get_context(self):
        # Implement context extraction logic here
        normalized_query = self.get_normalized_query()
        matched_words = self.match_query()
        matched_context = self.get_inverted_context()
        context = self.get_entity_contexts(matched_context)

        return {
            "original_query": self.original_query,
            "normalized_query": normalized_query,
            "matched_context": matched_context,
            "matched_words": matched_words,
            "context": context,
        }
