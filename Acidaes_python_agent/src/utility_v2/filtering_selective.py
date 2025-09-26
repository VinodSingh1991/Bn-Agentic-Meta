"""
Selective Filtering Logic - Relevance-based field filtering
Returns only highly relevant fields based on semantic scoring
"""

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class SelectiveFilter:
    """
    Applies selective filtering based on relevance scores
    Returns filtered subset of fields for cleaner LLM input
    """
    
    def __init__(self):
        self.min_relevance_threshold = 0.5
        self.max_results = 80
    
    def apply_filtering(self, context: Dict[str, Any], query_analysis: Dict[str, Any], nl_query: str) -> Dict[str, Any]:
        """
        Apply selective filtering based on relevance scores and query characteristics
        
        Args:
            context: Raw context with all fields and relevance scores
            query_analysis: Query analysis information
            nl_query: Original natural language query
            
        Returns:
            Filtered context with high-relevance fields only
        """
        try:
            available_fields = context.get("available_fields", {})
            relevance_scores = context.get("relevance_scores", {})
            
            if not available_fields:
                return context
            
            # Get query characteristics for adaptive filtering
            query_type = query_analysis.get("query_type", "general")
            intent = query_analysis.get("intent", "general_information")
            specificity = query_analysis.get("specificity", 0.5)
            
            # Apply different filtering strategies based on query type
            if query_type == "specific_retrieval":
                min_threshold = 0.7
                max_results = 50
            elif query_type == "comprehensive_retrieval":
                min_threshold = 0.4
                max_results = 100
            elif query_type == "targeted_search":
                min_threshold = 0.6
                max_results = 75
            else:
                min_threshold = self.min_relevance_threshold
                max_results = self.max_results
            
            # Apply relevance threshold filtering
            filtered_fields = {}
            filtered_scores = {}
            
            for field_id, field_info in available_fields.items():
                relevance = relevance_scores.get(field_id, 0.0)
                
                # Basic relevance filter
                if relevance >= min_threshold:
                    # Additional intent-based filtering
                    if self._passes_intent_filter(field_info, intent, nl_query):
                        filtered_fields[field_id] = field_info
                        filtered_scores[field_id] = relevance
            
            # Sort by relevance and limit results
            sorted_fields = sorted(
                filtered_fields.items(),
                key=lambda x: filtered_scores.get(x[0], 0.0),
                reverse=True
            )[:max_results]
            
            # Rebuild context with filtered results
            final_fields = dict(sorted_fields)
            final_scores = {k: filtered_scores[k] for k in final_fields.keys()}
            
            context["available_fields"] = final_fields
            context["relevance_scores"] = final_scores
            context["filtering_applied"] = {
                "type": "selective",
                "min_threshold": min_threshold,
                "max_results": max_results,
                "original_count": len(available_fields),
                "filtered_count": len(final_fields)
            }
            
            return context
            
        except Exception as e:
            logger.error(f"Selective filtering failed: {e}")
            return context
    
    def _passes_intent_filter(self, field_info: Dict[str, Any], intent: str, query: str) -> bool:
        """Check if field passes intent-specific filtering"""
        
        field_text = (
            field_info.get('field_name', '') + ' ' +
            field_info.get('object_name', '') + ' ' +
            ' '.join(field_info.get('synonyms', []))
        ).lower()
        
        # Intent-specific keyword matching
        intent_keywords = {
            "contact_information": ["contact", "email", "phone", "address", "communication"],
            "identification": ["name", "title", "id", "identifier"],
            "status_inquiry": ["status", "stage", "state", "condition"],
            "location_inquiry": ["address", "location", "territory", "region"],
            "financial_data": ["revenue", "amount", "price", "cost", "financial", "money"],
            "temporal_data": ["date", "time", "created", "modified", "due", "start", "end"],
            "communication_history": ["activity", "communication", "email", "call", "meeting", "history"],
            "lead_management": ["lead", "source", "campaign", "conversion", "tracking"],
            "sales_forecasting": ["forecast", "pipeline", "prediction", "probability"]
        }
        
        # Get keywords for this intent
        keywords = intent_keywords.get(intent, [])
        
        if not keywords:
            return True  # No specific filtering for unknown intents
        
        # Check if field contains intent-relevant keywords
        return any(keyword in field_text for keyword in keywords)