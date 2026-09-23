from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config import settings
from database import get_db
from models import Usuario

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash('dummy-verification-password')
oauth2 = OAuth2PasswordBearer(tokenUrl='auth/login')


def criar_token(usuario_id: int):
    now = datetime.now(timezone.utc)
    return jwt.encode({'sub': str(usuario_id), 'iat': now,
                       'exp': now + timedelta(minutes=settings.token_minutes)},
                      settings.jwt_secret, algorithm='HS256')


def usuario_atual(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    error = HTTPException(401, 'Credenciais inválidas ou expiradas', headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=['HS256'],
                             options={'require': ['sub', 'exp', 'iat']})
        usuario_id = int(payload['sub'])
    except (jwt.InvalidTokenError, ValueError, TypeError):
        raise error
    usuario = db.get(Usuario, usuario_id)
    if usuario is None:
        raise error
    return usuario


def administrador(usuario: Usuario = Depends(usuario_atual)):
    if not usuario.is_admin:
        raise HTTPException(403, 'Apenas administradores podem alterar o catálogo')
    return usuario
