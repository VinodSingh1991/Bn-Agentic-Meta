from files_handler.file_loader import FileLoader
from RAG.get_query_pattern_by_object import get_base_patterns, in_patterns, related_base_patterns, get_summary_pattern_dict, related_base_patterns_dict_structured, in_patterns_dict


class RagCreator:
    def __init__(self):
        self.loader = FileLoader()

    def get_objects(self):
        try:
            # Fetch all required data
            objects = self.loader.loadJsonFile("objects.json")
            return objects
        except Exception as e:
            print(f"Error getting Object files: {e}")

    def build_pattern1(self):
        objects = self.get_objects()
        list_of_queries = []

        for obj in objects:
            object_name = obj.get("ObjectName", "")
            
            # Process base patterns for current object
            for pattern in get_base_patterns:
                base_query = pattern.replace("{ObjectPlural}", object_name + "s")
                base_query = base_query.replace("{Object}", object_name)
                list_of_queries.append(base_query)
                
                # Add extended queries with in_patterns
                for in_pattern in in_patterns:
                    extended_query = f"{base_query} {in_pattern}"
                    list_of_queries.append(extended_query)

            # Process related patterns for current object with all other objects
            for related_pattern in related_base_patterns:
                for rel_obj in objects:
                    related_object_name = rel_obj.get("ObjectName", "")
                    if related_object_name == object_name:
                        continue  # Skip if both objects are the same
                    
                    related_query = related_pattern.replace("{ObjectPlural}", object_name + "s")
                    related_query = related_query.replace("{RelatedObject}", related_object_name)
                    list_of_queries.append(related_query)
                    
                    # Add extended related queries with in_patterns
                    for in_pattern in in_patterns:
                        extended_related_query = f"{related_query} {in_pattern}"
                        list_of_queries.append(extended_related_query)

        self.loader.save_files_for_rag("queries.json", list_of_queries)

        return list_of_queries
    
    def build_pattern(self):
        try:
            objects = self.get_objects()
            if not objects:
                print("No objects found to process")
                return []
                
            list_of_queries = []

            for obj in objects:
                object_name = obj.get("ObjectName", "")
                if not object_name:
                    print(f"Skipping object with empty ObjectName: {obj}")
                    continue
                
                # Process base patterns for current object
                for pattern_key, pattern_value in get_summary_pattern_dict.items():
                    base_query = pattern_key.replace("{ObjectPlural}", object_name + "s")
                    base_query = base_query.replace("{Object}", object_name)

                    base_metadata = pattern_value.copy()
                    base_metadata["primary_object"] = object_name
                    list_of_queries.append({
                        "query": base_query,
                        "meta_data": base_metadata
                    })
                    
                    # Add extended queries with in_patterns
                    for in_key, in_pattern in in_patterns_dict.items():
                        extended_query = f"{base_query} {in_key}"
                        extended_metadata = base_metadata.copy()
                        extended_metadata["output_format"] = in_pattern
                        list_of_queries.append({
                            "query": extended_query,
                            "meta_data": extended_metadata
                        })

                # Process related patterns for current object with all other objects
                for related_pattern_key, related_pattern_value in related_base_patterns_dict_structured.items():
                    for rel_obj in objects:
                        related_object_name = rel_obj.get("ObjectName", "")
                        if not related_object_name or related_object_name == object_name:
                            continue  # Skip if related object name is empty or same as current object
                        
                        related_query = related_pattern_key.replace("{ObjectPlural}", object_name + "s")
                        related_query = related_query.replace("{RelatedObject}", related_object_name)
                        
                        related_metadata = related_pattern_value.copy()
                        related_metadata["primary_object"] = object_name
                        related_metadata["related_objects"] = related_object_name
                        list_of_queries.append({
                            "query": related_query,
                            "meta_data": related_metadata
                        })

                        # Add extended related queries with in_patterns
                        for in_key, in_pattern in in_patterns_dict.items():
                            extended_related_query = f"{related_query} {in_key}"
                            extended_related_metadata = related_metadata.copy()
                            extended_related_metadata["output_format"] = in_pattern
                            list_of_queries.append({
                                "query": extended_related_query,
                                "meta_data": extended_related_metadata
                            })

            # Save the generated queries
            try:
                self.loader.save_files_for_rag("queries.json", list_of_queries)
                print(f"Successfully generated and saved {len(list_of_queries)} queries")
            except Exception as save_error:
                print(f"Error saving queries to file: {save_error}")
            
            return list_of_queries
            
        except Exception as e:
            print(f"Error in build_pattern: {e}")
            return []
