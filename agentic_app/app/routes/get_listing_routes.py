from services.get_listing_service import  ListingService
from fastapi import APIRouter

router = APIRouter()


@router.get("/rpt_listing")
def get_rpt_listing():
    listing_service = ListingService()
    listing_service.get_rpt_listing()
    return {"listing": "listing file has been created"}


@router.get("/gold5_listing")
def get_gold5_listing():
    listing_service = ListingService()
    listing_service.get_gold5_listing()
    return {"listing": "listing file has been created"}

@router.get("/object_relationship_listing")
def get_object_relationship_listing():
    listing_service = ListingService()
    listing_service.get_object_relation_listing()
    return {"listing": "listing file has been created"}


@router.get("/listing_gold5_enriched")
def get_listing_gold5_enriched():
    listing_service = ListingService()
    listing_service.map_object_and_gold5_listing()
    return {"listing": "listing file has been created"}

@router.get("/listing_rpt_enriched")
def get_listing_rpt_enriched():
    listing_service = ListingService()
    listing_service.map_object_and_rpt_listing()
    return {"listing": "listing file has been created"}

