from services.get_layouts_service import LayoutService
from fastapi import APIRouter

router = APIRouter()


@router.get("/layouts_4")
def get_layouts():
    layout_service = LayoutService()
    layout_service.get_layouts()
    return {"layouts": "layout file has been created"}

@router.get("/create_layouts_5")
def create_layouts():
    layout_service = LayoutService()
    layout_service.create_layouts()
    return {"layouts": "layout file has been created"}
