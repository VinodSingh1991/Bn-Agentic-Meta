import json
from typing import Dict, Any, Optional
from .file_loader import FileLoader
import os

class LoadFiles:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.data: Dict[str, Any] = {}

    # Load all JSON files in the folder
    def load_all_json(self) ->  Dict[str, Any]:
        """
        Load all JSON files in the folder.
        The key will be the filename, and the value will be the JSON content.
        """
        
        folder_dir = os.listdir(self.folder_path)
        file_loader = FileLoader()

        for filename in folder_dir:
            if filename.endswith('.json'):
                file_path = os.path.join(self.folder_path, filename)
                json_data = file_loader.load_json(file_path)
                if json_data is not None:
                    self.data[filename] = json_data

    # Save files to the folder
    def save_files(self, filename: str, output_path: str, content: Any) -> None:
        os.makedirs(output_path, exist_ok=True)
        file_path = os.path.join(output_path, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            if filename.endswith('.json'):
                json.dump(content, file, ensure_ascii=False, indent=4)
            elif filename.endswith('.txt'):
                file.write(content)
            else:
                print("Unsupported file format.")
    # Get the loaded data
    def get_data(self) -> Dict[str, Any]:
        self.load_all_json()
        return self.data