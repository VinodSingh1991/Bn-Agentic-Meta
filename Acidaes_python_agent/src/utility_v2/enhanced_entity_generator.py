"""
Enhanced Entity Generator for utility_v2
Creates entities.json with enhanced features for faster searching and better context generation
Based on the original utility folder process with enhancements
"""

import json
import logging
import sys
import os
from typing import Dict, List, Optional, Any
from pathlib import Path

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.utility.meta_data import MetaDataUtility
from src.utility.public_util import get_data_from_response_data, generate_words
from src.utility.nlp_dict.object_synonyms import OBJECT_SYNONYMS

logger = logging.getLogger(__name__)

class EnhancedEntityGenerator:
    """
    Enhanced version of entity generation with additional features:
    - Semantic indexing for faster searches
    - Enhanced synonym generation
    - Relevance scoring metadata
    - Fast lookup indexes
    """
    
    def __init__(self, source_folder: str = None):
        # Use absolute path to memory_db folder  
        if source_folder is None:
            current_dir = Path(__file__).parent
            project_root = current_dir.parent.parent
            source_folder = str(project_root / "memory_db" / "orignal")
        
        self.source_folder = source_folder
        self.meta_data_utility = MetaDataUtility(folder_path=source_folder)
        self.output_file = "./src/utility_v2/entities.json"
        
    def get_fields_dict(self) -> Dict[str, Any]:
        """Get fields as a dictionary with fieldId as key (enhanced version)"""
        field_collection = {}
        
        try:
            # Get system fields
            system_fields_response = self.meta_data_utility.get_fields_from_src("system_fields.json")
            custom_fields_response = self.meta_data_utility.get_fields_from_src("fields.json")
            
            system_fields_data = get_data_from_response_data(system_fields_response)
            custom_fields_data = get_data_from_response_data(custom_fields_response)
            
            for field in system_fields_data + custom_fields_data:
                field_dict = field.dict() if hasattr(field, "dict") else dict(field)
                field_id = field_dict.get("fieldId")
                
                if field_id:
                    # Enhanced field ID processing
                    field_id_str = str(field_id).strip().lstrip("-").rstrip("-")
                    field_collection[field_id_str] = field_dict
                    
        except Exception as e:
            logger.error(f"Error loading fields data: {e}")
            
        return field_collection
    
    def get_object_dict(self) -> Dict[str, Any]:
        """Get objects as a dictionary with objectId as key (enhanced version)"""
        object_collection = {}
        
        try:
            objects_response = self.meta_data_utility.get_fields_from_src("objects.json")
            objects_data = get_data_from_response_data(objects_response)
            
            for obj in objects_data:
                obj_dict = obj.dict() if hasattr(obj, "dict") else dict(obj)
                obj_id = obj_dict.get("objectId")
                
                if obj_id:
                    object_collection[obj_id] = obj_dict
                    
        except Exception as e:
            logger.error(f"Error loading objects data: {e}")
            
        return object_collection
    
    def get_layout_by_object_id(self, object_id: str) -> Optional[List[str]]:
        """Get layout fields for an object ID"""
        try:
            layout_response = self.meta_data_utility.get_fields_from_src("layouts.json")
            layout_data = get_data_from_response_data(layout_response)
            
            for layout in layout_data:
                layout_dict = layout.dict() if hasattr(layout, "dict") else dict(layout)
                layout_object_id = layout_dict.get("objectId")
                fields = layout_dict.get("fields")
                
                if layout_object_id == object_id and fields:
                    return fields
                    
        except Exception as e:
            logger.error(f"Error loading layout data for object {object_id}: {e}")
            
        return None
    
    def get_enhanced_field_synonyms(self, field_name: str, field_label: str, 
                                  field_modified: str, field_layout_id: str) -> List[str]:
        """Generate enhanced synonyms for fields with semantic analysis"""
        synonyms_set = set()
        
        # Add all available field identifiers
        if field_name:
            synonyms_set.add(field_name)
        if field_label:
            synonyms_set.add(field_label)
        if field_modified:
            synonyms_set.add(field_modified)
        if field_layout_id:
            synonyms_set.add(field_layout_id)
            
        # Generate word variants using the existing utility
        initial_synonyms = list(synonyms_set)
        enhanced_synonyms = generate_words(initial_synonyms)
        
        # Add semantic enhancements based on field type/name
        semantic_synonyms = self._generate_semantic_field_synonyms(field_name, field_label)
        enhanced_synonyms.extend(semantic_synonyms)
        
        # Remove duplicates and return
        return list(set(enhanced_synonyms))
    
    def _generate_semantic_field_synonyms(self, field_name: str, field_label: str) -> List[str]:
        """Generate semantic synonyms based on field meaning"""
        semantic_synonyms = []
        
        # Common field patterns and their synonyms
        field_patterns = {
            'name': ['title', 'label', 'identifier', 'full name'],
            'email': ['e-mail', 'electronic mail', 'mail address', 'contact email'],
            'phone': ['telephone', 'mobile', 'contact number', 'phone number'],
            'address': ['location', 'street', 'billing address', 'mailing address'],
            'status': ['state', 'condition', 'stage', 'current status'],
            'amount': ['value', 'price', 'cost', 'revenue', 'sum'],
            'date': ['time', 'when', 'timestamp', 'created date'],
            'priority': ['importance', 'urgency', 'level', 'severity'],
            'description': ['details', 'notes', 'summary', 'comments'],
            'type': ['category', 'kind', 'classification', 'genre'],
            'id': ['identifier', 'key', 'reference', 'number']
        }
        
        # Check field name and label for patterns
        for pattern, synonyms in field_patterns.items():
            if pattern in (field_name or '').lower() or pattern in (field_label or '').lower():
                semantic_synonyms.extend(synonyms)
                
        return semantic_synonyms
    
    def get_enhanced_object_synonyms(self, object_name: str) -> List[str]:
        """Get enhanced object synonyms from the dictionary"""
        if not object_name:
            return []
            
        # Get base synonyms from the dictionary
        base_synonyms = OBJECT_SYNONYMS.get(object_name, [])
        
        # Add semantic enhancements
        enhanced_synonyms = base_synonyms.copy()
        
        # Add common business object patterns
        if object_name.endswith('s'):  # Plural objects
            singular = object_name[:-1]
            enhanced_synonyms.append(singular)
            
        # Add lowercase and variations
        enhanced_synonyms.append(object_name.lower())
        if base_synonyms:
            enhanced_synonyms.extend([syn.lower() for syn in base_synonyms])
            
        return list(set(enhanced_synonyms))
    
    def get_enhanced_field_entities(self) -> Dict[str, Any]:
        """Generate enhanced field entities with additional metadata"""
        entities = {}
        fields_dict = self.get_fields_dict()
        
        for field_id, field_info in fields_dict.items():
            try:
                # Extract field information
                field_name = field_info.get("fieldName")
                field_label = field_info.get("fieldLabel")
                object_id = field_info.get("objectId")
                object_name = field_info.get("objectName")
                field_modified = field_info.get("modifiedFieldId")
                field_layout_id = field_info.get("layoutFieldId")
                data_type = field_info.get("dataType", "string")
                
                # Generate enhanced synonyms
                enhanced_synonyms = self.get_enhanced_field_synonyms(
                    field_name, field_label, field_modified, field_layout_id
                )
                
                # Create enhanced entity
                entities[field_id] = {
                    "index": field_id,
                    "type": "field",
                    "parentId": object_id,
                    "parentName": object_name,
                    "field_id": field_id,
                    "field_name": field_name,
                    "relation": "objectId",
                    "fieldLabel": field_label,
                    "layout_field_id": field_layout_id,
                    "object_name": object_name,
                    "object_id": object_id,
                    "data_type": data_type,
                    "key": field_layout_id or field_id,
                    "field_synonyms": enhanced_synonyms
                }
                
            except Exception as e:
                logger.error(f"Error processing field {field_id}: {e}")
                # Keep empty object for failed processing
                entities[field_id] = {}
                
        return entities
    
    def get_enhanced_object_entities(self) -> Dict[str, Any]:
        """Generate enhanced object entities with additional metadata"""
        entities = {}
        object_dict = self.get_object_dict()
        
        for object_id, object_info in object_dict.items():
            try:
                object_name = object_info.get("objectName")
                
                # Generate enhanced synonyms
                enhanced_synonyms = self.get_enhanced_object_synonyms(object_name)
                
                # Create enhanced entity
                entities[object_id] = {
                    "index": object_id,
                    "type": "object",
                    "parentId": "rootId",
                    "parentName": "rootName",
                    "relation": "self_parent",
                    "object_id": object_id,
                    "object_name": object_name,
                    "object_synonyms": enhanced_synonyms
                }
                
            except Exception as e:
                logger.error(f"Error processing object {object_id}: {e}")
                # Keep empty object for failed processing
                entities[object_id] = {}
                
        return entities
    
    def generate_enhanced_entities(self) -> Dict[str, Any]:
        """Generate the complete enhanced entities dictionary"""
        logger.info("Starting enhanced entity generation...")
        
        # Generate field and object entities
        field_entities = self.get_enhanced_field_entities()
        object_entities = self.get_enhanced_object_entities()
        
        # Combine entities
        all_entities = {**object_entities, **field_entities}
        
        logger.info(f"Generated {len(all_entities)} entities ({len(object_entities)} objects, {len(field_entities)} fields)")
        
        return all_entities
    
    def save_entities_to_file(self, entities: Optional[Dict[str, Any]] = None) -> str:
        """Save the enhanced entities to JSON file"""
        if entities is None:
            entities = self.generate_enhanced_entities()
            
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
            
            # Save to file
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(entities, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Enhanced entities saved to {self.output_file}")
            return self.output_file
            
        except Exception as e:
            logger.error(f"Error saving entities to file: {e}")
            raise
    
    def generate_inverted_index(self, entities: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """Generate enhanced inverted index for fast synonym lookup - preserving original case"""
        if entities is None:
            entities = self.generate_enhanced_entities()
            
        inverted_index = {}
        processed_entities = 0
        skipped_entities = 0
        total_synonyms = 0
        
        for entity_id, entity_data in entities.items():
            if not entity_data:  # Skip empty entities
                skipped_entities += 1
                continue
                
            processed_entities += 1
            
            # Get synonyms based on entity type
            synonyms = []
            if entity_data.get("type") == "field":
                synonyms = entity_data.get("field_synonyms", [])
            elif entity_data.get("type") == "object":
                synonyms = entity_data.get("object_synonyms", [])
            
            # Create inverted index entries - preserve original case
            for synonym in synonyms:
                if synonym and str(synonym).strip():
                    # Use original case for the key, but ensure it's a clean string
                    clean_synonym = str(synonym).strip()
                    if clean_synonym:
                        # If duplicate exists, keep the first occurrence (case-insensitive check)
                        existing_key = None
                        for existing in inverted_index.keys():
                            if existing.lower() == clean_synonym.lower():
                                existing_key = existing
                                break
                        
                        if not existing_key:
                            inverted_index[clean_synonym] = entity_id
                            total_synonyms += 1
                        
        logger.info(f"Inverted index generation: {processed_entities} entities processed, "
                   f"{skipped_entities} skipped, {total_synonyms} unique synonyms indexed")
        
        return inverted_index
    
    def save_inverted_index(self, inverted_index: Optional[Dict[str, str]] = None) -> str:
        """Save the enhanced inverted index to JSON file"""
        if inverted_index is None:
            inverted_index = self.generate_inverted_index()
            
        output_file = "./src/utility_v2/inverted_index.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(inverted_index, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Enhanced inverted index saved to {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error saving inverted index: {e}")
            raise

def main():
    """Main function to generate enhanced entities"""
    generator = EnhancedEntityGenerator()
    
    try:
        # Generate and save entities
        entities = generator.generate_enhanced_entities()
        generator.save_entities_to_file(entities)
        
        # Generate and save inverted index
        inverted_index = generator.generate_inverted_index(entities)
        generator.save_inverted_index(inverted_index)
        
        # Verification: Check that all inverted index entries point to valid entities
        valid_mappings = 0
        invalid_mappings = 0
        for synonym, entity_id in inverted_index.items():
            if entity_id in entities:
                valid_mappings += 1
            else:
                invalid_mappings += 1
                print(f"⚠️  Invalid mapping: '{synonym}' -> '{entity_id}' (entity not found)")
        
        print(f"✅ Verification: {valid_mappings} valid mappings, {invalid_mappings} invalid mappings")
        
    except Exception as e:
        print(f"❌ Entity generation failed: {e}")
        raise

if __name__ == "__main__":
    main()