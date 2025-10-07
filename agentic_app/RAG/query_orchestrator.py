from typing import List, Dict, Any, Optional
from RAG.query_builder import BaseQueryBuilder
from RAG.query_utils import ObjectManager, QuerySaver, QueryValidator, QueryStatistics


class QueryOrchestrator:
    """Orchestrates multiple query builders and manages the overall query generation process"""
    
    def __init__(self, object_manager: ObjectManager, query_saver: QuerySaver):
        self.object_manager = object_manager
        self.query_saver = query_saver
        self.validator = QueryValidator()
        self.builders: List[BaseQueryBuilder] = []
        
    def add_builder(self, builder: BaseQueryBuilder) -> 'QueryOrchestrator':
        """Add a query builder to the orchestrator (chainable)"""
        self.builders.append(builder)
        return self
    
    def add_builders(self, builders: List[BaseQueryBuilder]) -> 'QueryOrchestrator':
        """Add multiple query builders (chainable)"""
        self.builders.extend(builders)
        return self
    
    def clear_builders(self) -> 'QueryOrchestrator':
        """Clear all builders (chainable)"""
        self.builders.clear()
        return self
    
    def generate_queries(self, objects: Optional[List[Dict[str, Any]]] = None) -> List[Any]:
        """Generate queries using all registered builders"""
        if objects is None:
            objects = self.object_manager.load_objects()
        
        if not objects:
            print("No objects available for query generation")
            return []
        
        all_queries = []
        
        for i, builder in enumerate(self.builders):
            try:
                print(f"Running builder {i+1}/{len(self.builders)}: {builder.__class__.__name__}")
                queries = builder.build_queries(objects)
                all_queries.extend(queries)
                print(f"Generated {len(queries)} queries from {builder.__class__.__name__}")
            except Exception as e:
                print(f"Error in builder {builder.__class__.__name__}: {e}")
                continue
        
        return all_queries
    
    def generate_and_save(self, filename: str = "orchestrated_queries.json", 
                         objects: Optional[List[Dict[str, Any]]] = None) -> List[Any]:
        """Generate queries and save them to file"""
        queries = self.generate_queries(objects)
        
        if queries:
            # Validate queries
            valid_queries = self.validator.filter_valid_queries(queries)
            
            # Save queries
            if self.query_saver.save_queries(valid_queries, filename):
                print(f"Saved {len(valid_queries)} valid queries out of {len(queries)} total")
            
            # Show statistics
            QueryStatistics.print_stats(valid_queries)
            
            return valid_queries
        else:
            print("No queries generated")
            return []
    
    def get_builder_info(self) -> List[Dict[str, str]]:
        """Get information about registered builders"""
        return [
            {
                "name": builder.__class__.__name__,
                "module": builder.__class__.__module__,
                "type": type(builder).__name__
            }
            for builder in self.builders
        ]
    
    def print_builder_info(self):
        """Print information about registered builders"""
        print(f"\n=== Query Builders ({len(self.builders)}) ===")
        for i, info in enumerate(self.get_builder_info(), 1):
            print(f"{i}. {info['name']}")
        print("=" * 30)


class QueryPipeline:
    """High-level pipeline for query generation with predefined configurations"""
    
    def __init__(self, object_manager: ObjectManager, query_saver: QuerySaver):
        self.object_manager = object_manager
        self.query_saver = query_saver
        self.orchestrator = QueryOrchestrator(object_manager, query_saver)
    
    def create_simple_pipeline(self, base_patterns: List[str], in_patterns: List[str], 
                              related_patterns: List[str]) -> QueryOrchestrator:
        """Create a pipeline for simple string queries"""
        from RAG.query_builder import SimpleQueryBuilder, RelatedQueryBuilder
        
        return (self.orchestrator
                .clear_builders()
                .add_builder(SimpleQueryBuilder(base_patterns, in_patterns))
                .add_builder(RelatedQueryBuilder(related_patterns, in_patterns)))
    
    def create_structured_pipeline(self, pattern_dict: Dict[str, Dict], 
                                  in_patterns_dict: Dict[str, Dict],
                                  related_patterns_dict: Dict[str, Dict]) -> QueryOrchestrator:
        """Create a pipeline for structured queries"""
        from RAG.query_builder import StructuredQueryBuilder, StructuredRelatedQueryBuilder
        
        return (self.orchestrator
                .clear_builders()
                .add_builder(StructuredQueryBuilder(pattern_dict, in_patterns_dict))
                .add_builder(StructuredRelatedQueryBuilder(related_patterns_dict, in_patterns_dict)))
    
    def create_hybrid_pipeline(self, simple_patterns: Dict[str, List[str]], 
                              structured_patterns: Dict[str, Dict]) -> QueryOrchestrator:
        """Create a pipeline that combines simple and structured queries"""
        from RAG.query_builder import (
            SimpleQueryBuilder, RelatedQueryBuilder,
            StructuredQueryBuilder, StructuredRelatedQueryBuilder
        )
        
        return (self.orchestrator
                .clear_builders()
                .add_builder(SimpleQueryBuilder(
                    simple_patterns['base'], simple_patterns['in_patterns']
                ))
                .add_builder(RelatedQueryBuilder(
                    simple_patterns['related'], simple_patterns['in_patterns']
                ))
                .add_builder(StructuredQueryBuilder(
                    structured_patterns['base'], structured_patterns['in_patterns']
                ))
                .add_builder(StructuredRelatedQueryBuilder(
                    structured_patterns['related'], structured_patterns['in_patterns']
                )))


class ConfigurableRagCreator:
    """Configurable RAG creator using the pipeline architecture"""
    
    def __init__(self, file_loader):
        self.object_manager = ObjectManager(file_loader)
        self.query_saver = QuerySaver(file_loader)
        self.pipeline = QueryPipeline(self.object_manager, self.query_saver)
    
    def create_simple_queries(self, patterns_config: Dict[str, List[str]], 
                             filename: str = "simple_queries.json") -> List[str]:
        """Create simple queries using configuration"""
        orchestrator = self.pipeline.create_simple_pipeline(
            patterns_config['base_patterns'],
            patterns_config['in_patterns'],
            patterns_config['related_patterns']
        )
        
        return orchestrator.generate_and_save(filename)
    
    def create_structured_queries(self, patterns_config: Dict[str, Dict], 
                                 filename: str = "structured_queries.json") -> List[Dict[str, Any]]:
        """Create structured queries using configuration"""
        orchestrator = self.pipeline.create_structured_pipeline(
            patterns_config['base_patterns'],
            patterns_config['in_patterns'],
            patterns_config['related_patterns']
        )
        
        return orchestrator.generate_and_save(filename)
    
    def create_hybrid_queries(self, simple_config: Dict[str, List[str]], 
                             structured_config: Dict[str, Dict],
                             filename: str = "hybrid_queries.json") -> List[Any]:
        """Create both simple and structured queries"""
        orchestrator = self.pipeline.create_hybrid_pipeline(simple_config, structured_config)
        
        return orchestrator.generate_and_save(filename)