from fastapi import APIRouter, HTTPException, Depends
from app.database import usuarios_col
from app.models.user_models import UsuarioCreate, UsuarioResponse
from app.auth.security import obtener_hash # Importante
from bson import ObjectId
from app.auth.dependencies import obtener_usuario_actual

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=UsuarioResponse)
async def crear_usuario(user: UsuarioCreate):
    user_dict = user.dict()
    
    # Aquí ocurre la magia del Hashing (Passlib)
    user_dict["password"] = obtener_hash(user_dict["password"])
    
    resultado = usuarios_col.insert_one(user_dict)
    
    # Devolvemos el objeto con el ID de Mongo
    return {**user_dict, "id": str(resultado.inserted_id)}

@router.get("/")
async def obtener_usuarios():
    usuarios = []
    for u in usuarios_col.find():
        u["id"] = str(u["_id"])
        usuarios.append(u)
    return usuarios

@router.get("/me")
async def leer_mi_perfil(current_user: str = Depends(obtener_usuario_actual)):
    return {"mensaje": f"Hola {current_user}, este es tu perfil privado"}

