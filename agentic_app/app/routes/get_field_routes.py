from services.get_fields_service import FieldsService
from fastapi import APIRouter

router = APIRouter()


@router.get("/field_3")
def get_fields():
    fields_service = FieldsService()
    fields_service.get_fields()
    return {"fields": "field file has been created"}


@router.get("/create_fields_4")
def get_fields():
    fields_service = FieldsService()
    fields_service.create_fields_from_cache()
    return {"fields": "field file has been created"}

@router.get("/create_grouped_fields")
def get_grouped_fields():
    fields_service = FieldsService()
    fields_service.group_fields_by_roles_and_object()
    return {"fields": "grouped fields file has been created"}
