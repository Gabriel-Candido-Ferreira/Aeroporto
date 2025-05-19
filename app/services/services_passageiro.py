from fastapi import HTTPException
from bson import ObjectId
from app.database import db
from app.schemas.schema_passageiro import Passageiro
from app.services.services_voo import voos_collection
from bson.errors import InvalidId

passageiros_collection = db.passageiros
voos_collection = db.voos

def passageiro_helper(passageiro) -> dict:
    return {
        "id": str(passageiro["_id"]),
        "nome": passageiro["nome"],
        "cpf": passageiro["cpf"],
        "vooId": str(passageiro["vooId"]),
        "statusCheckIn": passageiro["statusCheckIn"]
    }

async def criar_passageiro(passageiro_data: Passageiro):
    existente = await passageiros_collection.find_one({"cpf": passageiro_data.cpf})
    if existente:
        raise HTTPException(status_code=400, detail="Passageiro com este CPF já existe.")

    try:
        passageiro_dict = passageiro_data.dict()
        passageiro_dict["vooId"] = ObjectId(passageiro_dict["vooId"])
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="ID do voo inválido.")

    voo = await voos_collection.find_one({"_id": passageiro_dict["vooId"]})
    if not voo:
        raise HTTPException(status_code=404, detail="Voo não encontrado.")

    result = await passageiros_collection.insert_one(passageiro_dict)
    return {
        "message": "Passageiro criado com sucesso!",
        "id": str(result.inserted_id)
    }
async def obter_todos_passageiros():
    passageiros_cursor = passageiros_collection.find()
    passageiros = []
    async for passageiro in passageiros_cursor:
        passageiros.append(passageiro_helper(passageiro))
    return passageiros

async def buscar_passageiro(id: str):
    try:
        _id = ObjectId(id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="ID inválido.")
    
    passageiro = await passageiros_collection.find_one({"_id": _id})
    if not passageiro:
        raise HTTPException(status_code=404, detail="Passageiro não encontrado.")
    return passageiro_helper(passageiro)

async def atualizar_passageiro(id: str, data: Passageiro):
    try:
        _id = ObjectId(id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="ID inválido.")

    data_dict = data.dict()

    if data_dict.get("statusCheckIn") == "realizado":
        passageiro = await passageiros_collection.find_one({"_id": _id})
        if not passageiro:
            raise HTTPException(status_code=404, detail="Passageiro não encontrado.")
        
        voo = await voos_collection.find_one({"_id": ObjectId(passageiro["vooId"])})
        if not voo or voo["status"].lower() != "embarque":
            raise HTTPException(status_code=400, detail="Check-in permitido apenas se o voo estiver com status 'embarque'.")

    await passageiros_collection.update_one({"_id": _id}, {"$set": data_dict})
    return await buscar_passageiro(id)

async def deletar_passageiro(id: str):
    try:
        _id = ObjectId(id)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="ID inválido.")

    resultado = await passageiros_collection.delete_one({"_id": _id})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Passageiro não encontrado.")
    return {"message": "Passageiro deletado com sucesso."}
