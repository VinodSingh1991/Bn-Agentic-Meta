"""
Comprehensive Filtering Logic - Include all fields for matched entities
Returns complete field set for maximum LLM context
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class ComprehensiveFilter:
    """
    Applies comprehensive filtering - includes ALL fields for matched entities
    Provides complete context for maximum LLM capability
    """
    
    def __init__(self):
        pass
    
    def apply_filtering(self, context: Dict[str, Any], query_analysis: Dict[str, Any], nl_query: str) -> Dict[str, Any]:
        """
        Apply comprehensive filtering - include all fields for matched entities
        
        Args:
            context: Raw context with all fields and relevance scores
            query_analysis: Query analysis information (not used in comprehensive mode)
            nl_query: Original natural language query (not used in comprehensive mode)
            
        Returns:
            Complete context with all fields for matched entities
        """
        try:
            available_fields = context.get("available_fields", {})
            relevance_scores = context.get("relevance_scores", {})
            entities = context.get("entities", {})
            
            if not available_fields:
                return context
            
            # In comprehensive mode, we keep ALL fields for matched entities
            # No relevance threshold filtering
            # No intent-based filtering
            # No result count limiting
            
            comprehensive_fields = {}
            comprehensive_scores = {}
            
            # Include all fields that belong to matched entities
            for field_id, field_info in available_fields.items():
                field_object_id = field_info.get('object_id')
                field_object_name = field_info.get('object_name', '').lower()
                
                # Check if this field belongs to any matched entity
                entity_match = False
                for entity_id, entity_info in entities.items():
                    entity_object_id = entity_info.get('object_id')
                    entity_object_name = entity_info.get('object_name', '').lower()
                    
                    # Match by object_id or object_name
                    if (field_object_id == entity_object_id or 
                        field_object_name == entity_object_name):
                        entity_match = True
                        break
                
                if entity_match:
                    comprehensive_fields[field_id] = field_info
                    comprehensive_scores[field_id] = relevance_scores.get(field_id, 1.0)
            
            # Sort by object hierarchy and field name for consistent ordering
            sorted_fields = sorted(
                comprehensive_fields.items(),
                key=lambda x: (
                    x[1].get('object_name', ''),
                    x[1].get('field_name', '')
                )
            )
            
            final_fields = dict(sorted_fields)
            final_scores = {k: comprehensive_scores[k] for k in final_fields.keys()}
            
            context["available_fields"] = final_fields
            context["relevance_scores"] = final_scores
            context["filtering_applied"] = {
                "type": "comprehensive",
                "min_threshold": 0.0,
                "max_results": "unlimited",
                "original_count": len(available_fields),
                "filtered_count": len(final_fields)
            }
            
            return context
            
        except Exception as e:
            logger.error(f"Comprehensive filtering failed: {e}")
            return context
    
    def get_all_entity_fields(self, entity_manager, entity_object_ids: List[int]) -> Dict[str, Any]:
        """
        Get ALL fields for specified entities directly from entity manager
        
        Args:
            entity_manager: Enhanced entity manager instance
            entity_object_ids: List of object IDs to get all fields for
            
        Returns:
            Dictionary of all fields for the specified entities
        """
        try:
            all_fields = {}
            
            # Load full entities data if not already loaded
            if not hasattr(entity_manager, '_full_entities') or entity_manager._full_entities is None:
                import json
                with open(entity_manager.entities_file_path, 'r', encoding='utf-8') as f:
                    entity_manager._full_entities = json.load(f)
            
            # Get all fields for specified entities
            for item_id, item_data in entity_manager._full_entities.items():
                if (item_data.get('type') == 'field' and 
                    item_data.get('parentId') in entity_object_ids):
                    
                    field_info = {
                        'field_name': item_data.get('field_name'),
                        'object_name': item_data.get('object_name'),
                        'object_id': item_data.get('object_id'),
                        'data_type': item_data.get('data_type'),
                        'synonyms': item_data.get('field_synonyms', [])
                    }
                    
                    layout_field_id = item_data.get('layout_field_id', item_id)
                    all_fields[layout_field_id] = field_info
            
            return all_fields
            
        except Exception as e:
            logger.error(f"Failed to get all entity fields: {e}")
            return {}