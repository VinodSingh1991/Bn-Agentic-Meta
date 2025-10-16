from agents.tools.get_field_base import FieldData, BaseFieldTool

def get_field_by_field_name_and_object(field_name: str, object_name: str) -> FieldData | None:
    """Get field by field name and object name."""
    base_tool = BaseFieldTool()
    fields = base_tool.get_field_by_field_name_and_object(field_name, object_name)
    return fields[0] if fields else None


def get_field_by_object_name(object_name: str) -> list[FieldData] | None:
    """Get field by object name."""
    base_tool = BaseFieldTool()
    fields = base_tool.get_field_by_object_name(object_name)
    return fields if fields else None

def get_field_by_object_name_and_label(object_name: str, label: str) -> FieldData | None:
    """Get field by object name and label."""
    base_tool = BaseFieldTool()
    fields = base_tool.get_field_by_object_name_and_label(object_name, label)
    return fields[0] if fields else None