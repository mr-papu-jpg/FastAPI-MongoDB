from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os
from passlib.context import CryptContext

# Centralizamos aquí:
SECRET_KEY = "mi_clave_secreta_ultra_fija_123"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def obtener_hash(password: str):
    return pwd_context.hash(password)

def verificar_password(password_plana, password_hasheada):
    return pwd_context.verify(password_plana, password_hasheada)

def crear_token(data: dict):
    datos_copia = data.copy()
    exp = datetime.utcnow() + timedelta(minutes=15)
    datos_copia.update({"exp": exp})
    return jwt.encode(datos_copia, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_token(token: str):
    try:
        # Intentamos abrir el sobre (el token) con nuestra llave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Si todo está bien, devuelve los datos (el "sub")
    except JWTError:
        # Si el token es falso, expiró o está roto, devolvemos None
        return None
