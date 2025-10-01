from repositories.get_objects_repository import ObjectRepository
from files_handler.file_loader import FileLoader
from typing import List, Any

class ObjectService:
    def __init__(self):
        self.repository = ObjectRepository()
        self.loader = FileLoader()

    def get_objects_base(self) -> List[Any]:
        try:
            result = self.repository.get_objects()
            # Save the result to JSON file using the correct method name
            self.loader.save_files_at_orignal("objects.json", result)
            return result
        except Exception as e:
            print(f"Error in ObjectService.get_objects: {e}")
            return []
        
        
    def get_objects(self) -> List[Any]:
        
        result = self.get_objects_base()
            
        return result