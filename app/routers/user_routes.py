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

@router.get("/me", response_model=UsuarioResponse)
async def leer_mi_perfil(usuario: dict = Depends(obtener_usuario_actual)):
    # Como ya devolvemos el objeto usuario desde la dependencia,
    # solo tenemos que formatear el ID para Pydantic
    usuario["id"] = str(usuario["_id"])
    return usuario

@router.get("/{user_id}", response_model=UsuarioResponse)
async def obtener_usuario(user_id: str, current_user: dict = Depends(obtener_usuario_actual)):
    # Verificamos si el ID que solicita es el suyo
    if str(current_user["_id"]) != user_id:
        raise HTTPException(
            status_code=403, 
            detail="No tienes permiso para ver la información de otros usuarios"
        )
    
    usuario = usuarios_col.find_one({"_id": ObjectId(user_id)})
    usuario["id"] = str(usuario["_id"])
    return usuario
