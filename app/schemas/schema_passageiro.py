from pydantic import BaseModel, Field, validator
from typing import Optional, Literal

class Passageiro(BaseModel):
    nome: str
    cpf: str
    vooId: str
    statusCheckIn: Literal["pendente", "realizado"]

    @validator('nome')
    def validate_nome(cls, v):
        if len(v) < 3:
            raise ValueError('O nome deve ter pelo menos 3 caracteres')
        return v

    @validator('cpf')
    def validate_cpf(cls, v):
        if not v.isdigit() or len(v) != 11:
            raise ValueError('CPF deve conter exatamente 11 dígitos numéricos')
        return v