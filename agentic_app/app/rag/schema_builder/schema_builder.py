from typing import Any
from warnings import filters
from rag.patterns.get_patterns import get_patterns
from rag.schema_builder.load_output_files import LoadOutputFiles
from rag.schema_builder.set_metadata import SetMetadata


class SchemaBuilder:
    def __init__(self):
        self.get_patterns = get_patterns
        self.repository = LoadOutputFiles()
        self.metadata = SetMetadata()

    def prepare_query(self, pattern: str, document: Any) -> str:
        # Implement the logic to prepare a query based on the pattern and document
        # This is a placeholder implementation
        query = document.get("query_label", "")
        if query:
            return f"{pattern.get('prefix', '')} {query} {pattern.get('suffix', '')}"
        return query

    def prepare_metadata(self, document: Any, pattern: dict) -> dict:
        # Implement the logic to prepare metadata based on the pattern and document
        # This is a placeholder implementation
        datafield = document.get("query_fields", {})
        
        metadata = self.metadata.set_metadata(
            intent=pattern.get("intent", "GET"),
            output_format=pattern.get("output_format", "TABLE"),
            data_fields=datafield,
            limit=pattern.get("limit", 10),
            filters=pattern.get("filters", []),
            order_field=pattern.get("order_field", {}),
            order_direction=pattern.get("order_direction", "ASC"),
            group_by_fields=pattern.get("group_by_fields", []),
            docstring=pattern.get("docstring", "")
        )

        return metadata

    def prepare_document(self, pattern: str, document: Any) -> dict:
        query = self.prepare_query(pattern, document)
        metadata = self.prepare_metadata(document, pattern)

        return {"query": query, "meta_data": metadata}

    def create_files_by_data(
        self, get_queries, documents, full_count, data_type
    ):
        try:
            content = []
            count = 0
            if get_queries and documents:
                for pattern in get_queries:
                    for doc in documents:
                        document = self.prepare_document(pattern, doc)
                        count += 1
                        full_count += 1
                        content.append(document)

                        if count >= 100:
                            self.repository.save_file_at_rag_output(
                                f"rag_file_{full_count//100}_{data_type}_{pattern['intent'].lower()}.json",
                                content,
                            )
                            content = []
                            count = 0

        except Exception as e:
            print(f"Error loading listing files: {e}")
            return []

    def get_table_patterns(self):
        try:
            get_queries = self.get_patterns.get("get_table", [])
            listings = self.repository.get_all_layouts_and_listings()
            full_count = 0
            
            self.create_files_by_data(
                get_queries, listings, full_count, "listings"
            )

        except Exception as e:
            print(f"Error loading listing files: {e}")
            return []

    def get_detail_patterns(self):
        try:
            get_queries = self.get_patterns.get("get_detail", [])
            layout_fields = self.repository.load_layout_fields_file()
            full_count = 0
            
            self.create_files_by_data(
                get_queries, layout_fields, full_count, "fields"
            )

        except Exception as e:
            print(f"Error loading listing files: {e}")
            return []
        
        
    def show_top_patterns(self):
        try:
            get_queries = self.get_patterns.get("show_top", [])
            listings = self.repository.get_all_layouts_and_listings()
            full_count = 0
            
            self.create_files_by_data(
                get_queries, listings, full_count, "show_top_listings"
            )

        except Exception as e:
            print(f"Error loading listing files: {e}")
            return []
        
    def show_card_patterns(self):
        try:
            get_queries = self.get_patterns.get("get_card", [])
            listings = self.repository.get_all_layouts_and_listings()
            full_count = 0
            
            self.create_files_by_data(
                get_queries, listings, full_count, "show_card_listings"
            )

        except Exception as e:
            print(f"Error loading listing files: {e}")
            return []
        
    def show_bullet_patterns(self):
        try:
            get_queries = self.get_patterns.get("get_bullet", [])
            listings = self.repository.get_all_layouts_and_listings()
            full_count = 0
            
            self.create_files_by_data(
                get_queries, listings, full_count, "show_bullet_listings"
            )

        except Exception as e:
            print(f"Error loading listing files: {e}")
            return []
    
    def show_summarize_patterns(self):
        try:
            get_queries = self.get_patterns.get("get_summarized", [])
            listings = self.repository.get_all_layouts_and_listings()
            full_count = 0
            
            self.create_files_by_data(
                get_queries, listings, full_count, "show_summarized_listings"
            )

        except Exception as e:
            print(f"Error loading listing files: {e}")
            return []
        
        
    
    def build_rag(self):
        try:
            self.get_table_patterns()
            self.get_detail_patterns()
            self.show_top_patterns()
            self.show_card_patterns()
            self.show_bullet_patterns()
            self.show_summarize_patterns()

        except Exception as e:
            print(f"Error loading listing files: {e}")
            return []
