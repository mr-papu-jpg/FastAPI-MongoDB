from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from app.database import usuarios_col
from app.models.user_models import UsuarioCreate, UsuarioResponse
from app.auth.security import obtener_hash

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=UsuarioResponse)
async def crear_usuario(user: UsuarioCreate):
    # Hashear contraseña antes de guardar
    user_dict = user.dict()
    user_dict["password"] = obtener_hash(user_dict["password"])
    
    resultado = usuarios_col.insert_one(user_dict)
    
    # Creamos la respuesta adaptando el _id
    return {**user.dict(), "id": str(resultado.inserted_id)}

@router.get("/{id}", response_model=UsuarioResponse)
async def obtener_usuario(id: str):
    user = usuarios_col.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user["id"] = str(user["_id"])
    return user

