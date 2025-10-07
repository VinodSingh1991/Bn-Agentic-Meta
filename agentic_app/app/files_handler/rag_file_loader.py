import json
from typing import Dict, Any, Optional
from .file_reader import FileReader
import os


class RagFileLoader:
    def __init__(
        self,
        output_path: str = None,
        output_path_rag: str = None,
        
    ):
        if output_path is None:
            # Get the absolute path to the _local_db_/orignal_files directory
            # This assumes the current file is in app/files_handler/
            current_dir = os.path.dirname(os.path.abspath(__file__))
            app_dir = os.path.dirname(current_dir)  # Go up to app directory

            self.output_path = os.path.join(app_dir, "_local_db_", "output_files")
            self.original_path_layouts = os.path.join(
                app_dir, "_local_db_", "output_files/layouts"
            )
            self.rag_output_path = os.path.join(
                app_dir, "_local_db_", "rag_output_files"
            )
        else:
            self.output_path = output_path
            self.rag_output_path = output_path_rag
        # Ensure the directory exists
        os.makedirs(self.output_path, exist_ok=True)
        os.makedirs(self.rag_output_path, exist_ok=True)

        self.data: Dict[str, Any] = {}

    # Load all JSON files in the folder
    def load_all_layout_files_at_output(self) -> Dict[str, Any]:
        """
        Load all JSON files in the folder.
        The key will be the filename, and the value will be the JSON content.
        """

        # Check if the folder exists
        if not os.path.exists(self.original_path_layouts):
            print(f"Warning: Folder path does not exist: {self.original_path_layouts}")
            return self.data

        if not os.path.isdir(self.original_path_layouts):
            print(f"Warning: Path is not a directory: {self.original_path_layouts}")
            return self.data

        try:
            folder_dir = os.listdir(self.original_path_layouts)
            file_loader = FileReader()

            for filename in folder_dir:
                if filename.endswith(".json"):
                    file_path = os.path.join(self.original_path_layouts, filename)
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


    def load_file_at_output(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load a specific JSON file from the folder."""
        file_path = os.path.join(self.output_path, filename)
        file_loader = FileReader()
        json_data = file_loader.read_json(file_path)
        if json_data is not None:
            #print(f"Loaded JSON file: {filename}")
            return json_data
        else:
            print(f"Failed to load JSON file: {filename}")
            return None

    # Save files to the folder
    def save_files_at_rag_output(self, filename: str, content: Any) -> None:
        os.makedirs(self.rag_output_path, exist_ok=True)
        file_path = os.path.join(self.rag_output_path, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            if filename.endswith(".json"):
                json.dump(content, file, ensure_ascii=False, indent=4)
            elif filename.endswith(".txt"):
                file.write(content)
            else:
                print("Unsupported file format.")
                return
            
    def load_all_files_from_rag_output(self) -> Dict[str, Any]:
        """
        Load all JSON files in the folder.
        The key will be the filename, and the value will be the JSON content.
        """

        # Check if the folder exists
        if not os.path.exists(self.rag_output_path):
            print(f"Warning: Folder path does not exist: {self.rag_output_path}")
            return self.data

        if not os.path.isdir(self.rag_output_path):
            print(f"Warning: Path is not a directory: {self.rag_output_path}")
            return self.data

        try:
            folder_dir = os.listdir(self.rag_output_path)
            file_loader = FileReader()

            for filename in folder_dir:
                if filename.endswith(".json"):
                    file_path = os.path.join(self.rag_output_path, filename)
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
    
    def load_all_rag_files(self):
        try:
            all_rags = []
            layouts = self.load_all_files_from_rag_output()
            if layouts:
                for layout in layouts.values():
                    if isinstance(layout, list):
                        all_rags.extend(layout)
                    else:
                        all_rags.append(layout)
            return all_rags                                                         
        except Exception as e:
            print(f"Error loading RAG files: {e}")
            return []