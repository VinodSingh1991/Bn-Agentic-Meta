"""
Enhanced Smart Entity Manager with improved precision and context accuracy
Core functionality for entity and field management
"""

import json
import os
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
import logging
import re

logger = logging.getLogger(__name__)

@dataclass
class FieldInfo:
    """Enhanced field information structure"""
    layout_field_id: str
    object_name: str
    object_id: str
    field_name: str
    synonyms: List[str]
    data_type: str
    key: str
    relevance_score: float = 0.0

@dataclass
class ObjectInfo:
    """Enhanced object information structure"""
    object_name: str
    object_id: str
    synonyms: List[str]
    key: str
    relevance_score: float = 0.0

class EnhancedSmartEntityManager:
    """
    Enhanced entity manager for high-precision field and entity matching
    """
    
    def __init__(self, entities_file_path: str = "./src/utility_v2/entities.json"):
        self.entities_file_path = entities_file_path
        
        # Core indexes
        self.layout_field_index: Dict[str, FieldInfo] = {}
        self.object_index: Dict[str, ObjectInfo] = {}
        self.object_fields_index: Dict[str, List[str]] = {}
        self.synonym_field_index: Dict[str, str] = {}
        self.synonym_object_index: Dict[str, str] = {}
        
        # Enhanced search indexes
        self.field_term_index: Dict[str, Set[str]] = {}
        self.object_term_index: Dict[str, Set[str]] = {}
        
        # Semantic patterns
        self._load_semantic_patterns()
        self._build_indexes()
    
    def _load_semantic_patterns(self):
        """Load semantic patterns for better query understanding"""
        self.semantic_patterns = {
            "contact_info": ["email", "phone", "mobile", "telephone", "contact"],
            "identity": ["name", "title", "id", "identifier"],
            "location": ["address", "city", "state", "country", "location", "region"],
            "status": ["status", "state", "stage", "priority", "condition"],
            "financial": ["amount", "price", "revenue", "value", "cost", "budget"],
            "dates": ["date", "time", "created", "modified", "close", "due"],
            "description": ["description", "details", "notes", "comments", "subject"]
        }
    
    def _build_indexes(self) -> None:
        """Build core performance indexes"""
        try:
            entities = self._load_entities()
            
            for key, entity_data in entities.items():
                if self._has_layout_field_id(entity_data):
                    self._index_field_enhanced(key, entity_data)
                elif self._has_object_data(entity_data):
                    self._index_object_enhanced(key, entity_data)
            
            self._build_term_indexes()
            
        except Exception as e:
            logger.error(f"Failed to build indexes: {e}")
            raise
    
    def _load_entities(self) -> Dict:
        """Load entities.json file with error handling"""
        if not os.path.exists(self.entities_file_path):
            logger.warning(f"Entities file not found: {self.entities_file_path}")
            return {}
            
        try:
            with open(self.entities_file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load entities file: {e}")
            return {}
    
    def _has_layout_field_id(self, entity_data: Dict) -> bool:
        """Check if entity has layout_field_id (indicates it's a field)"""
        return isinstance(entity_data, dict) and 'layout_field_id' in entity_data and entity_data['layout_field_id']
    
    def _has_object_data(self, entity_data: Dict) -> bool:
        """Check if entity has object data (indicates it's an object)"""
        return (isinstance(entity_data, dict) and 
                ('object_name' in entity_data or 'objectName' in entity_data))
    
    def _index_field_enhanced(self, key: str, entity_data: Dict) -> None:
        """Enhanced field indexing with better synonym and term handling"""
        try:
            layout_field_id = entity_data.get('layout_field_id', '')
            if not layout_field_id:
                return
                
            field_name = (entity_data.get('field_name') or 
                         entity_data.get('label') or 
                         entity_data.get('title', ''))
            
            object_name = (entity_data.get('object_name') or 
                          entity_data.get('objectName', ''))
            
            data_type = entity_data.get('data_type', 'string')
            
            # Enhanced synonym processing
            synonyms = self._process_field_synonyms(entity_data, field_name)
            object_id = str(entity_data.get('object_id', key))
            
            field_info = FieldInfo(
                layout_field_id=layout_field_id,
                object_name=object_name,
                object_id=object_id,
                field_name=field_name,
                synonyms=synonyms,
                data_type=data_type,
                key=key
            )
            
            # Index by layout_field_id (O(1) lookup)
            self.layout_field_index[layout_field_id] = field_info
            
            # Index object -> fields relationship
            if object_name:
                if object_name not in self.object_fields_index:
                    self.object_fields_index[object_name] = []
                self.object_fields_index[object_name].append(layout_field_id)
            
            # Enhanced synonym indexing
            all_terms = self._extract_field_terms(field_name, synonyms, layout_field_id)
            for term in all_terms:
                self.synonym_field_index[term.lower().strip()] = layout_field_id
                    
        except Exception as e:
            logger.warning(f"Failed to index field {key}: {e}")
    
    def _process_field_synonyms(self, entity_data: Dict, field_name: str) -> List[str]:
        """Enhanced synonym processing with automatic generation"""
        synonyms = entity_data.get('field_synonyms', [])
        if isinstance(synonyms, str):
            synonyms = [synonyms]
        elif not isinstance(synonyms, list):
            synonyms = []
        
        # Add field name variants
        if field_name:
            synonyms.extend(self._generate_field_name_variants(field_name))
        
        # Add layout_field_id variants
        layout_id = entity_data.get('layout_field_id', '')
        if layout_id:
            synonyms.extend(self._generate_layout_id_variants(layout_id))
        
        return list(set(synonyms))  # Remove duplicates
    
    def _generate_field_name_variants(self, field_name: str) -> List[str]:
        """Generate variants of field names for better matching"""
        variants = []
        lower_name = field_name.lower()
        
        # Add the original name
        variants.append(lower_name)
        
        # Remove common prefixes/suffixes
        cleaned = re.sub(r'^(case_|ac_|le_|op_)', '', lower_name)
        cleaned = re.sub(r'(_code|_id|_name)$', '', cleaned)
        if cleaned != lower_name:
            variants.append(cleaned)
        
        # Split compound words
        parts = re.split(r'[_\s-]+', lower_name)
        variants.extend(parts)
        
        # Add semantic variations
        semantic_map = {
            'name': ['title', 'label', 'identifier'],
            'email': ['mail', 'e-mail', 'electronic mail'],
            'phone': ['telephone', 'contact number', 'mobile'],
            'address': ['location', 'street', 'residence'],
            'status': ['state', 'condition', 'stage'],
            'amount': ['value', 'price', 'cost', 'revenue']
        }
        
        for part in parts:
            if part in semantic_map:
                variants.extend(semantic_map[part])
        
        return [v for v in variants if v]  # Remove empty strings
    
    def _generate_layout_id_variants(self, layout_id: str) -> List[str]:
        """Generate variants of layout field IDs"""
        variants = []
        lower_id = layout_id.lower()
        
        # Add original
        variants.append(lower_id)
        
        # Split by underscore
        parts = lower_id.split('_')
        variants.extend(parts)
        
        # Remove prefixes
        if len(parts) > 1:
            variants.append('_'.join(parts[1:]))
        
        return [v for v in variants if v and len(v) > 1]
    
    def _extract_field_terms(self, field_name: str, synonyms: List[str], layout_id: str) -> Set[str]:
        """Extract all searchable terms for a field"""
        terms = set()
        
        # Add field name terms
        if field_name:
            terms.update(self._extract_terms_from_text(field_name))
        
        # Add synonym terms
        for synonym in synonyms:
            terms.update(self._extract_terms_from_text(synonym))
        
        # Add layout ID terms
        terms.update(self._extract_terms_from_text(layout_id))
        
        return terms
    
    def _extract_terms_from_text(self, text: str) -> Set[str]:
        """Extract meaningful terms from text"""
        if not text:
            return set()
        
        # Split by various delimiters
        terms = set()
        parts = re.split(r'[_\s-]+', text.lower())
        
        for part in parts:
            # Clean the part
            clean_part = re.sub(r'[^a-z0-9]', '', part)
            if len(clean_part) > 1:  # Ignore single characters
                terms.add(clean_part)
        
        # Add the full text as well
        clean_full = re.sub(r'[^a-z0-9\s]', '', text.lower()).strip()
        if clean_full:
            terms.add(clean_full)
        
        return terms
    
    def _index_object_enhanced(self, key: str, entity_data: Dict) -> None:
        """Enhanced object indexing with better synonym handling"""
        try:
            object_name = (entity_data.get('object_name') or 
                          entity_data.get('objectName') or 
                          entity_data.get('label', ''))
            
            if not object_name:
                return
                
            object_id = str(entity_data.get('object_id', key))
            
            # Enhanced synonym processing
            synonyms = self._process_object_synonyms(entity_data, object_name)
            
            obj_info = ObjectInfo(
                object_name=object_name,
                object_id=object_id,
                synonyms=synonyms,
                key=key
            )
            
            # Index by object name
            self.object_index[object_name] = obj_info
            
            # Enhanced synonym indexing
            all_terms = self._extract_object_terms(object_name, synonyms)
            for term in all_terms:
                self.synonym_object_index[term.lower().strip()] = object_name
                    
        except Exception as e:
            logger.warning(f"Failed to index object {key}: {e}")
    
    def _process_object_synonyms(self, entity_data: Dict, object_name: str) -> List[str]:
        """Enhanced object synonym processing"""
        synonyms = entity_data.get('object_synonyms', [])
        if isinstance(synonyms, str):
            synonyms = [synonyms]
        elif not isinstance(synonyms, list):
            synonyms = []
        
        # Add object name variants
        if object_name:
            synonyms.extend(self._generate_object_name_variants(object_name))
        
        return list(set(synonyms))  # Remove duplicates
    
    def _generate_object_name_variants(self, object_name: str) -> List[str]:
        """Generate variants of object names"""
        variants = []
        lower_name = object_name.lower()
        
        # Add original
        variants.append(lower_name)
        
        # Add singular/plural forms
        if lower_name.endswith('s'):
            variants.append(lower_name[:-1])  # Remove 's' for singular
        else:
            variants.append(lower_name + 's')  # Add 's' for plural
        
        # Add common business synonyms
        business_synonyms = {
            'accounts': ['customers', 'clients', 'companies', 'organizations'],
            'leads': ['prospects', 'potential customers'],
            'opportunities': ['deals', 'sales', 'revenue opportunities'],
            'cases': ['tickets', 'issues', 'problems', 'support requests'],
            'contacts': ['people', 'individuals', 'persons']
        }
        
        if lower_name in business_synonyms:
            variants.extend(business_synonyms[lower_name])
        
        return variants
    
    def _extract_object_terms(self, object_name: str, synonyms: List[str]) -> Set[str]:
        """Extract all searchable terms for an object"""
        terms = set()
        
        # Add object name terms
        if object_name:
            terms.update(self._extract_terms_from_text(object_name))
        
        # Add synonym terms
        for synonym in synonyms:
            terms.update(self._extract_terms_from_text(synonym))
        
        return terms
    
    def _build_term_indexes(self):
        """Build term-based indexes for faster searching"""
        # Build field term index
        for field_id, field_info in self.layout_field_index.items():
            all_terms = self._extract_field_terms(
                field_info.field_name, 
                field_info.synonyms, 
                field_info.layout_field_id
            )
            
            for term in all_terms:
                if term not in self.field_term_index:
                    self.field_term_index[term] = set()
                self.field_term_index[term].add(field_id)
        
        # Build object term index
        for obj_name, obj_info in self.object_index.items():
            all_terms = self._extract_object_terms(obj_info.object_name, obj_info.synonyms)
            
            for term in all_terms:
                if term not in self.object_term_index:
                    self.object_term_index[term] = set()
                self.object_term_index[term].add(obj_name)
    
    def get_relevant_fields_for_query_enhanced(self, nl_query: str, min_relevance: float = 0.3) -> List[FieldInfo]:
        """Enhanced query processing with relevance scoring"""
        query_terms = self._extract_query_terms_enhanced(nl_query)
        semantic_context = self._detect_semantic_context(nl_query)
        
        field_scores = {}
        
        # Score fields based on direct term matches
        for term in query_terms:
            matching_fields = self.field_term_index.get(term, set())
            for field_id in matching_fields:
                if field_id not in field_scores:
                    field_scores[field_id] = 0.0
                field_scores[field_id] += 1.0
        
        # Boost scores based on semantic context
        for context, patterns in self.semantic_patterns.items():
            if context in semantic_context:
                for pattern in patterns:
                    matching_fields = self.field_term_index.get(pattern, set())
                    for field_id in matching_fields:
                        if field_id not in field_scores:
                            field_scores[field_id] = 0.0
                        field_scores[field_id] += 0.5  # Semantic boost
        
        # Filter and sort by relevance
        relevant_fields = []
        max_score = max(field_scores.values()) if field_scores else 1.0
        
        for field_id, score in field_scores.items():
            normalized_score = score / max_score
            if normalized_score >= min_relevance:
                field_info = self.layout_field_index[field_id]
                field_info.relevance_score = normalized_score
                relevant_fields.append(field_info)
        
        # Sort by relevance score
        relevant_fields.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return relevant_fields
    
    def _extract_query_terms_enhanced(self, query: str) -> List[str]:
        """Enhanced query term extraction with better filtering"""
        # Expanded stop words
        stop_words = {
            "show", "get", "list", "display", "find", "search", "fetch", "retrieve",
            "all", "some", "any", "for", "with", "by", "from", "in", "on", "at",
            "the", "a", "an", "and", "or", "but", "of", "to", "is", "are", "was", "were",
            "that", "this", "these", "those", "my", "your", "his", "her", "its", "our", "their"
        }
        
        # Extract meaningful terms
        terms = []
        words = re.findall(r'\b\w+\b', query.lower())
        
        for word in words:
            if (word not in stop_words and 
                len(word) > 2 and 
                not word.isdigit()):
                terms.append(word)
        
        return terms
    
    def _detect_semantic_context(self, query: str) -> List[str]:
        """Detect semantic context from query"""
        contexts = []
        query_lower = query.lower()
        
        # Pattern matching for different contexts
        context_patterns = {
            "contact_info": ["email", "phone", "contact", "call", "reach"],
            "identity": ["name", "who", "identity", "person", "individual"],
            "location": ["where", "address", "location", "city", "region"],
            "status": ["status", "state", "condition", "how", "priority"],
            "financial": ["revenue", "money", "cost", "price", "financial", "budget"],
            "description": ["details", "description", "info", "information", "about"]
        }
        
        for context, patterns in context_patterns.items():
            if any(pattern in query_lower for pattern in patterns):
                contexts.append(context)
        
        return contexts
    
    def get_context_for_query_enhanced(self, nl_query: str) -> Dict[str, Any]:
        """Enhanced context generation with improved accuracy and entity-field relationship respect"""
        context = {
            "available_fields": {},
            "entities": {},
            "field_mappings": {},
            "query_optimization": True,
            "relevance_scores": {},
            "semantic_context": self._detect_semantic_context(nl_query)
        }
        
        # Step 1: Find relevant entities first (this determines which fields are accessible)
        relevant_entities = self._find_relevant_entities_for_query(nl_query)
        
        # Step 2: Get fields only from relevant entities (respecting parentId boundaries)
        relevant_fields = self._get_fields_from_entities(nl_query, relevant_entities)
        
        # Step 3: Build available_fields with improved relevance scores
        for field in relevant_fields:
            context["available_fields"][field.layout_field_id] = {
                "field_name": field.field_name,
                "data_type": field.data_type,
                "synonyms": field.synonyms,
                "object_name": field.object_name,
                "object_id": field.object_id,
                "relevance_score": field.relevance_score
            }
            
            # Add to field mappings for LLM
            context["field_mappings"][field.layout_field_id] = field.field_name
            context["relevance_scores"][field.layout_field_id] = field.relevance_score
        
        # Step 4: Include relevant entities in context
        for entity_obj_id, entity_score in relevant_entities.items():
            # Find the entity by object_id
            for entity_name, obj_info in self.object_index.items():
                if str(obj_info.object_id) == entity_obj_id:
                    context["entities"][entity_name] = {
                        "object_name": obj_info.object_name,
                        "object_id": obj_info.object_id,
                        "synonyms": obj_info.synonyms,
                        "relevance_score": entity_score
                    }
                    break
        
        return context
    
    def _find_relevant_entities_for_query(self, nl_query: str) -> Dict[str, float]:
        """Find relevant entities (objects) for the query with improved scoring"""
        query_terms = self._extract_query_terms_enhanced(nl_query)
        entity_scores = {}
        
        # Score entities based on term matching
        for term in query_terms:
            matching_objects = self.object_term_index.get(term, set())
            for obj_name in matching_objects:
                if obj_name not in entity_scores:
                    entity_scores[obj_name] = 0.0
                
                # Improved scoring: exact matches get higher scores
                if obj_name in self.object_index:
                    obj_info = self.object_index[obj_name]
                    
                    # Exact object name match (highest priority)
                    if term.lower() == obj_info.object_name.lower():
                        entity_scores[obj_name] += 2.0
                    # Exact synonym match (high priority)
                    elif any(term.lower() == syn.lower() for syn in obj_info.synonyms):
                        entity_scores[obj_name] += 1.5
                    # Partial match (lower priority)
                    else:
                        entity_scores[obj_name] += 1.0
        
        # Filter entities with minimum relevance threshold
        min_threshold = 0.5
        relevant_entities = {
            str(self.object_index[entity_name].object_id): score 
            for entity_name, score in entity_scores.items()
            if score >= min_threshold and entity_name in self.object_index
        }
        
        return relevant_entities
    
    def _get_fields_from_entities(self, nl_query: str, relevant_entities: Dict[str, float]) -> List[FieldInfo]:
        """Get fields only from relevant entities, respecting parentId boundaries"""
        if not relevant_entities:
            # If no specific entities found, fall back to direct field matching
            return self.get_relevant_fields_for_query_enhanced(nl_query)
        
        entity_fields = []
        query_terms = self._extract_query_terms_enhanced(nl_query)
        
        # Get all fields that belong to relevant entities (respecting parentId)
        for field_id, field_info in self.layout_field_index.items():
            # Check if this field belongs to any of the relevant entities
            # The object_id in FieldInfo represents the parentId (entity this field belongs to)
            field_parent_id = str(field_info.object_id)
            
            if field_parent_id in relevant_entities:
                # Calculate field relevance score within the entity context
                field_score = self._calculate_field_relevance_score(field_info, query_terms)
                
                # Boost score based on parent entity relevance
                entity_boost = relevant_entities[field_parent_id] * 0.2
                field_score += entity_boost
                
                # Create enhanced field info with improved relevance
                enhanced_field = FieldInfo(
                    field_name=field_info.field_name,
                    layout_field_id=field_info.layout_field_id,
                    object_name=field_info.object_name,
                    object_id=field_info.object_id,
                    data_type=field_info.data_type,
                    synonyms=field_info.synonyms,
                    key=field_id,  # Add the required key parameter
                    relevance_score=min(field_score, 1.0)  # Cap at 1.0
                )
                
                entity_fields.append(enhanced_field)
        
        # Sort by relevance score and apply minimum threshold
        entity_fields.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # Filter by minimum relevance
        min_field_threshold = 0.3
        relevant_fields = [
            field for field in entity_fields 
            if field.relevance_score >= min_field_threshold
        ]
        
        return relevant_fields
    
    def _calculate_field_relevance_score(self, field_info: FieldInfo, query_terms: List[str]) -> float:
        """Calculate improved relevance score for a field based on semantic similarity"""
        score = 0.0
        field_terms = set()
        
        # Extract field-related terms
        field_terms.update(self._extract_terms_from_text(field_info.field_name))
        field_terms.update(self._extract_terms_from_text(field_info.layout_field_id))
        
        # Add synonym terms
        for synonym in field_info.synonyms:
            field_terms.update(self._extract_terms_from_text(synonym))
        
        # Calculate matching score with improved algorithm
        total_query_terms = len(query_terms)
        matched_terms = 0
        
        for query_term in query_terms:
            query_term_lower = query_term.lower()
            
            # Exact field name match (highest priority)
            if query_term_lower == field_info.field_name.lower():
                score += 1.0
                matched_terms += 1
            # Exact synonym match (high priority)
            elif any(query_term_lower == syn.lower() for syn in field_info.synonyms):
                score += 0.8
                matched_terms += 1
            # Partial match in field terms (medium priority)
            elif any(query_term_lower in field_term for field_term in field_terms):
                score += 0.5
                matched_terms += 1
            # Substring match (low priority)
            elif any(field_term in query_term_lower for field_term in field_terms if len(field_term) > 2):
                score += 0.3
                matched_terms += 1
        
        # Normalize score based on query coverage
        if total_query_terms > 0:
            coverage_bonus = matched_terms / total_query_terms * 0.2
            score += coverage_bonus
        
        return min(score, 1.0)  # Cap at 1.0