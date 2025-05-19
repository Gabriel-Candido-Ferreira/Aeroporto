from fastapi import APIRouter, HTTPException
from app.schemas.schema_funcionario import Funcionario
from app.services.services_funcionario import criar_funcionario, obter_todos_funcionarios, buscar_funcionario, atualizar_funcionario, deletar_funcionario

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])

@router.get("/")
async def get_all():
    passageiros = await obter_todos_funcionarios()
    return passageiros

@router.post("/")
async def create(passageiro: Funcionario):
    try:
        return await criar_funcionario(passageiro)  
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/{id}")
async def get_by_id(id: str):
    passageiro = await buscar_funcionario(id)
    if not passageiro:
        raise HTTPException(status_code=404, detail="Passageiro não encontrado")
    return passageiro

@router.put("/{id}")
async def update(id: str, passageiro: Funcionario):
    try:
        atualizado = await atualizar_funcionario(id, passageiro)
        return atualizado
    except HTTPException as e:
        raise e  
    
@router.delete("/{id}")
async def delete(id: str):
    try:
        await deletar_funcionario(id)
        return {"msg": "Passageiro deletado com sucesso"}
    except HTTPException as e:
        raise e 