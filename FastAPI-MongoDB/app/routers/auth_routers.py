from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database import usuarios_col
from app.auth.security import verificar_password, crear_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 1. Buscar al usuario por nombre
    usuario_db = usuarios_col.find_one({"nombre": form_data.username})
    
    if not usuario_db:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")

    # 2. Verificar la contraseña (Passlib entra en acción)
    if not verificar_password(form_data.password, usuario_db["password"]):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")

    # 3. Generar el Token JWT
    token = crear_token({"sub": usuario_db["nombre"]})
    
    return {"access_token": token, "token_type": "bearer"}

