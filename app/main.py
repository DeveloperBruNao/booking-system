from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db, engine, Base
from app.models import user, space, booking
from app.schemas import user as user_schemas, space as space_schemas, booking as booking_schemas
from app.crud import user as user_crud, space as space_crud, booking as booking_crud
from app.auth.security import verify_token, criar_token_acesso

# Criar tabelas no banco
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Booking System API",
    description="Sistema profissional de reservas - DeveloperBruNao",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependência para obter usuário atual
def obter_usuario_atual(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    user_email = token.get("sub")
    usuario = user_crud.obter_usuario_por_email(db, user_email)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return usuario

@app.get("/")
def read_root():
    return {
        "message": "Booking System API 🏨", 
        "developer": "DeveloperBruNao",
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "booking-system"}