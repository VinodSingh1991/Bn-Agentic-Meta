from typing import List, Dict, Any
from files_handler.file_loader import FileLoader


class ObjectManager:
    """Manages loading and validation of objects"""
    
    def __init__(self, file_loader: FileLoader):
        self.loader = file_loader
    
    def load_objects(self, filename: str = "objects.json") -> List[Dict[str, Any]]:
        """Load objects from file with error handling"""
        try:
            objects = self.loader.loadJsonFile(filename)
            if not objects:
                print(f"No objects found in {filename}")
                return []
            
            # Validate objects
            valid_objects = []
            for obj in objects:
                if self._validate_object(obj):
                    valid_objects.append(obj)
                else:
                    print(f"Skipping invalid object: {obj}")
            
            print(f"Loaded {len(valid_objects)} valid objects from {filename}")
            return valid_objects
            
        except Exception as e:
            print(f"Error loading objects from {filename}: {e}")
            return []
    
    def _validate_object(self, obj: Dict[str, Any]) -> bool:
        """Validate that object has required fields"""
        if not isinstance(obj, dict):
            return False
        
        object_name = obj.get("ObjectName", "")
        if not object_name or not isinstance(object_name, str):
            return False
            
        return True
    
    def get_object_names(self, objects: List[Dict[str, Any]]) -> List[str]:
        """Extract object names from objects list"""
        return [obj.get("ObjectName", "") for obj in objects if obj.get("ObjectName")]


class QuerySaver:
    """Handles saving queries to files"""
    
    def __init__(self, file_loader: FileLoader):
        self.loader = file_loader
    
    def save_queries(self, queries: List[Any], filename: str = "queries.json") -> bool:
        """Save queries to file with error handling"""
        try:
            self.loader.save_files_for_rag(filename, queries)
            print(f"Successfully saved {len(queries)} queries to {filename}")
            return True
        except Exception as e:
            print(f"Error saving queries to {filename}: {e}")
            return False
    
    def save_simple_queries(self, queries: List[str], filename: str = "simple_queries.json") -> bool:
        """Save simple string queries"""
        return self.save_queries(queries, filename)
    
    def save_structured_queries(self, queries: List[Dict[str, Any]], filename: str = "structured_queries.json") -> bool:
        """Save structured queries with metadata"""
        return self.save_queries(queries, filename)


class QueryValidator:
    """Validates and filters queries"""
    
    @staticmethod
    def validate_simple_query(query: str) -> bool:
        """Validate a simple string query"""
        return isinstance(query, str) and len(query.strip()) > 0
    
    @staticmethod
    def validate_structured_query(query: Dict[str, Any]) -> bool:
        """Validate a structured query"""
        if not isinstance(query, dict):
            return False
        
        # Check required fields
        if "query" not in query or "meta_data" not in query:
            return False
        
        # Validate query field
        if not isinstance(query["query"], str) or len(query["query"].strip()) == 0:
            return False
        
        # Validate meta_data field
        if not isinstance(query["meta_data"], dict):
            return False
        
        return True
    
    @staticmethod
    def filter_valid_queries(queries: List[Any]) -> List[Any]:
        """Filter out invalid queries from a list"""
        valid_queries = []
        
        for query in queries:
            if isinstance(query, str):
                if QueryValidator.validate_simple_query(query):
                    valid_queries.append(query)
            elif isinstance(query, dict):
                if QueryValidator.validate_structured_query(query):
                    valid_queries.append(query)
        
        return valid_queries


class QueryStatistics:
    """Provides statistics about generated queries"""
    
    @staticmethod
    def get_query_stats(queries: List[Any]) -> Dict[str, Any]:
        """Get statistics about queries"""
        stats = {
            "total_queries": len(queries),
            "simple_queries": 0,
            "structured_queries": 0,
            "unique_objects": set(),
            "query_types": {}
        }
        
        for query in queries:
            if isinstance(query, str):
                stats["simple_queries"] += 1
            elif isinstance(query, dict):
                stats["structured_queries"] += 1
                
                # Extract object information from metadata
                meta_data = query.get("meta_data", {})
                if "primary_object" in meta_data:
                    stats["unique_objects"].add(meta_data["primary_object"])
                
                # Count query types
                query_type = meta_data.get("type", "unknown")
                stats["query_types"][query_type] = stats["query_types"].get(query_type, 0) + 1
        
        stats["unique_objects"] = len(stats["unique_objects"])
        return stats
    
    @staticmethod
    def print_stats(queries: List[Any]):
        """Print query statistics"""
        stats = QueryStatistics.get_query_stats(queries)
        
        print(f"\n=== Query Generation Statistics ===")
        print(f"Total queries generated: {stats['total_queries']}")
        print(f"Simple queries: {stats['simple_queries']}")
        print(f"Structured queries: {stats['structured_queries']}")
        print(f"Unique objects processed: {stats['unique_objects']}")
        
        if stats['query_types']:
            print(f"Query types:")
            for query_type, count in stats['query_types'].items():
                print(f"  - {query_type}: {count}")
        
        print("=" * 40)