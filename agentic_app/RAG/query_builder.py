from typing import List, Dict, Any
from abc import ABC, abstractmethod


class BaseQueryBuilder(ABC):
    """Abstract base class for query builders"""
    
    def __init__(self):
        pass
    
    @abstractmethod
    def build_queries(self, objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Build queries for given objects"""
        pass
    
    def _validate_object_name(self, obj: Dict[str, Any]) -> str:
        """Validate and return object name"""
        object_name = obj.get("ObjectName", "")
        if not object_name:
            raise ValueError(f"Object has empty ObjectName: {obj}")
        return object_name
    
    def _replace_placeholders(self, pattern: str, object_name: str, related_object_name: str = None) -> str:
        """Replace placeholders in pattern with actual values"""
        query = pattern.replace("{ObjectPlural}", object_name + "s")
        query = query.replace("{Object}", object_name)
        if related_object_name:
            query = query.replace("{RelatedObject}", related_object_name)
        return query


class SimpleQueryBuilder(BaseQueryBuilder):
    """Builder for simple string-based queries"""
    
    def __init__(self, base_patterns: List[str], in_patterns: List[str]):
        super().__init__()
        self.base_patterns = base_patterns
        self.in_patterns = in_patterns
    
    def build_queries(self, objects: List[Dict[str, Any]]) -> List[str]:
        """Build simple string queries"""
        queries = []
        
        for obj in objects:
            try:
                object_name = self._validate_object_name(obj)
                
                # Process base patterns
                for pattern in self.base_patterns:
                    base_query = self._replace_placeholders(pattern, object_name)
                    queries.append(base_query)
                    
                    # Add extended queries with in_patterns
                    for in_pattern in self.in_patterns:
                        extended_query = f"{base_query} {in_pattern}"
                        queries.append(extended_query)
                        
            except ValueError as e:
                print(f"Skipping invalid object: {e}")
                continue
                
        return queries


class StructuredQueryBuilder(BaseQueryBuilder):
    """Builder for structured queries with metadata"""
    
    def __init__(self, pattern_dict: Dict[str, Dict], in_patterns_dict: Dict[str, Dict]):
        super().__init__()
        self.pattern_dict = pattern_dict
        self.in_patterns_dict = in_patterns_dict
    
    def build_queries(self, objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Build structured queries with metadata"""
        queries = []
        
        for obj in objects:
            try:
                object_name = self._validate_object_name(obj)
                
                # Process base patterns
                for pattern_key, pattern_value in self.pattern_dict.items():
                    base_query = self._replace_placeholders(pattern_key, object_name)
                    
                    base_metadata = pattern_value.copy()
                    base_metadata["primary_object"] = object_name
                    
                    queries.append({
                        "query": base_query,
                        "meta_data": base_metadata
                    })
                    
                    # Add extended queries with in_patterns
                    for in_key, in_pattern in self.in_patterns_dict.items():
                        extended_query = f"{base_query} {in_key}"
                        extended_metadata = base_metadata.copy()
                        extended_metadata["output_format"] = in_pattern
                        
                        queries.append({
                            "query": extended_query,
                            "meta_data": extended_metadata
                        })
                        
            except ValueError as e:
                print(f"Skipping invalid object: {e}")
                continue
                
        return queries


class RelatedQueryBuilder(BaseQueryBuilder):
    """Builder for queries involving related objects"""
    
    def __init__(self, related_patterns: List[str], in_patterns: List[str]):
        super().__init__()
        self.related_patterns = related_patterns
        self.in_patterns = in_patterns
    
    def build_queries(self, objects: List[Dict[str, Any]]) -> List[str]:
        """Build queries for related objects"""
        queries = []
        
        for obj in objects:
            try:
                object_name = self._validate_object_name(obj)
                
                # Process related patterns with all other objects
                for related_pattern in self.related_patterns:
                    for rel_obj in objects:
                        try:
                            related_object_name = self._validate_object_name(rel_obj)
                            if related_object_name == object_name:
                                continue  # Skip if both objects are the same
                                
                            related_query = self._replace_placeholders(
                                related_pattern, object_name, related_object_name
                            )
                            queries.append(related_query)
                            
                            # Add extended related queries with in_patterns
                            for in_pattern in self.in_patterns:
                                extended_related_query = f"{related_query} {in_pattern}"
                                queries.append(extended_related_query)
                                
                        except ValueError:
                            continue  # Skip invalid related objects
                            
            except ValueError as e:
                print(f"Skipping invalid object: {e}")
                continue
                
        return queries


class StructuredRelatedQueryBuilder(BaseQueryBuilder):
    """Builder for structured queries involving related objects"""
    
    def __init__(self, related_patterns_dict: Dict[str, Dict], in_patterns_dict: Dict[str, Dict]):
        super().__init__()
        self.related_patterns_dict = related_patterns_dict
        self.in_patterns_dict = in_patterns_dict
    
    def build_queries(self, objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Build structured queries for related objects"""
        queries = []
        
        for obj in objects:
            try:
                object_name = self._validate_object_name(obj)
                
                # Process related patterns with all other objects
                for related_pattern_key, related_pattern_value in self.related_patterns_dict.items():
                    for rel_obj in objects:
                        try:
                            related_object_name = self._validate_object_name(rel_obj)
                            if related_object_name == object_name:
                                continue  # Skip if both objects are the same
                                
                            related_query = self._replace_placeholders(
                                related_pattern_key, object_name, related_object_name
                            )
                            
                            related_metadata = related_pattern_value.copy()
                            related_metadata["primary_object"] = object_name
                            related_metadata["related_objects"] = related_object_name
                            
                            queries.append({
                                "query": related_query,
                                "meta_data": related_metadata
                            })
                            
                            # Add extended related queries with in_patterns
                            for in_key, in_pattern in self.in_patterns_dict.items():
                                extended_related_query = f"{related_query} {in_key}"
                                extended_related_metadata = related_metadata.copy()
                                extended_related_metadata["output_format"] = in_pattern
                                
                                queries.append({
                                    "query": extended_related_query,
                                    "meta_data": extended_related_metadata
                                })
                                
                        except ValueError:
                            continue  # Skip invalid related objects
                            
            except ValueError as e:
                print(f"Skipping invalid object: {e}")
                continue
                
        return queries