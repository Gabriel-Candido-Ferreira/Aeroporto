from pydantic import BaseModel, EmailStr, validator
from typing import Optional


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
    def validate_cargo(cls, v):
        if len(v) < 3:
            raise ValueError('O cargo deve ter pelo menos 3 caracteres')
        return v


class FuncionarioResponse(BaseModel):
    id: str
    nome: str
    email: EmailStr
    cargo: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    nome: Optional[str] = None
    cargo: Optional[str] = None
