from files_handler.file_loader import FileLoader
from pydantic import BaseModel

#  {
#         "ObjectId": 6,
#         "ObjectName": "Lead",
#         "FieldId": -10057739,
#         "FieldName": "TerritoryType",
#         "Label": "SN_Lead_TerritoryType",
#         "ViewLabel": "SN_View_Lead_TerritoryType",
#         "FieldType": "Number",
#         "IsFilterable": false,
#         "FieldTableName": "Leads",
#         "LayoutFieldId": ""
#     },


class FieldData(BaseModel):
    roleid: int
    object_name: str
    name: str
    FieldName: str
    field_type: str

class BaseFieldTool:
    
    def __init__(self):
        self.file_loader = FileLoader()
    
    def load_field_files(self) -> dict:
        """Load all JSON files from the folder."""
        return self.file_loader.loadJsonFile("fields.json")
    
    
    def get_field_by_field_name_and_object(self, field_name: int, object_name: str) -> list[FieldData]:
        """Get fields by role ID and object name."""
        all_fields = self.load_field_files()
        filtered_fields = [
            FieldData(
                roleid=field.get("RoleId", 1),
                object_name=field.get("ObjectName", ""),
                name=field.get("Label", ""),
                FieldName=field.get("FieldName", ""),
                field_type=field.get("FieldType", "")
            )
            for field in all_fields
            if field.get("FieldName", None) == field_name and field.get("ObjectName", "").lower() == object_name.lower()
        ]
        return filtered_fields
    
    def get_field_by_object_name(self, object_name: str) -> list[FieldData]:
        """Get fields by role ID and object name."""
        all_fields = self.load_field_files()
        filtered_fields = [
            FieldData(
                roleid=field.get("RoleId", 1),
                object_name=field.get("ObjectName", ""),
                name=field.get("Label", ""),
                FieldName=field.get("FieldName", ""),
                field_type=field.get("FieldType", "")
            )
            for field in all_fields
            if field.get("ObjectName", "").lower() == object_name.lower()
        ]
        return filtered_fields

    def get_field_by_object_name_and_label(self, object_name: str, label: str) -> list[FieldData]:
        """Get fields by role ID, object name, and label."""
        all_fields = self.load_field_files()
        filtered_fields = [
            FieldData(
                roleid=field.get("RoleId", 1),
                object_name=field.get("ObjectName", ""),
                name=field.get("Label", ""),
                FieldName=field.get("FieldName", ""),
                field_type=field.get("FieldType", "")
            )
            for field in all_fields
            if field.get("ObjectName", "").lower() == object_name.lower() and field.get("Label", "").lower() == label.lower()
        ]
        return filtered_fields