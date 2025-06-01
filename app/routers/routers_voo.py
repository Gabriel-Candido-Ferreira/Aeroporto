from fastapi import APIRouter, HTTPException, Depends
from app.schemas.schema_voo import Voo
from app.services.services_voo import (
    criar_voo,
    obter_todos_voos,
    obter_voo_por_id,
    atualizar_voo,
    deletar_voo
)
from app.services.auth import get_current_user, get_current_admin_user

router = APIRouter(prefix="/voos", tags=["Voos"])


@router.get("/")
async def get_voos(current_user: dict = Depends(get_current_user)):
    return await obter_todos_voos()


@router.get("/{voo_id}")
async def get_voo(voo_id: str, current_user: dict = Depends(get_current_user)):
    try:
        return await obter_voo_por_id(voo_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/")
async def create_voo(voo: Voo, current_admin: dict = Depends(get_current_admin_user)):
    try:
        return await criar_voo(voo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{voo_id}")
async def update_voo(
    voo_id: str,
    voo: Voo,
    current_admin: dict = Depends(get_current_admin_user)
):
    try:
        return await atualizar_voo(voo_id, voo)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{voo_id}")
async def delete_voo(
    voo_id: str,
    current_admin: dict = Depends(get_current_admin_user)
):
    try:
        return await deletar_voo(voo_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
