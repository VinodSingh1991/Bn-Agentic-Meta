# RAG System Refactoring Documentation

## Overview

The RAG (Retrieval-Augmented Generation) system has been refactored into reusable, modular classes that follow SOLID principles and provide better maintainability, testability, and extensibility.

## Architecture

### Core Components

#### 1. Query Builders (`query_builder.py`)

**Abstract Base Class: `BaseQueryBuilder`**
- Provides common functionality for all query builders
- Handles placeholder replacement and validation
- Defines the interface that all builders must implement

**Concrete Builders:**
- `SimpleQueryBuilder`: Generates simple string-based queries
- `StructuredQueryBuilder`: Generates queries with metadata
- `RelatedQueryBuilder`: Generates queries involving related objects
- `StructuredRelatedQueryBuilder`: Generates structured queries with related objects

#### 2. Utility Classes (`query_utils.py`)

**`ObjectManager`**
- Handles loading and validation of objects from files
- Provides object filtering and validation

**`QuerySaver`**
- Manages saving queries to different file formats
- Handles both simple and structured query saving

**`QueryValidator`**
- Validates query formats and structures
- Filters out invalid queries

**`QueryStatistics`**
- Provides statistics about generated queries
- Helps with monitoring and debugging

#### 3. Orchestration (`query_orchestrator.py`)

**`QueryOrchestrator`**
- Manages multiple query builders
- Provides chainable API for adding builders
- Coordinates query generation across builders

**`QueryPipeline`**
- High-level pipeline management
- Predefined configurations for common use cases
- Factory methods for different pipeline types

**`ConfigurableRagCreator`**
- Main entry point for configurable query generation
- Uses pipeline architecture internally

#### 4. Factory and Configuration (`rag_factory.py`)

**`RagFactory`**
- Factory class for creating all RAG components
- Provides static methods for component creation
- Simplifies object creation and dependency injection

**`RagConfigBuilder`**
- Builder pattern for creating configurations
- Chainable API for adding patterns
- Separate methods for simple and structured configurations

**`RagPresetConfigs`**
- Predefined configurations for common scenarios
- Basic, advanced, and comprehensive presets

#### 5. Main RAG Creator (`rag_creater.py`)

**`RagCreator` (Updated)**
- Backward-compatible main class
- Uses new architecture internally
- Provides legacy methods and new functionality

## Benefits of the New Architecture

### 1. **Separation of Concerns**
- Each class has a single responsibility
- Query building, saving, validation, and orchestration are separate
- Easy to modify one aspect without affecting others

### 2. **Reusability**
- Components can be used independently
- Mix and match different builders and configurations
- Easy to create custom combinations

### 3. **Extensibility**
- Easy to add new query builder types
- Simple to create new configurations
- Plugin-like architecture for adding functionality

### 4. **Testability**
- Each component can be tested in isolation
- Mock dependencies easily
- Clear interfaces for testing

### 5. **Maintainability**
- Code is organized logically
- Easy to find and fix issues
- Clear separation between different functionalities

## Usage Patterns

### 1. Basic Usage (Backward Compatible)
```python
rag_creator = RagFactory.create_rag_creator()
queries = rag_creator.build_pattern()
```

### 2. Configurable Usage
```python
configurable_rag = RagFactory.create_configurable_rag_creator()
config = RagPresetConfigs.get_basic_config()
queries = configurable_rag.create_simple_queries(config['simple_patterns'])
```

### 3. Custom Builder Usage
```python
builder = RagFactory.create_simple_query_builder(patterns, in_patterns)
orchestrator = RagFactory.create_orchestrator()
queries = orchestrator.add_builder(builder).generate_and_save("queries.json")
```

### 4. Pipeline Usage
```python
pipeline = RagFactory.create_pipeline()
orchestrator = pipeline.create_simple_pipeline(base_patterns, in_patterns, related_patterns)
queries = orchestrator.generate_and_save("pipeline_queries.json")
```

### 5. Configuration Builder Usage
```python
config = RagConfigBuilder() \
    .add_simple_base_patterns(["What is {Object}?"]) \
    .add_simple_in_patterns(["in detail"]) \
    .build()
```

## File Structure

```
RAG/
├── query_builder.py           # Core query builders
├── query_utils.py            # Utility classes
├── query_orchestrator.py     # Orchestration and pipeline
├── rag_factory.py           # Factory and configuration
├── rag_creater.py           # Main RAG creator (updated)
├── examples/
│   └── rag_usage_examples.py # Usage examples
└── get_query_pattern_by_object.py # Original patterns (unchanged)
```

## Migration Guide

### From Original to New System

**Old Way:**
```python
from RAG.rag_creater import RagCreator

rag = RagCreator()
queries = rag.build_pattern()
```

**New Way (Backward Compatible):**
```python
from RAG.rag_factory import RagFactory

rag = RagFactory.create_rag_creator()
queries = rag.build_pattern()  # Same method, improved implementation
```

**New Way (Full Featured):**
```python
from RAG.rag_factory import RagFactory, RagPresetConfigs

configurable_rag = RagFactory.create_configurable_rag_creator()
config = RagPresetConfigs.get_comprehensive_config()
results = configurable_rag.create_hybrid_queries(
    config['simple_patterns'], 
    config['structured_patterns']
)
```

## Best Practices

### 1. Use Factory Methods
Always use `RagFactory` to create components instead of direct instantiation.

### 2. Leverage Configuration Builder
Use `RagConfigBuilder` for complex configurations instead of manual dictionary creation.

### 3. Use Preset Configurations
Start with `RagPresetConfigs` and customize as needed.

### 4. Chain Operations
Use the chainable API for cleaner code:
```python
orchestrator.add_builder(builder1).add_builder(builder2).generate_and_save("queries.json")
```

### 5. Validate and Monitor
Always check query statistics and validation results for quality assurance.

## Error Handling

The new architecture includes comprehensive error handling:
- Graceful failure of individual builders
- Validation of objects and queries
- Detailed error messages and logging
- Continuation of processing even when some components fail

## Performance Considerations

- Lazy loading of objects
- Efficient validation and filtering
- Memory-conscious query generation
- Optional statistics gathering

## Future Extensibility

The architecture is designed to support:
- New query builder types
- Different file formats and storage backends
- Custom validation rules
- Additional orchestration patterns
- Plugin-based extensions

## Examples

See `RAG/examples/rag_usage_examples.py` for comprehensive usage examples covering all the new functionality.