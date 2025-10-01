from repositories.get_roles_repository import RoleRepository
from files_handler.file_loader import FileLoader
from typing import List, Any

class RoleService:
    def __init__(self):
        self.repository = RoleRepository()
        self.loader = FileLoader()

    def get_roles_base(self) -> List[Any]:
        try:
            result = self.repository.get_roles()
            # Save the result to JSON file using the correct method name
            self.loader.save_files_at_orignal("roles.json", result)
            return result
        except Exception as e:
            print(f"Error in RoleService.get_roles: {e}")
            return []
        
    def get_roles(self) -> List[Any]:
        
        result = self.get_roles_base()
        return result