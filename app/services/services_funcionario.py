from fastapi import HTTPException
from bson import ObjectId
from bson.errors import InvalidId
from app.database import db
from app.schemas.schema_funcionario import Funcionario
from app.utils.security import hash_password

funcionarios_collection = db.funcionarios


def funcionarion_helper(funcionario) -> dict:
    return {
        "id": str(funcionario["_id"]),
        "nome": funcionario["nome"],
        "email": funcionario["email"],
        "cargo": funcionario["cargo"]
    }


async def criar_funcionario(funcionario_data: Funcionario):
    existente = await funcionarios_collection.find_one({"email": funcionario_data.email})
    if existente:
        raise HTTPException(status_code=400, detail="Funcionário com este e-mail já existe.")

    funcionario_dict = funcionario_data.dict()

    if "senha" not in funcionario_dict or not funcionario_dict["senha"]:
        raise HTTPException(status_code=400, detail="Campo 'senha' é obrigatório.")

    funcionario_dict["senha"] = hash_password(funcionario_dict["senha"])
    
    result = await funcionarios_collection.insert_one(funcionario_dict)

    funcionario = await funcionarios_collection.find_one({"_id": result.inserted_id})

    return funcionarion_helper(funcionario)


async def obter_todos_funcionarios():
    funcionarios_cursor = funcionarios_collection.find()
    funcionarios = []
    async for funcionario in funcionarios_cursor:
        funcionarios.append(funcionarion_helper(funcionario))
    return funcionarios


async def buscar_funcionario_por_nome(nome: str):
    funcionario = await funcionarios_collection.find_one({"nome": nome})
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado.")
    return funcionarion_helper(funcionario)


async def buscar_funcionario(id: str):
    try:
        _id = ObjectId(id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="ID inválido.")

    funcionario = await funcionarios_collection.find_one({"_id": _id})
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado.")
    return funcionarion_helper(funcionario)


async def atualizar_funcionario(id: str, data: Funcionario):
    try:
        _id = ObjectId(id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="ID inválido.")

    data_dict = data.dict(exclude_unset=True)

    existing_user = await funcionarios_collection.find_one({
        "email": data_dict.get("email"),
        "_id": {"$ne": _id}
    })
    if existing_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado para outro funcionário.")

    funcionario = await funcionarios_collection.find_one({"_id": _id})
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado.")

    if "senha" in data_dict and data_dict["senha"]:
        data_dict["senha"] = hash_password(data_dict["senha"])
    else:
        data_dict.pop("senha", None)

    await funcionarios_collection.update_one({"_id": _id}, {"$set": data_dict})
    return await buscar_funcionario(id)


async def deletar_funcionario(id: str):
    try:
        _id = ObjectId(id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="ID inválido.")

    resultado = await funcionarios_collection.delete_one({"_id": _id})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado.")
    return {"message": "Funcionário deletado com sucesso."}
