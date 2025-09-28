from src.utility.meta_data import MetaDataUtility
from src.interfaces.response_model import ResponseModel
from src.utility.public_util import get_data_from_response_data, generate_words
from src.utility.nlp_dict.object_synonyms import OBJECT_SYNONYMS


class EntityNormalization:
    def __init__(self):
        self.meta_data_utility = MetaDataUtility()

    # Get fields as a dictionary with fieldId as key
    def get_fields_dict(self) -> ResponseModel:
        fieldCollection = {}
        system_fields_response = self.meta_data_utility.get_fields_from_src(
            "system_fields.json"
        )
        custom_fields_response = self.meta_data_utility.get_fields_from_src(
            "fields.json"
        )
        # fields_response is a Pydantic model: FieldsResponse
        system_fields_data = get_data_from_response_data(system_fields_response)
        custom_fields_data = get_data_from_response_data(custom_fields_response)

        for field in system_fields_data + custom_fields_data:
            # field is a FieldModel, convert to dict if needed
            field_dict = field.dict() if hasattr(field, "dict") else dict(field)
            field_id = field_dict.get("fieldId")
            if field_id:
                # Ensure field_id is a string and strip leading/trailing whitespace and dashes
                field_id_str = str(field_id).strip().lstrip("-").rstrip("-")
                fieldCollection[field_id_str] = field_dict
        return fieldCollection

    # Get objects as a dictionary with objectId as key
    def get_object_dict(self) -> ResponseModel:
        object_Collection = {}
        objects_response = self.meta_data_utility.get_fields_from_src("objects.json")
        # fields_response is a Pydantic model: FieldsResponse
        objects_data = get_data_from_response_data(objects_response)

        for obj in objects_data:
            obj_dict = obj.dict() if hasattr(obj, "dict") else dict(obj)
            obj_id = obj_dict.get("objectId")
            if obj_id:
                object_Collection[obj_id] = obj_dict
        return object_Collection

    def get_field_synonyms(self, field_name: str, field_label: str) -> list:
        # Generate synonyms for the field name and label
        synonyms = [field_name]
        if field_label and field_label != field_name:
            synonyms.append(field_label)
        # Add more sophisticated synonym generation if needed
        return synonyms

    # get field entities
    def get_field_entities(self) -> ResponseModel:
        entities = {}
        fields_dict = self.get_fields_dict()
        for field_id, field_info in fields_dict.items():
            field_name = field_info.get("fieldName")
            field_label = field_info.get("fieldLabel")
            object_id = field_info.get("objectId")
            object_name = field_info.get("objectName")
            field_modified = field_info.get("modifiedFieldId")
            field_layout_id = field_info.get("layoutFieldId")
            field_synonyms = field_info.get("synonyms", [field_label, field_name, field_modified, field_layout_id])
            # Use list concatenation to merge synonyms, field_name, and field_label
            fls_synonyms = list(field_synonyms)
            if field_name and field_name not in fls_synonyms:
                fls_synonyms.append(field_name)
            if field_label and field_label not in fls_synonyms:
                fls_synonyms.append(field_label)
            if field_modified and field_modified not in fls_synonyms:
                fls_synonyms.append(field_modified)
            if field_layout_id and field_layout_id not in fls_synonyms:
                fls_synonyms.append(field_layout_id)

            field_sys = generate_words(fls_synonyms)

            # print(f"Generating synonyms for field_sys: {field_sys}")

            entities[field_id] = {
                "index": field_id,
                "type": "field",
                "parentId": object_id,
                "parentName": object_name,
                "fieldId": field_id,
                "fieldName": field_name,
                "relation": "objectId",
                "fieldLabel": field_label,
                "layout_field_id": field_layout_id,
                "synonyms": field_sys,
            }
        return entities

    def get_object_synonyms(self, object_name: str) -> list:
        # Generate synonyms for the object name
        object_sys = OBJECT_SYNONYMS.get(object_name, None)
        print(f"Generating synonyms for object: {object_name}")
        # Add more sophisticated synonym generation if needed
        return object_sys

    def get_layout_by_objectId(self, object_id: str) -> ResponseModel:

        layout_response = self.meta_data_utility.get_fields_from_src("layouts.json")
        # fields_response is a Pydantic model: FieldsResponse
        layout_data = get_data_from_response_data(layout_response)

        for layout in layout_data:
            layout_dict = layout.dict() if hasattr(layout, "dict") else dict(layout)
            layout_object_id = layout_dict.get("objectId")
            field = layout_dict.get("fields")
            # Only return if field is not None and not empty
            if layout_object_id == object_id and field:
                return field

    def get_object_entities(self) -> ResponseModel:
        entities = {}
        object_dict = self.get_object_dict()
        for object_id, object_info in object_dict.items():
            object_name = object_info.get("objectName")
            entities[object_id] = {
                "index": object_id,
                "type": "object",
                "parentId": "rootId",
                "parentName": "rootName",
                "relation": "self_parent",
                "objectId": object_id,
                "objectName": object_name,
                "layouts_fields": self.get_layout_by_objectId(object_id),
                "synonyms": self.get_object_synonyms(object_name),
            }
        return entities

    # Get all entities (fields and objects)
    def get_entities(self) -> ResponseModel:
        field_entities = self.get_field_entities()
        object_entities = self.get_object_entities()

        return {**object_entities, **field_entities}

    # Get inverted index mapping synonyms to entity IDs
    def get_invertedIndex(self) -> ResponseModel:
        field_entities = self.get_field_entities()
        object_entities = self.get_object_entities()
        entity_reverted_index = {}
        for key, value in {**field_entities, **object_entities}.items():
            synonyms = value.get("synonyms", [])
            # Flatten if synonyms is not a list (e.g., None or single string)
            if not isinstance(synonyms, list):
                synonyms = [synonyms] if synonyms else []
            for synonym in synonyms:
                if synonym:
                    # Lowercase and strip whitespace for robust matching
                    norm_syn = str(synonym).strip().lower()
                    entity_reverted_index[norm_syn] = key
        return entity_reverted_index
