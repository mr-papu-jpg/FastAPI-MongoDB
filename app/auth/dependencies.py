from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.database import usuarios_col
from app.auth.utils import SECRET_KEY, ALGORITHM # Importamos las constantes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    # Definimos la excepción que lanzaremos si algo sale mal
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 1. Decodificamos el payload usando la SECRET_KEY importada
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # 2. Extraemos el 'sub' (nombre de usuario)
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        # Si el token expiró, la firma no coincide o es inválido
        raise credentials_exception

    # 3. Buscamos al usuario en la BD
    usuario = usuarios_col.find_one({"nombre": username})

    if usuario is None:
        # Útil para debug en Termux: si el servidor se reinició y borró la RAM
        print(f"⚠️ ERROR: El usuario '{username}' no existe en la base de datos actual.")
        raise credentials_exception

    return usuario

