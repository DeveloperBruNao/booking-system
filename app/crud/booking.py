from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from app.models.booking import Booking, BookingStatus
from app.schemas.booking import ReservaCriar
from datetime import datetime
from fastapi import HTTPException

def verificar_disponibilidade(db: Session, espaco_id: int, inicio: datetime, fim: datetime, reserva_id: int = None):
    """
    Verifica se o espaço está disponível no horário solicitado.
    Lógica complexa que considera sobreposição de horários.
    """
    # Query para encontrar reservas conflitantes
    query = db.query(Booking).filter(
        Booking.space_id == espaco_id,
        Booking.status.in_([BookingStatus.PENDENTE, BookingStatus.CONFIRMADA]),
        or_(
            # Caso 1: Nova reserva começa durante uma reserva existente
            and_(Booking.start_time <= inicio, Booking.end_time > inicio),
            # Caso 2: Nova reserva termina durante uma reserva existente
            and_(Booking.start_time < fim, Booking.end_time >= fim),
            # Caso 3: Nova reserva engloba uma reserva existente
            and_(Booking.start_time >= inicio, Booking.end_time <= fim),
            # Caso 4: Reserva existente engloba a nova reserva
            and_(Booking.start_time <= inicio, Booking.end_time >= fim)
        )
    )
    
    # Se estiver atualizando uma reserva, exclui ela mesma da verificação
    if reserva_id:
        query = query.filter(Booking.id != reserva_id)
    
    reservas_conflitantes = query.count()
    return reservas_conflitantes == 0

def calcular_preco_reserva(espaco, inicio: datetime, fim: datetime):
    """Calcula o preço total baseado na duração e preço por hora"""
    duracao_horas = (fim - inicio).total_seconds() / 3600
    return espaco.preco_por_hora * duracao_horas

def criar_reserva(db: Session, reserva: ReservaCriar, usuario_id: int):
    """Cria uma nova reserva com todas as validações de negócio"""
    espaco = obter_espaco_por_id(db, reserva.space_id)
    
    if not espaco:
        raise HTTPException(status_code=404, detail="Espaço não encontrado")
    
    if not espaco.is_available:
        raise HTTPException(status_code=400, detail="Espaço não está disponível para reservas")
    
    # Validações de negócio
    if reserva.start_time >= reserva.end_time:
        raise HTTPException(status_code=400, detail="Horário de início deve ser antes do horário de fim")
    
    if reserva.start_time < datetime.now():
        raise HTTPException(status_code=400, detail="Não é possível fazer reservas no passado")
    
    # Verifica disponibilidade
    if not verificar_disponibilidade(db, reserva.space_id, reserva.start_time, reserva.end_time):
        raise HTTPException(status_code=400, detail="Espaço não disponível no horário selecionado")
    
    # Calcula preço
    preco_total = calcular_preco_reserva(espaco, reserva.start_time, reserva.end_time)
    
    # Cria a reserva
    db_reserva = Booking(
        **reserva.dict(),
        user_id=usuario_id,
        total_price=preco_total,
        status=BookingStatus.PENDENTE
    )
    
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

def obter_reservas_usuario(db: Session, usuario_id: int):
    """Obtém todas as reservas de um usuário"""
    return db.query(Booking).filter(Booking.user_id == usuario_id).order_by(Booking.start_time.desc()).all()

def obter_reserva_por_id(db: Session, reserva_id: int):
    """Obtém uma reserva específica"""
    return db.query(Booking).filter(Booking.id == reserva_id).first()

def cancelar_reserva(db: Session, reserva_id: int, usuario_id: int):
    """Cancela uma reserva (apenas se for do usuário)"""
    reserva = db.query(Booking).filter(
        Booking.id == reserva_id, 
        Booking.user_id == usuario_id
    ).first()
    
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva não encontrada")
    
    if reserva.status == BookingStatus.CANCELADA:
        raise HTTPException(status_code=400, detail="Reserva já está cancelada")
    
    # Não permite cancelar reservas que já começaram
    if reserva.start_time < datetime.now():
        raise HTTPException(status_code=400, detail="Não é possível cancelar reservas que já começaram")
    
    reserva.status = BookingStatus.CANCELADA
    db.commit()
    db.refresh(reserva)
    return reserva

def confirmar_reserva(db: Session, reserva_id: int):
    """Confirma uma reserva (para admin)"""
    reserva = obter_reserva_por_id(db, reserva_id)
    if reserva:
        reserva.status = BookingStatus.CONFIRMADA
        db.commit()
        db.refresh(reserva)
    return reserva

def obter_reservas_por_espaco(db: Session, espaco_id: int, inicio: datetime, fim: datetime):
    """Obtém reservas de um espaço em um período específico"""
    return db.query(Booking).filter(
        Booking.space_id == espaco_id,
        Booking.start_time >= inicio,
        Booking.end_time <= fim,
        Booking.status.in_([BookingStatus.PENDENTE, BookingStatus.CONFIRMADA])
    ).all()