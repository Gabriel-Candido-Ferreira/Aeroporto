from fastapi import APIRouter, HTTPException, Depends
from app.services.auth import get_current_user, get_current_admin_user
from app.schemas.schema_passageiro import Passageiro
from app.services.services_passageiro import (
    criar_passageiro,
    obter_todos_passageiros,
    buscar_passageiro,
    atualizar_passageiro,
    deletar_passageiro
)

router = APIRouter(prefix="/passageiros", tags=["Passageiros"])


# 🔓 Pode ser público, mas se quiser pode proteger também
@router.get("/")
async def get_all():
    passageiros = await obter_todos_passageiros()
    return passageiros


# 🔒 Somente usuários autenticados podem criar passageiros
@router.post("/")
async def create(passageiro: Passageiro, current_user: dict = Depends(get_current_user)):
    try:
        return await criar_passageiro(passageiro)  
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}")
async def get_by_id(id: str):
    passageiro = await buscar_passageiro(id)
    if not passageiro:
        raise HTTPException(status_code=404, detail="Passageiro não encontrado")
    return passageiro


# 🔐 Somente administradores podem atualizar passageiros
@router.put("/{id}")
async def update(
    id: str,
    passageiro: Passageiro,
    current_admin: dict = Depends(get_current_admin_user)
):
    try:
        atualizado = await atualizar_passageiro(id, passageiro)
        return atualizado
    except HTTPException as e:
        raise e  


# 🔐 Somente administradores podem deletar passageiros
@router.delete("/{id}")
async def delete(
    id: str,
    current_admin: dict = Depends(get_current_admin_user)
):
    try:
        await deletar_passageiro(id)
        return {"msg": "Passageiro deletado com sucesso"}
    except HTTPException as e:
        raise e  
