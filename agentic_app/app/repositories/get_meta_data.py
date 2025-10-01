from typing import Any, Dict, List
from files_handler.file_loader import FileLoader


class MetaDataRepository:

    def __init__(self):
        self.loader = FileLoader()

    def get_meta_data(self) -> List[Dict[str, Any]]:
        """Load all fields from the __local__ JSON file

        Returns:
            List[Dict[str, Any]]: List of object dictionaries with relevant fields
        """
        try:
            meta_data = self.loader.load_json_file_from_output("grouped_fields.json")
            print(f"Successfully fetched {len(meta_data)} grouped_fields")

            return meta_data if meta_data else None

        except Exception as e:
            print(f"Error fetching grouped_fields: {e}")
            return None
