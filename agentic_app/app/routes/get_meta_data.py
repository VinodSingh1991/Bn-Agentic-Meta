from rag.schema_builder.schema_builder import SchemaBuilder
from fastapi import APIRouter
from services.get_meta_data_service import MetaDataService

router = APIRouter()


@router.get("/fetch_all_listings_and_layouts")
def get_listing_for_rag():
    builderContext = SchemaBuilder()
    print("meta_data", "meta_data fetched successfully")
    return builderContext.build_rag()


# @router.get("/fetch_meta_data_by_role_id")
# def get_meta_data(role_id: str = None):
#     meta_data_service = MetaDataService()
#     meta_data = meta_data_service.get_meta_data_by_role_id(role_id)
#     print("meta_data", "meta_data fetched successfully")
#     return meta_data
