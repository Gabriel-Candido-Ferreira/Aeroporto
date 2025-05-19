from pydantic import BaseModel, validator

class Portao(BaseModel):
    codigo: str
    disponivel: bool

    @validator('codigo')
    def validate_codigo(cls, v):
        if not v or len(v) < 2:
            raise ValueError('Código do portão inválido')
        return v
