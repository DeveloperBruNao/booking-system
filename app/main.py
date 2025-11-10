from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db, engine, Base
from app.models import user, space, booking
from app.schemas import user as user_schemas, space as space_schemas, booking as booking_schemas
from app.crud import user as user_crud, space as space_crud, booking as booking_crud
from app.auth.security import obter_usuario_atual, criar_token_acesso, verificar_token

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

# Dependência para obter usuário atual (AGORA CORRIGIDA)
def obter_usuario_logado(
    token_data: dict = Depends(obter_usuario_atual),
    db: Session = Depends(get_db)
):
    """
    Obtém o usuário atual a partir do token JWT
    """
    user_email = token_data.get("sub")
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    usuario = user_crud.obter_usuario_por_email(db, user_email)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado"
        )
    
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
def obter_usuario_logado_endpoint(usuario_atual: user_schemas.UsuarioResposta = Depends(obter_usuario_logado)):
    """
    Obter informações do usuário logado
    """
    return usuario_atual

# ========== ENDPOINTS DE ESPAÇOS ==========

@app.get("/espacos/", response_model=List[space_schemas.EspacoResposta])
def listar_espacos(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """
    Listar todos os espaços disponíveis
    """
    return space_crud.obter_espacos(db, skip=skip, limit=limit)

@app.get("/espacos/{espaco_id}", response_model=space_schemas.EspacoResposta)
def obter_espaco(espaco_id: int, db: Session = Depends(get_db)):
    """
    Obter detalhes de um espaço específico
    """
    espaco = space_crud.obter_espaco_por_id(db, espaco_id)
    if not espaco:
        raise HTTPException(status_code=404, detail="Espaço não encontrado")
    return espaco

@app.post("/espacos/", response_model=space_schemas.EspacoResposta)
def criar_espaco(
    espaco_data: space_schemas.EspacoCriar,
    db: Session = Depends(get_db),
    usuario_atual: user_schemas.UsuarioResposta = Depends(obter_usuario_logado)
):
    """
    Criar novo espaço (requer autenticação)
    """
    return space_crud.criar_espaco(db, espaco_data)

@app.put("/espacos/{espaco_id}/disponibilidade")
def atualizar_disponibilidade_espaco(
    espaco_id: int,
    disponivel: bool,
    db: Session = Depends(get_db),
    usuario_atual: user_schemas.UsuarioResposta = Depends(obter_usuario_logado)
):
    """
    Atualizar disponibilidade de um espaço (requer autenticação)
    """
    espaco = space_crud.atualizar_disponibilidade_espaco(db, espaco_id, disponivel)
    if not espaco:
        raise HTTPException(status_code=404, detail="Espaço não encontrado")
    
    status_msg = "disponível" if disponivel else "indisponível"
    return {"message": f"Espaço {espaco.nome} agora está {status_msg}"}

# ========== ENDPOINTS DE RESERVAS ==========

@app.post("/reservas/", response_model=booking_schemas.ReservaResposta)
def criar_reserva(
    reserva_data: booking_schemas.ReservaCriar,
    db: Session = Depends(get_db),
    usuario_atual: user_schemas.UsuarioResposta = Depends(obter_usuario_logado)
):
    """
    Criar nova reserva
    """
    try:
        return booking_crud.criar_reserva(db, reserva_data, usuario_atual.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.get("/reservas/minhas", response_model=List[booking_schemas.ReservaResposta])
def listar_minhas_reservas(
    db: Session = Depends(get_db),
    usuario_atual: user_schemas.UsuarioResposta = Depends(obter_usuario_logado)
):
    """
    Listar todas as reservas do usuário logado
    """
    return booking_crud.obter_reservas_usuario(db, usuario_atual.id)

@app.get("/reservas/{reserva_id}", response_model=booking_schemas.ReservaResposta)
def obter_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    usuario_atual: user_schemas.UsuarioResposta = Depends(obter_usuario_logado)
):
    """
    Obter detalhes de uma reserva específica
    """
    reserva = booking_crud.obter_reserva_por_id(db, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    
    # Verificar se a reserva pertence ao usuário
    if reserva.user_id != usuario_atual.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado a acessar esta reserva"
        )
    
    return reserva

@app.post("/reservas/{reserva_id}/cancelar")
def cancelar_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    usuario_atual: user_schemas.UsuarioResposta = Depends(obter_usuario_logado)
):
    """
    Cancelar uma reserva
    """
    try:
        reserva = booking_crud.cancelar_reserva(db, reserva_id, usuario_atual.id)
        return {"message": "Reserva cancelada com sucesso", "reserva_id": reserva_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@app.post("/reservas/verificar-disponibilidade")
def verificar_disponibilidade(
    disponibilidade: booking_schemas.VerificarDisponibilidade,
    db: Session = Depends(get_db)
):
    """
    Verificar disponibilidade de um espaço em um horário específico
    """
    esta_disponivel = booking_crud.verificar_disponibilidade(
        db, 
        disponibilidade.space_id, 
        disponibilidade.start_time, 
        disponibilidade.end_time
    )
    
    espaco = space_crud.obter_espaco_por_id(db, disponibilidade.space_id)
    if not espaco:
        raise HTTPException(status_code=404, detail="Espaço não encontrado")
    
    return {
        "disponivel": esta_disponivel,
        "espaco_id": disponibilidade.space_id,
        "espaco_nome": espaco.nome,
        "inicio": disponibilidade.start_time,
        "fim": disponibilidade.end_time
    }

@app.get("/espacos/{espaco_id}/reservas")
def listar_reservas_espaco(
    espaco_id: int,
    inicio: str = None,
    fim: str = None,
    db: Session = Depends(get_db),
    usuario_atual: user_schemas.UsuarioResposta = Depends(obter_usuario_logado)
):
    """
    Listar reservas de um espaço em um período (requer autenticação)
    """
    from datetime import datetime
    
    espaco = space_crud.obter_espaco_por_id(db, espaco_id)
    if not espaco:
        raise HTTPException(status_code=404, detail="Espaço não encontrado")
    
    # Se não forem fornecidas datas, usa padrão (próximos 7 dias)
    if not inicio:
        inicio = datetime.now()
    else:
        inicio = datetime.fromisoformat(inicio)
        
    if not fim:
        fim = datetime.now().replace(hour=23, minute=59, second=59)
    else:
        fim = datetime.fromisoformat(fim)
    
    reservas = booking_crud.obter_reservas_por_espaco(db, espaco_id, inicio, fim)
    return reservas