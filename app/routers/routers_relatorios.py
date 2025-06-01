from fastapi import APIRouter, Query, HTTPException, Depends
from datetime import datetime
from app.database import db
from bson import ObjectId
from app.services.auth import get_current_user

voos_collection = db.voos
passageiros_collection = db.passageiros
portoes_collection = db.portoes

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


@router.get("/voos-programados-dia")
async def relatorio_voos_programados_do_dia(
    data: str = Query(..., description="Data no formato YYYY-MM-DD"),
    current_user: dict = Depends(get_current_user) 
):
    try:
        data_especifica = datetime.strptime(data, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD.")

    voos_cursor = voos_collection.find({
        "status": "programado",
        "$expr": { 
            "$eq": [
                { "$dateToString": { "format": "%Y-%m-%d", "date": "$dataHoraPartida" } }, 
                data_especifica.isoformat()
            ]
        }
    })

    relatorio = []

    async for voo in voos_cursor:
        portao = None
        if "portaoId" in voo:
            portao = await portoes_collection.find_one({"_id": ObjectId(voo["portaoId"])})

        passageiros_cursor = passageiros_collection.find({"vooId": voo["_id"]})
        passageiros = []
        async for p in passageiros_cursor:
            passageiros.append({
                "nome": p["nome"],
                "cpf": p["cpf"],
                "statusCheckIn": p["statusCheckIn"]
            })

        relatorio.append({
            "numeroVoo": voo["numeroVoo"],
            "origem": voo["origem"],
            "destino": voo["destino"],
            "dataHoraPartida": voo["dataHoraPartida"].isoformat(),
            "portao": portao["codigo"] if portao else "N/A",
            "passageiros": passageiros
        })

    return relatorio
