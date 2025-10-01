from typing import Any, Dict, List
from files_handler.file_loader import FileLoader
from database.connection import DatabaseConnection
from database.query_helper import QueryHelper
from enum_helper.object_list import object_list

class ObjectRepository:
    
    def __init__(self):
        self.db = DatabaseConnection()
        
    def get_object_enum_by_object_id(self, object_id: int) -> str:
        """Get the object name from the object_list enum by object ID"""

        return object_list.get(object_id, "UnknownObject")

    def get_objects(self) -> List[Dict[str, Any]]:
        """Get all objects from the ObjectMasterTableList table

        Returns:
            List[Dict[str, Any]]: List of object dictionaries with relevant fields
        """
        try:
            # Use direct query since QueryHelper might not be available
            objects_data = self.db.execute_query(QueryHelper.GetObjects)

            # Convert tuples to dictionaries for better handling
            objects = []
            for obj in objects_data:
                # Column names: OwnerId, RoleId, Name
                object_name = self.get_object_enum_by_object_id(obj.ItemType)
                
                if object_name == "UnknownObject":
                    continue
                
                obj_dict = {
                    "ObjectId": obj.ItemType,
                    "ObjectName": object_name,
                    "ObjectTableName": obj.TableName,
                    "ObjectOwnerField": obj.OwnerField,
                    "ObjectTablePrimaryKey": obj.PrimaryField,
                    "ObjectSubjectField": obj.SubjectField
                }
                objects.append(obj_dict)

            print(f"Successfully fetched {len(objects)} objects")
            return objects
            
        except Exception as e:
            print(f"Error fetching objects: {e}")
            return []
