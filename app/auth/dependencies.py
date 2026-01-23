from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.database import usuarios_col
from app.auth.utils import verificar_password # Importamos nuestra utilidad
import os

# Configuración básica (Asegúrate de tener tu SECRET_KEY)
SECRET_KEY = "tu_llave_secreta_super_segura"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    usuario = usuarios_col.find_one({"nombre": username})
    if usuario is None:
        raise credentials_exception
    
    return usuario

# Función extra por si tienes el login aquí o para validar credenciales
def autenticar_usuario(nombre: str, password_plano: str):
    usuario = usuarios_col.find_one({"nombre": nombre})
    if not usuario:
        return False
    # Usamos nuestra utilidad para comparar
    if not verificar_password(password_plano, usuario["password"]):
        return False
    return usuario

