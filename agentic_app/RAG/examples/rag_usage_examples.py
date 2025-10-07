"""
Example usage of the refactored RAG system

This file demonstrates how to use the new reusable classes for different scenarios.
"""

from files_handler.file_loader import FileLoader
from RAG.rag_factory import RagFactory, RagConfigBuilder, RagPresetConfigs
from RAG.get_query_pattern_by_object import (
    get_base_patterns, in_patterns, related_base_patterns,
    get_summary_pattern_dict, related_base_patterns_dict_structured, in_patterns_dict
)


def example_basic_usage():
    """Example of basic usage with the original RagCreator"""
    print("=== Basic Usage Example ===")
    
    # Create RAG creator (backward compatible)
    rag_creator = RagFactory.create_rag_creator()
    
    # Generate structured queries (main method)
    structured_queries = rag_creator.build_pattern()
    print(f"Generated {len(structured_queries)} structured queries")
    
    # Generate simple queries (legacy method)
    simple_queries = rag_creator.build_pattern1()
    print(f"Generated {len(simple_queries)} simple queries")
    
    # Generate all patterns
    all_results = rag_creator.build_all_patterns()
    print(f"Total: {all_results['total_all']} queries")


def example_configurable_usage():
    """Example of using the configurable RAG creator"""
    print("\n=== Configurable Usage Example ===")
    
    # Create configurable RAG creator
    file_loader = FileLoader()
    configurable_rag = RagFactory.create_configurable_rag_creator(file_loader)
    
    # Use preset configuration
    basic_config = RagPresetConfigs.get_basic_config()
    
    # Create simple queries
    simple_queries = configurable_rag.create_simple_queries(
        basic_config['simple_patterns'], 
        "example_simple_queries.json"
    )
    print(f"Generated {len(simple_queries)} simple queries")
    
    # Create structured queries with advanced config
    advanced_config = RagPresetConfigs.get_advanced_config()
    structured_queries = configurable_rag.create_structured_queries(
        advanced_config['structured_patterns'],
        "example_structured_queries.json"
    )
    print(f"Generated {len(structured_queries)} structured queries")


def example_custom_builder():
    """Example of creating custom query builders"""
    print("\n=== Custom Builder Example ===")
    
    # Create individual builders
    simple_builder = RagFactory.create_simple_query_builder(
        ["What is {Object}?", "Describe {ObjectPlural}"],
        ["in detail", "briefly"]
    )
    
    structured_builder = RagFactory.create_structured_query_builder(
        {
            "Analyze {Object} performance": {
                "type": "performance_analysis",
                "priority": "high"
            }
        },
        {
            "with charts": {"include_visualizations": True},
            "as report": {"format": "report"}
        }
    )
    
    # Use orchestrator to combine builders
    orchestrator = RagFactory.create_orchestrator()
    orchestrator.add_builder(simple_builder).add_builder(structured_builder)
    
    # Generate queries
    all_queries = orchestrator.generate_and_save("custom_queries.json")
    print(f"Generated {len(all_queries)} custom queries")


def example_pipeline_usage():
    """Example of using the pipeline architecture"""
    print("\n=== Pipeline Usage Example ===")
    
    # Create pipeline
    pipeline = RagFactory.create_pipeline()
    
    # Create simple pipeline
    simple_orchestrator = pipeline.create_simple_pipeline(
        get_base_patterns,
        in_patterns,
        related_base_patterns
    )
    
    simple_queries = simple_orchestrator.generate_and_save("pipeline_simple_queries.json")
    print(f"Pipeline generated {len(simple_queries)} simple queries")
    
    # Create structured pipeline
    structured_orchestrator = pipeline.create_structured_pipeline(
        get_summary_pattern_dict,
        in_patterns_dict,
        related_base_patterns_dict_structured
    )
    
    structured_queries = structured_orchestrator.generate_and_save("pipeline_structured_queries.json")
    print(f"Pipeline generated {len(structured_queries)} structured queries")


def example_config_builder():
    """Example of using the configuration builder"""
    print("\n=== Configuration Builder Example ===")
    
    # Build custom configuration
    config = RagConfigBuilder() \
        .add_simple_base_patterns([
            "What are the benefits of {Object}?",
            "How does {Object} work?",
            "Compare different {ObjectPlural}"
        ]) \
        .add_simple_in_patterns([
            "with examples",
            "in bullet points",
            "as a flowchart"
        ]) \
        .add_simple_related_patterns([
            "How do {ObjectPlural} integrate with {RelatedObject}?",
            "What's the relationship between {Object} and {RelatedObject}?"
        ]) \
        .add_structured_base_patterns({
            "Create {Object} documentation": {
                "type": "documentation",
                "format": "markdown",
                "sections": ["overview", "usage", "examples"]
            },
            "Generate {Object} test cases": {
                "type": "testing",
                "coverage": "comprehensive",
                "format": "automated"
            }
        }) \
        .add_structured_in_patterns({
            "with code examples": {
                "include_code": True,
                "language": "python"
            },
            "for beginners": {
                "complexity": "basic",
                "explanations": "detailed"
            }
        }) \
        .build()
    
    # Use the custom configuration
    configurable_rag = RagFactory.create_configurable_rag_creator()
    
    # Create hybrid queries
    hybrid_queries = configurable_rag.create_hybrid_queries(
        config['simple_patterns'],
        config['structured_patterns'],
        "hybrid_custom_queries.json"
    )
    print(f"Generated {len(hybrid_queries)} hybrid queries from custom config")


def example_advanced_orchestration():
    """Example of advanced orchestration with multiple builders"""
    print("\n=== Advanced Orchestration Example ===")
    
    # Create multiple specialized builders
    builders = [
        RagFactory.create_simple_query_builder(
            ["List {ObjectPlural}", "Show {Object} info"],
            ["concisely", "in detail"]
        ),
        RagFactory.create_related_query_builder(
            ["Connect {ObjectPlural} to {RelatedObject}"],
            ["with diagrams", "step by step"]
        ),
        RagFactory.create_structured_query_builder(
            {"Generate {Object} report": {"type": "report", "format": "pdf"}},
            {"with metrics": {"include_kpis": True}}
        ),
        RagFactory.create_structured_related_query_builder(
            {"Compare {ObjectPlural} with {RelatedObject}": {"type": "comparison"}},
            {"side by side": {"layout": "columns"}}
        )
    ]
    
    # Create orchestrator and add all builders
    orchestrator = RagFactory.create_orchestrator()
    orchestrator.add_builders(builders)
    
    # Show builder information
    orchestrator.print_builder_info()
    
    # Generate comprehensive queries
    comprehensive_queries = orchestrator.generate_and_save("comprehensive_queries.json")
    print(f"Generated {len(comprehensive_queries)} comprehensive queries")


if __name__ == "__main__":
    print("RAG System Examples")
    print("=" * 50)
    
    try:
        # Run all examples
        example_basic_usage()
        example_configurable_usage()
        example_custom_builder()
        example_pipeline_usage()
        example_config_builder()
        example_advanced_orchestration()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()