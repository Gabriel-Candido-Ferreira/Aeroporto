from fastapi import HTTPException
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.errors import DuplicateKeyError
from app.database import db
from app.schemas.schema_portao import Portao

portoes_collection = db.portoes

def portao_helper(portao) -> dict:
    return {
        "id": str(portao["_id"]),
        "codigo": portao["codigo"],
        "disponivel": portao["disponivel"],
    }

async def criar_indice():
    await portoes_collection.create_index([("codigo", 1)], unique=True)

async def listar_portoes():
    portoes = []
    async for portao in portoes_collection.find():
        portoes.append(portao_helper(portao))
    return portoes

async def criar_portao(data: dict):
    try:
        portao_data = Portao(**data.dict())
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

    codigo_existente = await portoes_collection.find_one({"codigo": portao_data.codigo})
    if codigo_existente:
        raise HTTPException(status_code=400, detail=f"O código {portao_data.codigo} já está em uso.")

    try:
        result = await portoes_collection.insert_one(portao_data.dict())
        portao = await portoes_collection.find_one({"_id": result.inserted_id})
        return portao_helper(portao)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail=f"O código {portao_data.codigo} já existe.")

async def buscar_portao(id: str):
    try:
        obj_id = ObjectId(id)
        portao = await portoes_collection.find_one({"_id": obj_id})
        if portao:
            return portao_helper(portao)
        raise HTTPException(status_code=404, detail="Portão não encontrado.")
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar portão: {str(e)}")

async def atualizar_portao(id: str, data: dict):
    try:
        obj_id = ObjectId(id)
        await portoes_collection.update_one({"_id": obj_id}, {"$set": data})
        return await buscar_portao(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar portão: {str(e)}")

async def deletar_portao(id: str):
    try:
        obj_id = ObjectId(id)
        result = await portoes_collection.delete_one({"_id": obj_id})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Portão não encontrado.")
        return True
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar portão: {str(e)}")
