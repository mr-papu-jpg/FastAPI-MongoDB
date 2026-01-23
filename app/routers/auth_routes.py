from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database import usuarios_col
from jose import jwt # Para generar el token aquí mismo
from app.auth.utils import verificar_password, SECRET_KEY, ALGORITHM # Importamos todo de utils

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. Buscar al usuario por nombre en la DB
    usuario_db = usuarios_col.find_one({"nombre": form_data.username})

    if not usuario_db:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    # 2. Verificar la contraseña usando la utilidad centralizada
    if not verificar_password(form_data.password, usuario_db["password"]):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    # 3. Generar el Token JWT usando las constantes unificadas
    # El 'sub' (subject) es el nombre del usuario
    payload = {"sub": usuario_db["nombre"]}
    
    # Creamos el token con la MISMA llave que usa dependencies.py
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}

