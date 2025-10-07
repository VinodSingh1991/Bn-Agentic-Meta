from typing import Dict, List, Any
from files_handler.file_loader import FileLoader
from RAG.query_builder import (
    SimpleQueryBuilder, StructuredQueryBuilder, 
    RelatedQueryBuilder, StructuredRelatedQueryBuilder
)
from RAG.query_utils import ObjectManager, QuerySaver, QueryValidator, QueryStatistics
from RAG.query_orchestrator import QueryOrchestrator, QueryPipeline, ConfigurableRagCreator
from RAG.rag_creater import RagCreator


class RagFactory:
    """Factory class for creating different types of RAG components"""
    
    @staticmethod
    def create_rag_creator(file_loader: FileLoader = None) -> RagCreator:
        """Create a standard RAG creator"""
        if file_loader is None:
            file_loader = FileLoader()
        return RagCreator()
    
    @staticmethod
    def create_configurable_rag_creator(file_loader: FileLoader = None) -> ConfigurableRagCreator:
        """Create a configurable RAG creator with pipeline support"""
        if file_loader is None:
            file_loader = FileLoader()
        return ConfigurableRagCreator(file_loader)
    
    @staticmethod
    def create_simple_query_builder(base_patterns: List[str], in_patterns: List[str]) -> SimpleQueryBuilder:
        """Create a simple query builder"""
        return SimpleQueryBuilder(base_patterns, in_patterns)
    
    @staticmethod
    def create_structured_query_builder(pattern_dict: Dict[str, Dict], 
                                       in_patterns_dict: Dict[str, Dict]) -> StructuredQueryBuilder:
        """Create a structured query builder"""
        return StructuredQueryBuilder(pattern_dict, in_patterns_dict)
    
    @staticmethod
    def create_related_query_builder(related_patterns: List[str], 
                                    in_patterns: List[str]) -> RelatedQueryBuilder:
        """Create a related query builder"""
        return RelatedQueryBuilder(related_patterns, in_patterns)
    
    @staticmethod
    def create_structured_related_query_builder(related_patterns_dict: Dict[str, Dict], 
                                               in_patterns_dict: Dict[str, Dict]) -> StructuredRelatedQueryBuilder:
        """Create a structured related query builder"""
        return StructuredRelatedQueryBuilder(related_patterns_dict, in_patterns_dict)
    
    @staticmethod
    def create_orchestrator(file_loader: FileLoader = None) -> QueryOrchestrator:
        """Create a query orchestrator"""
        if file_loader is None:
            file_loader = FileLoader()
        
        object_manager = ObjectManager(file_loader)
        query_saver = QuerySaver(file_loader)
        return QueryOrchestrator(object_manager, query_saver)
    
    @staticmethod
    def create_pipeline(file_loader: FileLoader = None) -> QueryPipeline:
        """Create a query pipeline"""
        if file_loader is None:
            file_loader = FileLoader()
        
        object_manager = ObjectManager(file_loader)
        query_saver = QuerySaver(file_loader)
        return QueryPipeline(object_manager, query_saver)
    
    @staticmethod
    def create_object_manager(file_loader: FileLoader = None) -> ObjectManager:
        """Create an object manager"""
        if file_loader is None:
            file_loader = FileLoader()
        return ObjectManager(file_loader)
    
    @staticmethod
    def create_query_saver(file_loader: FileLoader = None) -> QuerySaver:
        """Create a query saver"""
        if file_loader is None:
            file_loader = FileLoader()
        return QuerySaver(file_loader)
    
    @staticmethod
    def create_query_validator() -> QueryValidator:
        """Create a query validator"""
        return QueryValidator()


