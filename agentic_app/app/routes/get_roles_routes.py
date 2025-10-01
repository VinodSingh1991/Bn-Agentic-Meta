from services.get_roles_service import RoleService
from fastapi import APIRouter

router = APIRouter()


@router.get("/roles")
def get_roles():
    role_service = RoleService()
    roles = role_service.get_roles()
    return {"roles": roles}
