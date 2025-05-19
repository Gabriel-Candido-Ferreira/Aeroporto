from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Literal

class Funcionario(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    cargo: str

    @validator('nome')
    def validate_nome(cls, v):
        if len(v) < 3:
            raise ValueError('O nome deve ter pelo menos 3 caracteres')
        return v

    @validator('cargo')
    def validate_cpf(cls, v):
        if len(v) < 3:
            raise ValueError('O cargo deve ter pelo menos 3 caracteres')
        return v