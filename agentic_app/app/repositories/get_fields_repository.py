
from typing import Any, Dict, List
from database.connection import DatabaseConnection
from database.query_helper import QueryHelper
from enum_helper.field_type import field_type_inverted
from enum_helper.object_list import object_list
from files_handler.file_loader import FileLoader

class FieldsRepository:
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.loader = FileLoader()
        
    def get_field_type_by_id(self, field_id: int) -> str:
        """Get the field type from the field_type_inverted enum by field ID"""

        return field_type_inverted.get(field_id, "UnknownField")
    
    def get_object_enum_by_object_id(self, object_id: int) -> str:
        """Get the object name from the object_list enum by object ID"""

        return object_list.get(object_id, "UnknownObject")

    def get_fields(self) -> List[Dict[str, Any]]:
        """Get all fields from the FieldMasterTableList table

        Returns:
            List[Dict[str, Any]]: List of object dictionaries with relevant fields
        """
        try:
            # Use direct query since QueryHelper might not be available
            fields_data = self.db.execute_query(QueryHelper.GetSystemFields)

            # Convert tuples to dictionaries for better handling
            fields = []
            for obj in fields_data:
                # Column names: OwnerId, RoleId, Name
                field_type = self.get_field_type_by_id(obj.Type)
                object_name = self.get_object_enum_by_object_id(obj.KeyId)

                if object_name == "UnknownObject" or field_type == "UnknownField":
                    continue
                
                obj_dict = {
                    "ObjectId": obj.KeyId,
                    "ObjectName": object_name,
                    "FieldId": obj.FieldId,
                    "FieldName": obj.FieldName,
                    "Label": obj.Label,
                    "ViewLabel": obj.ViewLabel,
                    "FieldType": field_type,
                    "IsFilterable": obj.IsFilterable,
                    "FieldTableName": obj.TableName,
                    "LayoutFieldId": obj.LayoutFieldId
                }
                fields.append(obj_dict)

            print(f"Successfully fetched {len(fields)} fields_data")
            return fields

        except Exception as e:
            print(f"Error fetching fields: {e}")
            return []

    def get_layouts_fields(self) -> List[Dict[str, Any]]:
        """Load all fields from the __local__ JSON file

        Returns:
            List[Dict[str, Any]]: List of object dictionaries with relevant fields
        """
        try:
            layouts_fields = self.loader.load_json_file_from_output("layouts_fields.json")
            #print(f"Successfully fetched {len(layouts_fields)} layouts")

            return layouts_fields if layouts_fields else []

        except Exception as e:
            print(f"Error fetching layouts: {e}")
            return []
        

