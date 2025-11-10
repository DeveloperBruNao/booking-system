from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.booking import BookingStatus

class ReservaBase(BaseModel):
    space_id: int
    start_time: datetime
    end_time: datetime

class ReservaCriar(ReservaBase):
    pass

class ReservaResposta(ReservaBase):
    id: int
    user_id: int
    status: BookingStatus
    total_price: float
    criado_em: datetime

    class Config:
        from_attributes = True

class VerificarDisponibilidade(BaseModel):
    space_id: int
    start_time: datetime
    end_time: datetime