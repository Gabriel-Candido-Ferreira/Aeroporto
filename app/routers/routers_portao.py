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


# 🔓 Livre (listar todos os portões)
@router.get("/")
async def get_all():
    return await listar_portoes()


# 🔒 Apenas usuários autenticados podem criar
@router.post("/")
async def create(
    portao: Portao,
    current_user: dict = Depends(get_current_user)
):
    try:
        return await criar_portao(portao.dict())  
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# 🔓 Buscar por ID (livre)
@router.get("/{id}")
async def get_by_id(id: str):
    portao = await buscar_portao(id)
    if not portao:
        raise HTTPException(status_code=404, detail="Portão não encontrado")
    return portao


# 🔐 Apenas admin pode atualizar
@router.put("/{id}")
async def update(
    id: str,
    portao: Portao,
    current_admin: dict = Depends(get_current_admin_user)
):
    atualizado = await atualizar_portao(id, portao.dict())
    if not atualizado:
        raise HTTPException(status_code=404, detail="Portão não encontrado")
    return atualizado


# 🔐 Apenas admin pode deletar
@router.delete("/{id}")
async def delete(
    id: str,
    current_admin: dict = Depends(get_current_admin_user)
):
    sucesso = await deletar_portao(id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Portão não encontrado")
    return {"msg": "Portão deletado com sucesso"}
