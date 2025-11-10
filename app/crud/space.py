from sqlalchemy.orm import Session
from app.models.space import Space
from app.schemas.space import EspacoCriar

def obter_espacos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Space).filter(Space.is_available == True).offset(skip).limit(limit).all()

def obter_espaco_por_id(db: Session, espaco_id: int):
    return db.query(Space).filter(Space.id == espaco_id).first()

def criar_espaco(db: Session, espaco: EspacoCriar):
    db_espaco = Space(**espaco.dict())
    db.add(db_espaco)
    db.commit()
    db.refresh(db_espaco)
    return db_espaco

def atualizar_disponibilidade_espaco(db: Session, espaco_id: int, disponivel: bool):
    espaco = obter_espaco_por_id(db, espaco_id)
    if espaco:
        espaco.is_available = disponivel
        db.commit()
        db.refresh(espaco)
    return espaco