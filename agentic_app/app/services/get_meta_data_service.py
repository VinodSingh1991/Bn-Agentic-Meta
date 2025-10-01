from repositories.get_meta_data import MetaDataRepository
from services.get_layouts_service import LayoutService
from files_handler.file_loader import FileLoader
from typing import List, Any

class MetaDataService:
    def __init__(self):
        self.repository = MetaDataRepository()
        self.loader = FileLoader()
        self.service = LayoutService()

    def get_meta_data_by_role_id(self, role_id: str) -> List[Any]:
        try:
            result = self.repository.get_meta_data()
            
            if result:
                return result[role_id] if role_id in result else {}
            return {}
        except Exception as e:
            print(f"Error in MetaDataService.get_meta_data_by_role_id: {e}")
            return {}


    def get_objects_meta_data_by_object_name(self, role_id, object_id: str) -> List[Any]:
        try:
            result = self.get_meta_data_by_role_id(role_id)
            if result and object_id:
                filtered_result = result[object_id]
                return filtered_result
            return []
        except Exception as e:
            print(f"Error in get_objects_meta_data_by_object_name: {e}")
            return []
