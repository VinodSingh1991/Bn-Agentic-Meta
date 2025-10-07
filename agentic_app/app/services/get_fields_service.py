from services.get_layouts_service import LayoutService
from repositories.get_fields_repository import FieldsRepository
from files_handler.file_loader import FileLoader
from typing import List, Any, Dict
from collections import defaultdict

class FieldsService:
    def __init__(self):
        self.repository = FieldsRepository()
        self.loader = FileLoader()
        self.service = LayoutService()

    def get_fields_base(self) -> List[Any]:
        try:
            result = self.repository.get_fields()
            # Save the result to JSON file using the correct method name

            self.loader.save_files_at_orignal("fields.json", result)
            return result
        except Exception as e:
            print(f"Error in FieldsService.get_fields: {e}")
            return []

    def get_fields(self) -> List[Any]:

        result = self.get_fields_base()
        return result
    
    def get_layout_field_by_layout_field_id(self, layout_field_id: int, layout_fields: Any) -> List[Any]:
        
        if layout_fields:
            return layout_fields[layout_field_id] if layout_field_id in layout_fields else None
        return None

    def create_fields_from_cache(self) -> List[Any]:
        fields = self.loader.loadJsonFile("fields.json")

        new_fields = []

        for field in fields:
            obj_name = field.get("ObjectName", "Unknown")
            name = field.get("Label", "Unknown")
            enriched_field = {}
            enriched_field["roleid"] = 1
            enriched_field["object_name"] = obj_name
            enriched_field["field_id"] = field.get("FieldId", -1)
            enriched_field["name"] = name
            enriched_field["FieldName"] = field.get("FieldName", "Unknown")
            enriched_field["field_type"] = field.get("FieldType", "Text")

            
            new_fields.append({
                "query_label": f"{obj_name} {name}",
                "query_fields": [enriched_field]
            })

        self.loader.save_files_at_output("fields.json", new_fields)
        return new_fields

    def group_fields_by_roles(self) -> Dict[str, Any]:
        grouped = defaultdict(list)
        fields = self.loader.load_json_file_from_output("fields.json")
        
        for field in fields:
            roles = field.get("Roles", [])
            for role in roles:
                grouped[role].append(field)
        return dict(grouped)
    
    def group_fields_by_roles_and_object(self) -> Dict[str, Any]:
        grouped = self.group_fields_by_roles()

        for role, fields in grouped.items():
            object_grouped = self.get_fields_group_by_object_name(fields)
            grouped[role] = object_grouped
            if role is not None:
                self.loader.save_files_for_roles(f"{role}.json", object_grouped)

        self.loader.save_files_at_output("grouped_fields.json", grouped)
        return dict(grouped)

    def get_fields_group_by_object_name(self, fields:Any) -> List[Dict[str, Any]]:
        """Load all fields from the __local__ JSON file

        Returns:
            List[Dict[str, Any]]: List of object dictionaries with relevant fields
        """
        listings = self.loader.load_json_file_from_output("listing_gold5_enriched.json")
        grouped = defaultdict(lambda: {"object_fields": [], "object_listing": []})
    
        try:
            for field in fields:
                object_name = field.get("ObjectName", "Unknown")

                grouped[object_name]["object_fields"].append(field)
            
            for listing in listings:
                object_name = listing.get("ObjectName", "Unknown")
                grouped[object_name]["object_listing"].append(listing)

            # convert nested defaultdicts into normal dicts
            return {role: dict(objects) for role, objects in grouped.items()}

        except Exception as e:
            print(f"Error fetching layouts: {e}")
            return []