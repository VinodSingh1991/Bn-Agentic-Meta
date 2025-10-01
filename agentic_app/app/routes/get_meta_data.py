from services.get_meta_data_service import MetaDataService
from fastapi import APIRouter

router = APIRouter()


@router.get("/fetch_meta_data")
def get_meta_data(role_id: str = None, object_ids: str = None):
    meta_data_service = MetaDataService()
    meta_data = meta_data_service.get_objects_meta_data_by_object_name(role_id, object_ids)
    print("meta_data", "meta_data fetched successfully")
    return meta_data

@router.get("/fetch_meta_data_by_role_id")
def get_meta_data(role_id: str = None):
    meta_data_service = MetaDataService()
    meta_data = meta_data_service.get_meta_data_by_role_id(role_id)
    print("meta_data", "meta_data fetched successfully")
    return meta_data


