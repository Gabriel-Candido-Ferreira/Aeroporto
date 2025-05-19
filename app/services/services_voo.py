from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from app.database import db
from app.schemas.schema_voo import Voo
from app.services.services_portao import portoes_collection

voos_collection = db.voos

def voo_helper(voo) -> dict:
    return {
        "id": str(voo["_id"]),
        "numeroVoo": voo["numeroVoo"],
        "origem": voo["origem"],
        "destino": voo["destino"],
        "dataHoraPartida": voo["dataHoraPartida"].isoformat() if "dataHoraPartida" in voo else None,
        "portaoId": str(voo["portaoId"]) if "portaoId" in voo else None,
        "status": voo["status"]
    }

async def criar_voo(voo_data: Voo):
    try:
        portao_obj_id = ObjectId(voo_data.portaoId)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=400, detail="Portão ID inválido.")

    portao = await portoes_collection.find_one({"_id": portao_obj_id})
    if not portao or not portao["disponivel"]:
        raise HTTPException(status_code=400, detail="Portão não encontrado ou não disponível.")

    await portoes_collection.update_one({"_id": portao_obj_id}, {"$set": {"disponivel": False}})

    voo_dict = voo_data.dict()
    voo_dict["portaoId"] = portao_obj_id
    result = await voos_collection.insert_one(voo_dict)
    voo_criado = await voos_collection.find_one({"_id": result.inserted_id})
    return voo_helper(voo_criado)

async def obter_todos_voos():
    voos = []
    async for voo in voos_collection.find():
        voos.append(voo_helper(voo))
    return voos

async def obter_voo_por_id(voo_id: str):
    try:
        obj_id = ObjectId(voo_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID de voo inválido.")

    voo = await voos_collection.find_one({"_id": obj_id})
    if not voo:
        raise HTTPException(status_code=404, detail="Voo não encontrado.")
    
    return voo_helper(voo)

async def atualizar_voo(voo_id: str, voo_data: Voo):
    try:
        voo_obj_id = ObjectId(voo_id)
        novo_portao_obj_id = ObjectId(voo_data.portaoId)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido.")

    voo_antigo = await voos_collection.find_one({"_id": voo_obj_id})
    if not voo_antigo:
        raise HTTPException(status_code=404, detail="Voo não encontrado.")

    if str(voo_antigo["portaoId"]) != str(novo_portao_obj_id):
        novo_portao = await portoes_collection.find_one({"_id": novo_portao_obj_id})
        if not novo_portao or not novo_portao["disponivel"]:
            raise HTTPException(status_code=400, detail="Novo portão não encontrado ou indisponível.")

        await portoes_collection.update_one({"_id": voo_antigo["portaoId"]}, {"$set": {"disponivel": True}})
        await portoes_collection.update_one({"_id": novo_portao_obj_id}, {"$set": {"disponivel": False}})


    novo_dados_voo = voo_data.dict()
    novo_dados_voo["portaoId"] = novo_portao_obj_id
    await voos_collection.update_one({"_id": voo_obj_id}, {"$set": novo_dados_voo})

    if novo_dados_voo.get("status") == "concluído":
        await portoes_collection.update_one({"_id": novo_portao_obj_id}, {"$set": {"disponivel": True}})
    return {"message": "Voo atualizado com sucesso!"}

async def deletar_voo(voo_id: str):
    try:
        obj_id = ObjectId(voo_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido.")

    voo = await voos_collection.find_one({"_id": obj_id})
    if not voo:
        raise HTTPException(status_code=404, detail="Voo não encontrado.")

    if "portaoId" in voo:
        await portoes_collection.update_one(
            {"_id": voo["portaoId"]},
            {"$set": {"disponivel": True}}
        )

    await voos_collection.delete_one({"_id": obj_id})
    return {"message": "Voo deletado com sucesso!"}
