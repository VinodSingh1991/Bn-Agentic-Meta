
class SetMetadata:
    def __init__(self):
        pass
    
    def get_object_name(self, data_fields: list) -> str:
        if data_fields and isinstance(data_fields, list):
            return data_fields[0].get("object_name", "Unknown")
        return "Unknown"
    
    def get_role_id(self, data_fields: list) -> int:
        if data_fields and isinstance(data_fields, list):
            return data_fields[0].get("role_id", 1)
        return 1

    def set_metadata(
        self,
        intent: str,
        output_format: str,
        data_fields: list = [],
        filters: list = [],
        limit: int = 10,
        order_field: str = {},
        order_direction: str = "ASC",
        group_by_fields: list = [],
        docstring: str = ""
    ) -> dict:
        """This function is responsible for creating the metadata structure"""
        f"""{docstring}"""
        return {
            "object_name": self.get_object_name(data_fields),
            "role_id": self.get_role_id(data_fields),
            "intent": intent,
            "output_format": output_format,
            "data_fields": data_fields,
            "filters": filters,
            "limit": limit,
            "order": {"field": order_field, "direction": order_direction},
            "groupBy": group_by_fields
        }