class RagConfigBuilder:
    """Builder class for creating RAG configurations"""
    
    def __init__(self):
        self.config = {
            'simple_patterns': {
                'base_patterns': [],
                'in_patterns': [],
                'related_patterns': []
            },
            'structured_patterns': {
                'base_patterns': {},
                'in_patterns': {},
                'related_patterns': {}
            }
        }
    
    def add_simple_base_patterns(self, patterns: List[str]) -> 'RagConfigBuilder':
        """Add simple base patterns"""
        self.config['simple_patterns']['base_patterns'].extend(patterns)
        return self
    
    def add_simple_in_patterns(self, patterns: List[str]) -> 'RagConfigBuilder':
        """Add simple in patterns"""
        self.config['simple_patterns']['in_patterns'].extend(patterns)
        return self
    
    def add_simple_related_patterns(self, patterns: List[str]) -> 'RagConfigBuilder':
        """Add simple related patterns"""
        self.config['simple_patterns']['related_patterns'].extend(patterns)
        return self
    
    def add_structured_base_patterns(self, patterns: Dict[str, Dict]) -> 'RagConfigBuilder':
        """Add structured base patterns"""
        self.config['structured_patterns']['base_patterns'].update(patterns)
        return self
    
    def add_structured_in_patterns(self, patterns: Dict[str, Dict]) -> 'RagConfigBuilder':
        """Add structured in patterns"""
        self.config['structured_patterns']['in_patterns'].update(patterns)
        return self
    
    def add_structured_related_patterns(self, patterns: Dict[str, Dict]) -> 'RagConfigBuilder':
        """Add structured related patterns"""
        self.config['structured_patterns']['related_patterns'].update(patterns)
        return self
    
    def build(self) -> Dict[str, Any]:
        """Build and return the configuration"""
        return self.config.copy()
    
    def build_simple_config(self) -> Dict[str, List[str]]:
        """Build and return only simple configuration"""
        return self.config['simple_patterns'].copy()
    
    def build_structured_config(self) -> Dict[str, Dict]:
        """Build and return only structured configuration"""
        return self.config['structured_patterns'].copy()


class RagPresetConfigs:
    """Predefined configurations for common RAG use cases"""
    
    @staticmethod
    def get_basic_config() -> Dict[str, Any]:
        """Get basic configuration for simple use cases"""
        return RagConfigBuilder() \
            .add_simple_base_patterns([
                "What are {ObjectPlural}?",
                "List all {ObjectPlural}",
                "Show me {Object} details"
            ]) \
            .add_simple_in_patterns([
                "in JSON format",
                "as a table",
                "with examples"
            ]) \
            .add_simple_related_patterns([
                "How do {ObjectPlural} relate to {RelatedObject}?",
                "Compare {ObjectPlural} with {RelatedObject}"
            ]) \
            .build()
    
    @staticmethod
    def get_advanced_config() -> Dict[str, Any]:
        """Get advanced configuration with structured patterns"""
        return RagConfigBuilder() \
            .add_structured_base_patterns({
                "Analyze {ObjectPlural} data": {
                    "type": "analysis",
                    "complexity": "high",
                    "output_type": "report"
                },
                "Generate {Object} summary": {
                    "type": "summary",
                    "complexity": "medium",
                    "output_type": "text"
                }
            }) \
            .add_structured_in_patterns({
                "with detailed metrics": {
                    "format": "detailed",
                    "include_metrics": True
                },
                "in executive summary format": {
                    "format": "executive",
                    "length": "short"
                }
            }) \
            .build()
    
    @staticmethod
    def get_comprehensive_config() -> Dict[str, Any]:
        """Get comprehensive configuration with both simple and structured patterns"""
        builder = RagConfigBuilder()
        
        # Add basic simple patterns
        basic_config = RagPresetConfigs.get_basic_config()
        builder.add_simple_base_patterns(basic_config['simple_patterns']['base_patterns'])
        builder.add_simple_in_patterns(basic_config['simple_patterns']['in_patterns'])
        builder.add_simple_related_patterns(basic_config['simple_patterns']['related_patterns'])
        
        # Add advanced structured patterns
        advanced_config = RagPresetConfigs.get_advanced_config()
        builder.add_structured_base_patterns(advanced_config['structured_patterns']['base_patterns'])
        builder.add_structured_in_patterns(advanced_config['structured_patterns']['in_patterns'])
        
        return builder.build()