from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EspacoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    capacidade: int
    preco_por_hora: float

class EspacoCriar(EspacoBase):
    pass

class EspacoResposta(EspacoBase):
    id: int
    esta_disponivel: bool
    criado_em: datetime

    class Config:
        from_attributes = True