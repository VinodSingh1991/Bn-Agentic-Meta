from enum_helper.object_list import object_list 
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

                field["name"] = self.reader.get_element_attribute(col, "name")
                field["id"] = self.reader.get_element_attribute(col, "fieldid")
                field["relatedtype"] = self.reader.get_element_attribute(
                    col, "relatedtype"
                )
                field["listingtype"] = self.reader.get_element_attribute(
                    col, "listingtype"
                )
                field["listingid"] = self.reader.get_element_attribute(col, "listingid")
                field["fieldtype"] = self.reader.get_element_attribute(col, "fieldtype")
                field["roleid"] = role_id

                xml_data[field_id] = field

        return xml_data

    def get_layout_fields_by_layout_id(
        self, layout_id: Any, object_id: Any
    ) -> Optional[Dict[str, Any]]:
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

    def get_layouts_by_itemtype_id(
        self, object_id: Any, layouts: Any
    ) -> Optional[Dict[str, Any]]:
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
                layout
                for layout in all_layouts
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
            return [layout for layout in all_layouts if layout.get("RoleId") == role_id]
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
                                "RoleIds": (
                                    [field.get("roleid")] if field.get("roleid") else []
                                ),
                                "Synonyms": (
                                    [field.get("name")] if field.get("name") else []
                                ),
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

    def get_object_enum_by_object_id(self, object_id: int) -> str:
        """Get the object name from the object_list enum by object ID"""

        return object_list.get(object_id, "UnknownObject")

    def get_tab_labels(self, tab: str, obj_name: str) -> str:
        text = self.reader.find_elements(tab, "text", direct_child_only=True)

        if text and len(text) > 0:
            label = self.reader.find_elements(text[0], "lang", direct_child_only=True)

            if label and len(label) > 0:
                txt = self.reader.get_element_attribute(label[0], "text")
                return f"{obj_name} {txt}" if txt else None

        return None

    def get_section_labels(self, tab: str) -> Optional[List[str]]:
        pass

    def get_fields_from_tab(self, tab: str, all_field: Dict[str, Any], obj_name: str, layout_fields: List[Dict[str, Any]]) -> Optional[List[str]]:
        xml_data = []

        if tab:
            cols = self.reader.find_elements(tab, "col")
            for col in cols:
                field = {}
              
                field_id = self.reader.get_element_attribute(col, "fieldid")
                field_type = self.reader.get_element_attribute(col, "fieldtype")
                
                if field_id == "blankcell" or field_type == 40 or field_type == "40":
                    continue

                # Find field object by matching LayoutFieldId
                base_field = self.get_field_by_layout_field_id(all_field, field_id)
                
                
                #field["layout_id"] = self.reader.get_element_attribute(col, "fieldid")
                # field["relatedtype"] = self.reader.get_element_attribute(
                #     col, "relatedtype"
                # )
                # field["listingtype"] = self.reader.get_element_attribute(
                #     col, "listingtype"
                # )
                # field["listingid"] = self.reader.get_element_attribute(col, "listingid")
                # field["fieldtype"] = self.reader.get_element_attribute(col, "fieldtype")
                field["roleid"] = 1
                field["object_name"] = obj_name
                # Add base field information if found
                if base_field:
                    field["field_id"] = base_field.get("FieldId")
                    field["name"] = self.reader.get_element_attribute(col, "name")
                    field["FieldName"] = base_field.get("FieldName")
                    field["field_type"] = base_field.get("FieldType", "Text")
                    # Use Label from base field if name is empty
                    if not field["name"]:
                        field["name"] = base_field.get("Label")

                    xml_data.append(field)
                    layout_fields.append({
                        "query_label": f"{obj_name} {field['name']}",
                        "query_fields": [field]
                    })

        return xml_data

    def get_field_by_layout_field_id(self, all_fields: Dict[str, Any], layout_field_id: str) -> Optional[Dict[str, Any]]:
        try:
            # Handle if all_fields is a list
            if isinstance(all_fields, list):
                for field in all_fields:
                    if isinstance(field, dict) and field.get("LayoutFieldId") == layout_field_id:
                        return field
            
            return None
            
        except Exception as e:
            print(f"Error finding field by layout field ID {layout_field_id}: {e}")
            return None

    def get_section_sections(self, tab: str, obj_name: str, all_field: Dict[str, Any], layout_fields: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        xml_data = []
        sections = self.reader.find_elements(tab, "section")
        for section in sections:
            if section:
                section_label = self.get_tab_labels(section, obj_name)
                section_fields = self.get_fields_from_tab(section, all_field, obj_name, layout_fields)
                if section_fields and len(section_fields) > 0 and section_label:
                    xml_data.append(
                        {"query_label": section_label, "query_fields": section_fields}
                    )   

        return xml_data if xml_data else None

    def get_tabs_with_fields(
        self, root: str, obj_name: str, all_field: Dict[str, Any], layout_fields: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        xml_data = []
        tabs = self.reader.find_elements(root, "tab")
        for tab in tabs:
            if tab:
                tab_label = self.get_tab_labels(tab, obj_name)
                tab_fields = self.get_fields_from_tab(tab, all_field, obj_name, layout_fields)
                xml_data.append(
                    {"query_label": tab_label, "query_fields": tab_fields}
                )
                
                tab_sections = self.get_section_sections(tab, obj_name, all_field, layout_fields)
                
                if tab_sections:
                    xml_data.extend(tab_sections)
                # You can process tab_sections here if needed
                # For now, do nothing if tab_sections exists

        return xml_data

    def get_sections_with_fields(self, layout_xml: str) -> Optional[Dict[str, Any]]:
        pass

    def build_layout(self, layout_xml: str, layout_fields) -> Optional[Dict[str, Any]]:
    
        root = self.reader.read_xml_string(layout_xml["LayoutXML"])
        all_field = self.loader.loadJsonFile("fields.json")
        obj_name = self.get_object_enum_by_object_id(layout_xml["ItemTypeID"])
        tabs = self.get_tabs_with_fields(root, obj_name, all_field, layout_fields)
   

        return tabs

    def get_field_from_xml_query_info(self, layout_xml: str) -> Optional[str]:

        root = self.reader.read_xml_string(layout_xml)

        xml_data = []

        if root:
            fields = self.reader.find_elements(root, "selectfield")
            for col in fields:

                xml_data.append(self.reader.get_element_attribute(col, "fieldname"))

        return xml_data
