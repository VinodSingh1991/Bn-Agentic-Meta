import json
import csv
from typing import List, Dict, Any, Optional

class FileLoader:
    @staticmethod
    def load_json(file_path: str) -> Optional[Dict[str, Any]]:
        """Load a JSON file and return its content as a dictionary."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading JSON file: {e}")
            return None

    @staticmethod
    def load_csv(file_path: str) -> Optional[List[Dict[str, Any]]]:
        """Load a CSV file and return its content as a list of dictionaries."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return [row for row in reader]
        except FileNotFoundError as e:
            print(f"Error loading CSV file: {e}")
            return None
    
    @staticmethod
    def load_text(file_path: str) -> Optional[str]:
        """Load a text file and return its content as a string."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError as e:
            print(f"Error loading text file: {e}")
            return None
