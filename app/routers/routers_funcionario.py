from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.schemas.schema_funcionario import Funcionario, FuncionarioResponse, Token
from app.services.services_funcionario import (
    criar_funcionario, obter_todos_funcionarios, buscar_funcionario,
    atualizar_funcionario, deletar_funcionario, buscar_funcionario_por_nome
)
from app.utils.security import (
    create_access_token, verify_password, oauth2_scheme, get_current_user, get_current_admin
)

router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])



@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    funcionario = await buscar_funcionario_por_nome(form_data.username)
    if not funcionario or not verify_password(form_data.password, funcionario["senha"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = {
        "sub": str(funcionario["_id"]),
        "nome": funcionario["nome"],
        "cargo": funcionario["cargo"]
    }
    token = create_access_token(data=token_data)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/", dependencies=[Depends(get_current_user)])
async def get_all():
    funcionarios = await obter_todos_funcionarios()
    return funcionarios

@router.get("/{id}", dependencies=[Depends(get_current_user)])
async def get_by_id(id: str):
    funcionario = await buscar_funcionario(id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario

@router.post("/", dependencies=[Depends(get_current_admin)])
async def create(funcionario: Funcionario):
    try:
        return await criar_funcionario(funcionario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}", dependencies=[Depends(get_current_admin)])
async def update(id: str, funcionario: Funcionario):
    try:
        atualizado = await atualizar_funcionario(id, funcionario)
        return atualizado
    except HTTPException as e:
        raise e


@router.delete("/{id}", dependencies=[Depends(get_current_admin)])
async def delete(id: str):
    try:
        await deletar_funcionario(id)
        return {"msg": "Funcionário deletado com sucesso"}
    except HTTPException as e:
        raise e
