from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UsuarioCriar
from app.auth.security import criptografar_senha, verificar_senha

def obter_usuario_por_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def criar_usuario(db: Session, usuario: UsuarioCriar):
    senha_criptografada = criptografar_senha(usuario.senha)
    db_usuario = User(
        email=usuario.email,
        hashed_password=senha_criptografada,
        full_name=usuario.nome_completo
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def autenticar_usuario(db: Session, email: str, senha: str):
    usuario = obter_usuario_por_email(db, email)
    if not usuario:
        return False
    if not verificar_senha(senha, usuario.hashed_password):
        return False
    return usuario