from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import datetime

class Voo(BaseModel):
    numeroVoo: str
    origem: str
    destino: str
    dataHoraPartida: datetime
    portaoId: str
    status: Literal["programado", "embarque", "concluído"]

    @validator('numeroVoo')
    def validate_numero_voo(cls, v):
        if not v.strip():
            raise ValueError('Número do voo não pode estar vazio')
        if not v.isdigit():
            raise ValueError('Número do voo deve conter apenas dígitos')
        return v


    @validator('origem', 'destino')
    def validate_cidades(cls, v):
        if len(v) < 3:
            raise ValueError('Origem e destino devem ter pelo menos 3 caracteres')
        return v
    
    