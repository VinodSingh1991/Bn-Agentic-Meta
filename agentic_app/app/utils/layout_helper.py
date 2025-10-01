from utils.xml_reader import XMLReader
from repositories.get_layouts_repository import LayoutRepository
from files_handler.file_loader import FileLoader
from typing import List, Any, Dict, Optional


class LayoutHelper:
    def __init__(self):
        self.repository = LayoutRepository()
        self.loader = FileLoader()
        self.reader = XMLReader()

    def get_field_from_xml(self, layout_xml: str, role_id: int) -> Optional[str]:

        root = self.reader.read_xml_string(layout_xml)

        xml_data = {}
        
        if root:
            cols = self.reader.find_elements(root, "col")
            for col in cols:
                field = {}
                field_id = self.reader.get_element_attribute(col, "fieldid")

                if field_id == "blankcell":
                    continue

                field['name'] = self.reader.get_element_attribute(col, "name")
                field['id'] = self.reader.get_element_attribute(col, "fieldid")
                field['relatedtype'] = self.reader.get_element_attribute(col, "relatedtype")
                field['listingtype'] = self.reader.get_element_attribute(col, "listingtype")
                field['listingid'] = self.reader.get_element_attribute(col, "listingid")
                field['fieldtype'] = self.reader.get_element_attribute(col, "fieldtype")
                field['roleid'] = role_id

                xml_data[field_id] = field
        
        return xml_data

    def get_layout_fields_by_layout_id(self, layout_id: Any, object_id: Any) -> Optional[Dict[str, Any]]:
        """
        Get layout fields for a specific layout ID

        Args:
            layout_id: The layout ID to search for
        Returns:
            Optional[Dict[str, Any]]: The layout fields dictionary or None if not found
        """
        try:
            layout = self.get_layouts_by_itemtype_id(object_id)
        
            if layout:
                return layout.get("LayoutFields", None)
            return None
        except Exception as e:
            print(f"Error getting layout fields by layout ID {layout_id}: {e}")
            return None
    
    def get_layouts_by_itemtype_id(self, object_id: Any, layouts: Any) -> Optional[Dict[str, Any]]:
        """
        Get a specific layout by item type ID

        Args:
            layout_id: The layout ID to search for
            
        Returns:
            Optional[Dict[str, Any]]: The layout dictionary or None if not found
        """
        try:
            all_layouts = layouts
            return [
                layout for layout in all_layouts 
                if layout.get("ItemTypeID") == object_id
            ]
        except Exception as e:
            print(f"Error getting layout by item type ID {object_id}: {e}")
            return None
    
    def get_layouts_by_role(self, role_id: Any, layouts: Any) -> List[Dict[str, Any]]:
        """
        Get all layouts for a specific role
        
        Args:
            role_id: The role ID to filter by
            
        Returns:
            List[Dict[str, Any]]: List of layouts for the specified role
        """
        try:
            all_layouts = layouts
            return [
                layout for layout in all_layouts 
                if layout.get("RoleId") == role_id
            ]
        except Exception as e:
            print(f"Error getting layouts by role {role_id}: {e}")
            return []
        
        
    def build_layout_fields(self, layouts):
        layout_fields = {}
        if layouts: 
            for item in layouts:
                fields = item.get("LayoutFields", [])
                if fields:  
                    for key, field in fields.items():
                        if key not in layout_fields:
                            # Create new field entry
                            new_field = {
                                "Name": field.get("name"),
                                "Id": field.get("id"),
                                "RelatedType": field.get("relatedtype"),
                                "ListingType": field.get("listingtype"),
                                "ListingId": field.get("listingid"),
                                "FieldType": field.get("fieldtype"),
                                "RoleIds": [field.get("roleid")] if field.get("roleid") else [],
                                "Synonyms": [field.get("name")] if field.get("name") else []
                            }
                            layout_fields[key] = new_field
                        else:
                            # Update existing entry
                            existing_field = layout_fields[key]

                            # Add RoleId (avoid duplicates)
                            roleid = field.get("roleid")
                            if roleid and roleid not in existing_field["RoleIds"]:
                                existing_field["RoleIds"].append(roleid)

                            # Add synonym (avoid duplicates)
                            name = field.get("name")
                            if name and name not in existing_field["Synonyms"]:
                                existing_field["Synonyms"].append(name)

        return layout_fields

    def get_field_from_xml_query_info(self, layout_xml: str) -> Optional[str]:

        root = self.reader.read_xml_string(layout_xml)

        xml_data = []
        
        if root:
            fields = self.reader.find_elements(root, "selectfield")
            for col in fields:

                xml_data.append(self.reader.get_element_attribute(col, "fieldname"))
        
        return xml_data