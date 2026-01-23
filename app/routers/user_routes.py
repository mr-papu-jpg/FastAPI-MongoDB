from fastapi import APIRouter, HTTPException, Depends, status
from app.database import usuarios_col
from app.auth.utils import obtener_password_hash # Importamos nuestra utilidad
from app.auth.dependencies import obtener_usuario_actual
from pydantic import BaseModel

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Esquema para el registro
class UserRegister(BaseModel):
    nombre: str
    password: str
    dinero: float = 0.0

@router.post("/")
async def registrar_usuario(usuario: UserRegister):
    # Verificar si ya existe
    if usuarios_col.find_one({"nombre": usuario.nombre}):
        raise HTTPException(status_code=400, detail="El usuario ya existe")
    
    # Cifrar la contraseña usando nuestra función centralizada
    password_cifrada = obtener_password_hash(usuario.password)
    
    nuevo_usuario = {
        "nombre": usuario.nombre,
        "password": password_cifrada,
        "dinero": usuario.dinero,
        "esta_activo": True
    }
    
    usuarios_col.insert_one(nuevo_usuario)
    return {"message": "Usuario creado con éxito", "nombre": usuario.nombre}

@router.get("/me")
async def leer_perfil(usuario: dict = Depends(obtener_usuario_actual)):
    # No devolvemos el password por seguridad
    usuario.pop("password", None)
    usuario["_id"] = str(usuario["_id"])
    return usuario

@router.get("/saldo")
async def consultar_saldo(usuario: dict = Depends(obtener_usuario_actual)):
    return {"nombre": usuario["nombre"], "dinero": usuario["dinero"]}

@router.get("/buscar/{nombre_buscado}")
async def buscar_usuario(nombre_buscado: str, usuario_actual: dict = Depends(obtener_usuario_actual)):
    # Buscamos usuarios que contengan ese nombre (regex) sin mostrar password
    resultados = list(usuarios_col.find(
        {"nombre": {"$regex": nombre_buscado, "$options": "i"}},
        {"password": 0, "_id": 0}
    ))
    return {"resultados": resultados}

