from fastapi import APIRouter, HTTPException, Depends
from app.schemas.schema_portao import Portao
from app.services.services_portao import (
    listar_portoes,
    criar_portao,
    buscar_portao,
    atualizar_portao,
    deletar_portao
)
from app.services.auth import get_current_user, get_current_admin_user

router = APIRouter(prefix="/portoes", tags=["Portões"])


@router.get("/")
async def get_all(current_user: dict = Depends(get_current_user)):
    return await listar_portoes()


@router.post("/")
async def create(
    portao: Portao,
    current_user: dict = Depends(get_current_admin_user)
):
    try:
        return await criar_portao(portao)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}")
async def get_by_id(id: str, current_user: dict = Depends(get_current_user)):
    portao = await buscar_portao(id)
    if not portao:
        raise HTTPException(status_code=404, detail="Portão não encontrado")
    return portao


@router.put("/{id}")
async def update(
    id: str,
    portao: Portao,
    current_admin: dict = Depends(get_current_admin_user)
):
    atualizado = await atualizar_portao(id, portao)
    if not atualizado:
        raise HTTPException(status_code=404, detail="Portão não encontrado")
    return atualizado


@router.delete("/{id}")
async def delete(
    id: str,
    current_admin: dict = Depends(get_current_admin_user)
):
    sucesso = await deletar_portao(id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Portão não encontrado")
    return {"msg": "Portão deletado com sucesso"}
