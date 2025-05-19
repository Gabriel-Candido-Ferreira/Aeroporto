from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.aeroporto

passageiros_collection = db.get_collection("passageiros")
voos_collection = db.voos
portoes_collection = db.portoes
