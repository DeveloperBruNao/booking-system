from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv

load_dotenv()

CHAVE_SECRETA = os.getenv("SECRET_KEY", "chave-secreta-dev")
ALGORITMO = "HS256"
TEMPO_EXPIRACAO_TOKEN_MINUTOS = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def verificar_senha(senha_plana, senha_criptografada):
    return pwd_context.verify(senha_plana, senha_criptografada)

def criptografar_senha(senha):
    return pwd_context.hash(senha)

def criar_token_acesso(dados: dict):
    dados_para_codificar = dados.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=TEMPO_EXPIRACAO_TOKEN_MINUTOS)
    dados_para_codificar.update({"exp": expiracao})
    token_jwt = jwt.encode(dados_para_codificar, CHAVE_SECRETA, algorithm=ALGORITMO)
    return token_jwt

def verificar_token(token: str):
    """
    Verifica e decodifica um token JWT
    """
    try:
        payload = jwt.decode(token, CHAVE_SECRETA, algorithms=[ALGORITMO])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível validar as credenciais",
        )

def obter_usuario_atual(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependência para obter o usuário atual a partir do token
    """
    token = credentials.credentials
    payload = verificar_token(token)
    return payload