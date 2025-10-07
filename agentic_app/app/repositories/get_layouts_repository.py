from typing import Any, Dict, List
from database.connection import DatabaseConnection
from database.query_helper import QueryHelper
from enum_helper.field_type import field_type_inverted
from enum_helper.object_list import object_list
from files_handler.file_loader import FileLoader


class LayoutRepository:

    def __init__(self):
        self.db = DatabaseConnection()
        self.loader = FileLoader()

    def get_field_type_by_id(self, field_id: int) -> str:
        """Get the field type from the field_type_inverted enum by field ID"""

        return field_type_inverted.get(field_id, "UnknownField")

    def get_object_enum_by_object_id(self, object_id: int) -> str:
        """Get the object name from the object_list enum by object ID"""

        return object_list.get(object_id, "UnknownObject")

    def get_layout_group(self) -> List[Dict[str, Any]]:
        """Get all layouts from the LayoutGroupView table

        Returns:
            List[Dict[str, Any]]: List of object dictionaries with relevant fields
        """
        try:
            # Use direct query since QueryHelper might not be available
            layout_data = self.db.execute_query(QueryHelper.GetLayoutGroupView)

            # Convert tuples to dictionaries for better handling
            layouts = []
            for obj in layout_data:
                # Column names: ItemTypeID, LayoutID, LayoutType, LayoutXML
                layouts.append(
                    {
                        "ItemTypeID": obj.ItemTypeID,
                        "LayoutID": obj.LayoutID,
                        "LayoutType": obj.LayoutType,
                        "LayoutXML": obj.LayoutXML,
                    }
                )

            print(f"Successfully fetched {len(layouts)} layouts")
            return layouts

        except Exception as e:
            print(f"Error fetching layouts: {e}")
            return []
        
    
    def get_layout_ui_master(self) -> List[Dict[str, Any]]:
        """Get all layouts from the GetLayoutUIMaster table

        Returns:
            List[Dict[str, Any]]: List of object dictionaries with relevant fields
        """
        try:
            # Use direct query since QueryHelper might not be available
            layout_data = self.db.execute_query(QueryHelper.GetLayoutUIMaster)

            # Convert tuples to dictionaries for better handling
            layouts = []
            for obj in layout_data:
                # Column names: ItemTypeID, LayoutID, LayoutType, LayoutXML
                layouts.append(
                    {
                        "ItemTypeID": obj.ItemTypeID,
                        "LayoutID": obj.LayoutID,
                        "UIName": obj.Name
                    }
                )

            print(f"Successfully fetched {len(layouts)} layouts")
            return layouts

        except Exception as e:
            print(f"Error fetching layouts: {e}")
            return []  
        
    def get_layout_role_mapping(self) -> List[Dict[str, Any]]:
        """Get all layouts from the GetLayoutUIMaster table

        Returns:
            List[Dict[str, Any]]: List of object dictionaries with relevant fields
        """
        try:
            # Use direct query since QueryHelper might not be available
            layout_data = self.db.execute_query(QueryHelper.GetLayoutGroupRoleMapping)

            # Convert tuples to dictionaries for better handling
            layouts = []
            for obj in layout_data:
                # Column names: ItemTypeID, LayoutID, LayoutType, LayoutXML
                layouts.append(
                    {
                        "LayoutId": obj.LayoutId,
                        "RoleId": obj.RoleId
                    }
                )

            print(f"Successfully fetched {len(layouts)} layouts")
            return layouts

        except Exception as e:
            print(f"Error fetching layouts: {e}")
            return []  
        
    def get_layouts_file(self, file) -> List[Dict[str, Any]]:
        """Load all fields from the __local__ JSON file

        Returns:
            List[Dict[str, Any]]: List of object dictionaries with relevant fields
        """
        try:
            layouts = self.loader.loadJsonLayoutFile(file)
            print(f"Successfully fetched {len(layouts)} layouts")

            return layouts if layouts else []

        except Exception as e:
            print(f"Error fetching layouts: {e}")
            return []
