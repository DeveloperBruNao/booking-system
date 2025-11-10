from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    email: EmailStr
    nome_completo: str

class UsuarioCriar(UsuarioBase):
    senha: str

class UsuarioResposta(UsuarioBase):
    id: int
    esta_ativo: bool
    criado_em: datetime

    class Config:
        from_attributes = True

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str