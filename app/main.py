from fastapi import FastAPI
from app.routers import routers_funcionario, routers_voo, routers_portao, routers_passageiro, routers_relatorios

app = FastAPI()

app.include_router(routers_funcionario.router)
app.include_router(routers_voo.router)
app.include_router(routers_portao.router)
app.include_router(routers_passageiro.router)
app.include_router(routers_relatorios.router)