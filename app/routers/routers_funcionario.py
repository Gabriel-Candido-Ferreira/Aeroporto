from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.schema_funcionario import Funcionario, Token
from app.services.services_funcionario import (
    criar_funcionario, obter_todos_funcionarios, buscar_funcionario,
    atualizar_funcionario, deletar_funcionario, buscar_funcionario_por_email
)
from app.utils.security import (
    create_access_token, verify_password, oauth2_scheme, get_current_user, get_current_admin
)


router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    funcionario = await buscar_funcionario_por_email(form_data.username)

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


@router.get("/")
async def get_all(current_user: dict = Depends(get_current_user)):
    funcionarios = await obter_todos_funcionarios()
    return funcionarios


@router.get("/{id}")
async def get_by_id(id: str, current_user: dict = Depends(get_current_user)):
    funcionario = await buscar_funcionario(id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario


@router.post("/")
async def create(funcionario: Funcionario, current_admin: dict = Depends(get_current_admin)):
    try:
        return await criar_funcionario(funcionario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{id}")
async def update(id: str, funcionario: Funcionario, current_admin: dict = Depends(get_current_admin)):
    try:
        atualizado = await atualizar_funcionario(id, funcionario)
        return atualizado
    except HTTPException as e:
        raise e


@router.delete("/{id}")
async def delete(id: str, current_admin: dict = Depends(get_current_admin)):
    try:
        await deletar_funcionario(id)
        return {"msg": "Funcionário deletado com sucesso"}
    except HTTPException as e:
        raise e
