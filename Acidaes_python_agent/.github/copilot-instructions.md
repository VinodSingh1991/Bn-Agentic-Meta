# Copilot Instructions for Acidaes Python Agent

## Project Overview
This codebase is a FastAPI-based microservice for metadata normalization and entity extraction, supporting natural language query normalization and metadata management. It is structured for extensibility and integration with external systems.

## Architecture & Key Components
- **main.py**: FastAPI app entry point. Exposes endpoints for query normalization and entity/inverted index generation.
- **src/utility/**: Core business logic modules:
  - `meta_data.py`: Loads and saves metadata from JSON files in `memory_db/orignal` and `memory_db/db`.
  - `query_normalization.py`: Normalizes natural language queries using NLTK (WordNet, stopwords).
  - `entity_normalization.py`: Extracts entities and fields from metadata, generates synonyms.
  - `public_util.py`: Utility functions for extracting and generating field labels, phrases, and word splits.
  - `nlp_dict/`: Contains domain-specific stop words and object synonyms.
- **memory_db/**: Stores source and processed metadata JSON files. `orignal/` is the source, `db/` is the output.
- **nltk_data/**: Local NLTK data (WordNet, stopwords) for offline NLP processing.

## Developer Workflows
- **Run the API**: `uvicorn main:app --reload` (default host: localhost, port: 8000)
- **Endpoints**:
  - `/api/normalize_query?nl_query=...` → Returns normalized query
  - `/api/get_entities` → Generates and saves entities to `entities.json`
  - `/api/get_invertedIndex` → Generates and saves inverted index to `invertedIndex.json`
- **Metadata Update**: Place new source files in `memory_db/orignal/`, then call relevant endpoints to process and save to `memory_db/db/`.
- **NLTK Data**: NLTK data is loaded from `nltk_data/`. If missing, code will auto-download to this folder.

## Project-Specific Patterns & Conventions
- **File Paths**: All metadata file operations use relative paths (`./memory_db/orignal`, `./memory_db/db`).
- **Data Models**: Uses Pydantic models (see `src/interfaces/response_model.py`) for structured metadata.
- **Synonym Generation**: Field and object synonyms are generated using custom logic in `entity_normalization.py` and `nlp_dict/object_synonyms.py`.
- **Stop Words**: Custom stop words are defined in `nlp_dict/stop_words.py` and used in query normalization.
- **Error Handling**: Input validation is performed (e.g., type checks in `QueryNormalization`).

## Integration Points
- **External Libraries**: FastAPI, NLTK, Pydantic
- **No requirements.txt**: Dependencies are managed manually; ensure FastAPI, NLTK, and Pydantic are installed in your environment.
- **CORS**: Enabled for all origins for API accessibility.

## Examples
- To normalize a query: `GET /api/normalize_query?nl_query=Show all customer fields`
- To update entities after changing metadata: Place new `fields.json` in `memory_db/orignal/`, then call `GET /api/get_entities`

## Key Files & Directories
- `main.py`, `src/utility/`, `memory_db/`, `nltk_data/`

---
For questions or unclear conventions, review the relevant module in `src/utility/` or ask for clarification.
