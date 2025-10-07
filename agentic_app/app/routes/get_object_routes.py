from services.get_objects_service import ObjectService
from fastapi import APIRouter

router = APIRouter()


@router.get("/objects_two")
def get_objects():
    object_service = ObjectService()
    objects = object_service.get_objects()
    return {"objects": objects}
