from fastapi import APIRouter, HTTPException
from app.schemas.schema_portao import Portao
from app.services.services_portao import listar_portoes, criar_portao, buscar_portao, atualizar_portao, deletar_portao

router = APIRouter(prefix="/portoes", tags=["Portões"])

@router.get("/")
async def get_all():
    return await listar_portoes()

@router.post("/")
async def create(portao: Portao):
    try:
        return await criar_portao(portao.dict())  
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}")
async def get_by_id(id: str):
    portao = await buscar_portao(id)
    if not portao:
        raise HTTPException(status_code=404, detail="Portão não encontrado")
    return portao

@router.put("/{id}")
async def update(id: str, portao: Portao):
    atualizado = await atualizar_portao(id, portao.dict())
    if not atualizado:
        raise HTTPException(status_code=404, detail="Portão não encontrado")
    return atualizado

@router.delete("/{id}")
async def delete(id: str):
    sucesso = await deletar_portao(id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Portão não encontrado")
    return {"msg": "Portão deletado com sucesso"}
