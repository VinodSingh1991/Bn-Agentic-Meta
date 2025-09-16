from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.utility.meta_data import MetaDataUtility
from src.utility.query_normalization import QueryNormalization
from src.utility.entity_normalization import EntityNormalization
from src.utility.context_normalization import ContextNormalization

app = FastAPI()

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
    context_normalizer = ContextNormalization(nl_query)
    context = context_normalizer.get_context()
    return {"context": context}

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="localhost", port=8000)