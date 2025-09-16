    
from src.utility.load_meta_data_files import LoadFiles
from typing import Dict, Any
from src.interfaces.response_model import ResponseModel

class MetaDataUtility:

    def __init__(self, folder_path: str = "./memory_db/orignal", output_path: str = "./memory_db/db"):
        self.folder_path = folder_path
        self.output_path = output_path
        self.originalData: Dict[str, Any] = self.get_original_data()

    # Static method to get original data
    def get_original_data(self):
        file_loader = LoadFiles(self.folder_path)
        data = file_loader.get_data()
        for fname in ["objects.json", "fields.json", "layouts.json", "roles.json", "system_fields.json"]:
            content = data.get(fname)
            if content is not None and content != {}:
                file_loader.save_files(fname, self.output_path, content)
        return data
        
    # Static method to get original data
    def get_fields_from_src(self, file_name: str) -> ResponseModel:
        file_loader = LoadFiles(self.folder_path)
        data = file_loader.get_data()
        fname = file_name
        content = data.get(fname)
        
        return content
    
        # Static method to get original data
    def get_fields_from_db(self, file_name: str) -> ResponseModel:
        file_loader = LoadFiles(self.output_path)
        data = file_loader.get_data()
        fname = file_name
        content = data.get(fname)
        
        return content
    
    
    # Static method to get original data
    def save_fields_at_db(self, fieldName: str, content: Any):
        file_loader = LoadFiles(self.folder_path)
        if content is not None and content != {}:
            file_loader.save_files(fieldName, self.output_path, content)
        print("Content saved.")
        
    # Method to return the original data
    @staticmethod
    def get_data() -> Dict[str, Any]:
        return MetaDataUtility().originalData