import json
from typing import Dict, Any, Optional
from .file_reader import FileReader
import os

class FileLoader:
    def __init__(self, folder_path: str = None, output_path: str = None):
        if folder_path is None:
            # Get the absolute path to the _local_db_/orignal_files directory
            # This assumes the current file is in app/files_handler/
            current_dir = os.path.dirname(os.path.abspath(__file__))
            app_dir = os.path.dirname(current_dir)  # Go up to app directory
            self.folder_path = os.path.join(app_dir, "_local_db_", "orignal_files")
            self.output_path = os.path.join(app_dir, "_local_db_", "output_files")
        else:
            self.folder_path = folder_path
            self.output_path = output_path
        
        # Ensure the directory exists
        os.makedirs(self.folder_path, exist_ok=True)
        os.makedirs(self.output_path, exist_ok=True)
        self.data: Dict[str, Any] = {}

    # Load all JSON files in the folder
    def load_json_files(self) ->  Dict[str, Any]:
        """
        Load all JSON files in the folder.
        The key will be the filename, and the value will be the JSON content.
        """
        
        # Check if the folder exists
        if not os.path.exists(self.folder_path):
            print(f"Warning: Folder path does not exist: {self.folder_path}")
            return self.data
        
        if not os.path.isdir(self.folder_path):
            print(f"Warning: Path is not a directory: {self.folder_path}")
            return self.data
        
        try:
            folder_dir = os.listdir(self.folder_path)
            file_loader = FileReader()

            for filename in folder_dir:
                if filename.endswith('.json'):
                    file_path = os.path.join(self.folder_path, filename)
                    json_data = file_loader.read_json(file_path)
                    if json_data is not None:
                        self.data[filename] = json_data
                        print(f"Loaded JSON file: {filename}")
                    else:
                        print(f"Failed to load JSON file: {filename}")
                        
        except OSError as e:
            print(f"Error accessing directory {self.folder_path}: {e}")
        except Exception as e:
            print(f"Unexpected error loading JSON files: {e}")
            
        return self.data

    def loadJsonFile(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load a specific JSON file from the folder."""
        file_path = os.path.join(self.folder_path, filename)
        file_loader = FileReader()
        json_data = file_loader.read_json(file_path)
        if json_data is not None:
            print(f"Loaded JSON file: {filename}")
            return json_data
        else:
            print(f"Failed to load JSON file: {filename}")
            return None
        
    def load_json_file_from_output(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load a specific JSON file from the folder."""
        file_path = os.path.join(self.output_path, filename)
        file_loader = FileReader()
        json_data = file_loader.read_json(file_path)
        if json_data is not None:
            print(f"Loaded JSON file: {filename}")
            return json_data
        else:
            print(f"Failed to load JSON file: {filename}")
            return None
    # Save files to the folder
    def save_files_at_output(self, filename: str, content: Any) -> None:
        os.makedirs(self.output_path, exist_ok=True)
        file_path = os.path.join(self.output_path, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            if filename.endswith('.json'):
                json.dump(content, file, ensure_ascii=False, indent=4)
            elif filename.endswith('.txt'):
                file.write(content)
            else:
                print("Unsupported file format.")
                return
    
    # Save files to the folder
    def save_files_at_orignal(self, filename: str, content: Any) -> None:
        os.makedirs(self.folder_path, exist_ok=True)
        file_path = os.path.join(self.folder_path, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            if filename.endswith('.json'):
                json.dump(content, file, ensure_ascii=False, indent=4)
            elif filename.endswith('.txt'):
                file.write(content)
            else:
                print("Unsupported file format.")
                return
            
    # Get the loaded data
    def get_file_data(self) -> Dict[str, Any]:
        self.load_json_files()
        return self.data
    