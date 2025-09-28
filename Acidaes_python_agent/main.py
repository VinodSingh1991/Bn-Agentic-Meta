from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

from src.utility.meta_data import MetaDataUtility
from src.utility.query_normalization import QueryNormalization
from src.utility.entity_normalization import EntityNormalization
from src.utility.context_normalization import ContextNormalization

# Import enhanced context system
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.utility_v2.enhanced_context_api import EnhancedContextAPI

app = FastAPI()

# Initialize enhanced context system with production data
enhanced_context_api = EnhancedContextAPI("./src/utility_v2/entities.json")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/api/normalize_query")
def normalize_query(nl_query: str = ""):
    normalized_query = QueryNormalization.normalize_query(nl_query)
    return {"nl_query": nl_query, "normalized_query": normalized_query}

@app.get("/api/get_entities")
def get_entities():
    entity = EntityNormalization()
    entities = entity.get_entities()
    file_utility = MetaDataUtility()
    file_utility.save_fields_at_db("entities.json", entities)
    #print(entities)
    return {"entities": "Created entities..."}


@app.get("/api/get_invertedIndex")
def get_entities_invert():
    entity = EntityNormalization()
    original_meta = entity.get_invertedIndex()
    file_utility = MetaDataUtility()
    file_utility.save_fields_at_db("invertedIndex.json", original_meta)
    return {"entities": "Created inverted index..."}

@app.get("/api/get_context")
def get_entities_context(nl_query: str = ""):
    """Original context endpoint - enhanced with new system while maintaining compatibility"""
    try:
        # Use enhanced context system with fallback to original
        enhanced_context = enhanced_context_api.get_query_specific_context(nl_query)
        
        # Transform to original format for backward compatibility
        available_fields = enhanced_context.get("available_fields", {})
        field_mappings = {}
        entities = {}
        
        # Convert enhanced format to original format
        for field_id, field_info in available_fields.items():
            field_mappings[field_id] = field_info.get("field_name", "")
            
        for entity_name, entity_info in enhanced_context.get("entities", {}).items():
            entities[entity_name] = entity_info
            
        # Original format response with enhanced precision
        context = {
            "field_mappings": field_mappings,
            "entities": entities,
            "available_fields": available_fields,
            "enhanced": True,
            "relevance_scores": enhanced_context.get("relevance_scores", {}),
            "coverage_metrics": enhanced_context.get("coverage_metrics", {})
        }
        
        return {"context": context}
        
    except Exception as e:
        # Fallback to original system if enhanced system fails
        print(f"Enhanced context failed, using fallback: {e}")
        context_normalizer = ContextNormalization(nl_query)
        context = context_normalizer.get_context()
        return {"context": context}

@app.get("/api/get_enhanced_context")
def get_enhanced_context(nl_query: str = "", optimization: str = "high"):
    """New enhanced context endpoint with full precision features"""
    try:
        context = enhanced_context_api.get_query_specific_context(nl_query)
        return {
            "context": context,
            "query": nl_query,
            "optimization_level": optimization
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced context failed: {str(e)}")

# Remove the unused performance and validation endpoints

@app.post("/api/regenerate_enhanced_entities")
def regenerate_enhanced_entities():
    """Regenerate the enhanced entities.json file from source data"""
    try:
        from src.utility_v2.enhanced_entity_generator import EnhancedEntityGenerator
        
        generator = EnhancedEntityGenerator()
        entities = generator.generate_enhanced_entities()
        entities_file = generator.save_entities_to_file(entities)
        
        # Also regenerate inverted index
        inverted_index = generator.generate_inverted_index(entities)
        index_file = generator.save_inverted_index(inverted_index)
        
        # Reload the enhanced context API with new data
        global enhanced_context_api
        enhanced_context_api = EnhancedContextAPI("./src/utility_v2/entities.json")
        
        return {
            "message": "Enhanced entities regenerated successfully",
            "entities_file": entities_file,
            "index_file": index_file,
            "statistics": {
                "total_entities": len(entities),
                "total_index_terms": len(inverted_index),
                "objects": len([e for e in entities.values() if e and e.get("type") == "object"]),
                "fields": len([e for e in entities.values() if e and e.get("type") == "field"])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Entity regeneration failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="localhost", port=8000)