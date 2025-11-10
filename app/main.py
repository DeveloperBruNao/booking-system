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


# ========== ENDPOINTS DE AUTENTICAÇÃO ==========

@app.post("/auth/registrar", response_model=user_schemas.UsuarioResposta)
def registrar(usuario_data: user_schemas.UsuarioCriar, db: Session = Depends(get_db)):
    """
    Registrar novo usuário no sistema
    """
    usuario_existente = user_crud.obter_usuario_por_email(db, usuario_data.email)
    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    return user_crud.criar_usuario(db, usuario_data)

@app.post("/auth/login")
def login(login_data: user_schemas.UsuarioLogin, db: Session = Depends(get_db)):
    """
    Fazer login e obter token de acesso
    """
    usuario = user_crud.autenticar_usuario(db, login_data.email, login_data.senha)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    access_token = criar_token_acesso(data={"sub": usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/auth/me", response_model=user_schemas.UsuarioResposta)
def obter_usuario_logado(usuario_atual: user_schemas.UsuarioResposta = Depends(obter_usuario_atual)):
    """
    Obter informações do usuário logado
    """
    return usuario_atual