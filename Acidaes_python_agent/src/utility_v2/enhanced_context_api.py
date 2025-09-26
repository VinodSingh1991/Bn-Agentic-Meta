"""
Enhanced Context API with improved precision and accuracy
Core functionality for context generation
"""

import json
import logging
import sys
import os
from typing import Dict, List, Optional, Any

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utility_v2.enhanced_entity_manager import EnhancedSmartEntityManager
from utility_v2.filtering_selective import SelectiveFilter
from utility_v2.filtering_comprehensive import ComprehensiveFilter

logger = logging.getLogger(__name__)

class EnhancedContextAPI:
    """
    Enhanced context API with improved precision and accuracy
    Focuses on returning exactly the needed data for user queries
    """
    
    def __init__(self, entities_file_path: str = "./src/utility_v2/entities.json", filtering_mode: str = "selective"):
        self.entity_manager = EnhancedSmartEntityManager(entities_file_path)
        
        # FILTERING MODE SWITCH - Change between selective/comprehensive
        # Options: "selective" (relevance-based filtering) or "comprehensive" (all fields)
        # This switch allows testing both approaches for performance comparison
        self.FILTERING_MODE = filtering_mode  # Default: selective filtering
        
        # Initialize filtering strategies
        self.selective_filter = SelectiveFilter()
        self.comprehensive_filter = ComprehensiveFilter()
        
    def get_query_specific_context(self, nl_query: str) -> Dict[str, Any]:
        """
        Get enhanced query-specific context with entities.json-like structure
        
        Args:
            nl_query: Natural language query
        
        Returns:
            Context dictionary with entities.json structure (flat with entity/field keys)
        """
        try:
            # Get enhanced context from entity manager
            raw_context = self.entity_manager.get_context_for_query_enhanced(nl_query)
            
            # Apply filtering based on FILTERING_MODE switch
            if self.FILTERING_MODE == "selective":
                query_analysis = self._analyze_query(nl_query)
                filtered_context = self.selective_filter.apply_filtering(raw_context, query_analysis, nl_query)
            elif self.FILTERING_MODE == "comprehensive":
                query_analysis = self._analyze_query(nl_query)
                filtered_context = self.comprehensive_filter.apply_filtering(raw_context, query_analysis, nl_query)
            else:
                # Fallback to selective if invalid mode
                query_analysis = self._analyze_query(nl_query)
                filtered_context = self.selective_filter.apply_filtering(raw_context, query_analysis, nl_query)
            
            # Transform to entities.json-like structure
            entities_json_structure = self._transform_to_entities_structure(
                filtered_context, 
                nl_query
            )
            
            return entities_json_structure
            
        except Exception as e:
            logger.error(f"Failed to get query-specific context: {e}")
            return self._get_fallback_context(nl_query)
    
    def _transform_to_entities_structure(self, context: Dict[str, Any], nl_query: str) -> Dict[str, Any]:
        """
        Transform context to match entities.json structure with new key format
        
        Args:
            context: Filtered context from entity manager
            nl_query: Original query for metadata
            
        Returns:
            Dictionary with entities and available_fields structure
        """
        entities = {}
        available_fields = {}
        
        try:
            input_available_fields = context.get("available_fields", {})
            input_entities = context.get("entities", {})
            
            # Process entities - keep them in entities section with readable names
            for entity_key, entity_info in input_entities.items():
                object_id = entity_info.get("object_id")
                object_name = entity_info.get("object_name", "Unknown")
                
                entities[object_name] = {
                    "object_id": object_id,
                    "object_name": object_name,
                    "object_synonyms": entity_info.get("synonyms", []),
                    "fields": []  # Will be populated with field names
                }
            
            # Process fields - put them in available_fields with layout_field_id as key
            for field_key, field_info in input_available_fields.items():
                object_id = field_info.get("object_id")
                object_name = field_info.get("object_name", "Unknown")
                field_name = field_info.get("field_name", "Unknown")
                
                # Get field mappings to find proper field_id and layout_field_id
                field_mappings = context.get("field_mappings", {})
                
                # Find the proper field_id from mappings or use field_key
                layout_field_id = field_key  # Default to field_key
                
                # Search for the field in mappings
                for mapping_key, mapping_value in field_mappings.items():
                    if mapping_key == field_key or mapping_value == field_name:
                        layout_field_id = mapping_key
                        break
                
                # Load entities to find proper field_id
                field_id = self._find_field_id_in_entities(field_name, object_id)
                if not field_id:
                    field_id = field_key  # Fallback
                
                available_fields[layout_field_id] = {
                    "parentId": object_id,
                    "parentName": object_name,
                    "field_id": field_id,
                    "field_name": field_name,
                    "fieldLabel": self._generate_field_label(field_name, object_name),
                    "layout_field_id": layout_field_id,
                    "field_synonyms": field_info.get("synonyms", [])
                }
                
                # Add field to parent entity's field list
                if object_name in entities:
                    entities[object_name]["fields"].append(layout_field_id)
                
        except Exception as e:
            logger.error(f"Failed to transform to entities structure: {e}")
        
        return {
            "entities": entities,
            "available_fields": available_fields,
            "field_mappings": context.get("field_mappings", {}),
            "query": nl_query,
            "timestamp": self._get_timestamp()
        }
    
    def _find_field_id_in_entities(self, field_name: str, object_id: int) -> Optional[str]:
        """Find the proper field_id from entities.json"""
        try:
            with open(self.entity_manager.entities_file_path, 'r', encoding='utf-8') as f:
                entities_data = json.load(f)
            
            for item_id, item_data in entities_data.items():
                if (item_data.get('type') == 'field' and
                    item_data.get('field_name') == field_name and
                    item_data.get('object_id') == object_id):
                    return item_data.get('field_id', item_id)
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to find field_id: {e}")
            return None
    
    def _generate_field_label(self, field_name: str, object_name: str) -> str:
        """Generate a field label in standard format"""
        return f"SN_{object_name.upper()}_{field_name.upper()}"
    
    def _analyze_query(self, nl_query: str) -> Dict[str, Any]:
        """Analyze the query to understand intent and requirements"""
        analysis = {
            "query_length": len(nl_query),
            "word_count": len(nl_query.split()),
            "query_type": self._detect_query_type(nl_query),
            "intent": self._detect_intent(nl_query),
            "scope": self._detect_scope(nl_query),
            "specificity": self._calculate_specificity(nl_query)
        }
        
        return analysis
    
    def _detect_query_type(self, query: str) -> str:
        """Unbiased query type detection using statistical approach"""
        query_lower = query.lower()
        query_words = query_lower.split()
        
        # Statistical approach - count patterns, not specific words
        action_patterns = {
            "retrieval": ["show", "display", "list", "get", "retrieve", "view", "provide"],
            "filter": ["filter", "where", "with", "having", "only", "specific", "matching"],
            "aggregation": ["count", "sum", "total", "average", "calculate", "measure"],
            "search": ["find", "search", "look", "locate", "seek", "identify"]
        }
        
        # Score each pattern type
        pattern_scores = {}
        for pattern_type, words in action_patterns.items():
            score = sum(1 for word in query_words if word in words)
            pattern_scores[pattern_type] = score
        
        # Return highest scoring pattern, or general if no clear pattern
        max_score = max(pattern_scores.values()) if pattern_scores.values() else 0
        if max_score == 0:
            return "general"
        
        return max(pattern_scores.items(), key=lambda x: x[1])[0]
    
    def _detect_intent(self, query: str) -> str:
        """Enhanced intent detection with better precision"""
        query_lower = query.lower()
        
        # Enhanced communication detection
        if any(word in query_lower for word in ["communication", "history", "emails", "calls", "meetings"]):
            return "communication_history"
        elif any(word in query_lower for word in ["contact", "email", "phone"]):
            return "contact_information"
        elif any(word in query_lower for word in ["name", "title", "who"]):
            return "identification"
        elif any(word in query_lower for word in ["status", "stage", "condition"]):
            return "status_inquiry"
        elif any(word in query_lower for word in ["address", "location", "where"]):
            return "location_inquiry"
        elif any(word in query_lower for word in ["revenue", "amount", "value", "financial"]):
            return "financial_data"
        elif any(word in query_lower for word in ["date", "time", "when"]):
            return "temporal_data"
        elif any(word in query_lower for word in ["lead", "conversion", "source", "tracking"]):
            return "lead_management"
        elif any(word in query_lower for word in ["forecast", "prediction", "pipeline"]):
            return "sales_forecasting"
        else:
            return "general_information"
    
    def _detect_scope(self, query: str) -> str:
        """Detect the scope of the query (single field, multiple fields, all fields)"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["all", "every", "complete"]):
            return "comprehensive"
        elif len(query.split()) <= 3:
            return "specific"
        else:
            return "moderate"
    
    def _calculate_specificity(self, query: str) -> float:
        """Calculate how specific the query is (0.0 to 1.0) using unbiased metrics"""
        query_lower = query.lower()
        query_words = query_lower.split()
        
        # Base specificity score
        specificity_score = 0.5
        
        # Statistical approach based on query characteristics
        word_count = len(query_words)
        unique_words = len(set(query_words))
        
        # Longer queries with more unique words tend to be more specific
        length_factor = min(word_count / 10.0, 0.3)  # Cap at 0.3
        uniqueness_factor = (unique_words / word_count) * 0.2 if word_count > 0 else 0
        
        specificity_score += length_factor + uniqueness_factor
        
        # Penalize very generic words (common English words)
        generic_words = {"the", "and", "or", "a", "an", "is", "are", "with", "for", "to"}
        generic_ratio = sum(1 for word in query_words if word in generic_words) / len(query_words)
        specificity_score -= generic_ratio * 0.1
        
        return max(0.0, min(1.0, specificity_score))
    
    def _get_fallback_context(self, query: str) -> Dict[str, Any]:
        """Get a basic fallback context when enhanced processing fails"""
        return {
            "error": "Failed to generate enhanced context",
            "fallback_mode": True,
            "query": query,
            "generated_at": self._get_timestamp()
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()