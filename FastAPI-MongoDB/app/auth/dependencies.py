from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.auth.security import decodificar_token 
from app.database import usuarios_col

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    payload = decodificar_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    username = payload.get("sub")
    # Buscamos en la base de datos para confirmar que el usuario existe
    usuario = usuarios_col.find_one({"nombre": username})
    
    if usuario is None:
        raise HTTPException(status_code=401, detail="Usuario no existe en la base de datos")
        
    return usuario # Ahora devolvemos todo el objeto del usuario, no solo el nombre
