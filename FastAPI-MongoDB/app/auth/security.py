from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
import os

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
SECRET_KEY = "MI_LLAVE_SUPER_SECRETA" # Debería estar en el .env
ALGORITHM = "HS256"

def obtener_hash(password: str):
    return pwd_context.hash(password)

def verificar_password(password_plana, password_hasheada):
    return pwd_context.verify(password_plana, password_hasheada)

def crear_token(data: dict):
    datos_copia = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=15)
    datos_copia.update({"exp": exp})
    return jwt.encode(datos_copia, SECRET_KEY, algorithm=ALGORITHM)

