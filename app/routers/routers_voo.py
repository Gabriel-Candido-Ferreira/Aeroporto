from fastapi import APIRouter, HTTPException
from app.schemas.schema_voo import Voo
from app.services.services_voo import criar_voo, obter_todos_voos, obter_voo_por_id, atualizar_voo, deletar_voo

router = APIRouter(prefix="/voos", tags=["Voos"])

@router.post("/voos/")
async def create_voo(voo: Voo):
    try:
        return await criar_voo(voo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/voos/")
async def get_voos():
    return await obter_todos_voos()

@router.get("/voos/{voo_id}")
async def get_voo(voo_id: str):
    try:
        return await obter_voo_por_id(voo_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/voos/{voo_id}")
async def update_voo(voo_id: str, voo: Voo):
    try:
        return await atualizar_voo(voo_id, voo)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/voos/{voo_id}")
async def delete_voo(voo_id: str):
    try:
        return await deletar_voo(voo_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
