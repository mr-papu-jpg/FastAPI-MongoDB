import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Cargar variables de entorno
load_dotenv()

app = FastAPI()

# Conexión usando .env
URL_CLOUD = os.getenv("DATA_BASE_URL_CLOUD")
conexion = MongoClient(URL_CLOUD)
db = conexion["mi_proyecto_db"]
usuarios_col = db["usuarios"]

class Usuario(BaseModel):
    # Nota: No incluyas 'id' aquí si quieres que Mongo lo genere solo
    nombre: str
    dinero: int
    esta_activo: Optional[bool] = True

@app.post("/usuarios/")
async def crear_usuario(user: Usuario):
    user_dict = user.dict()
    # MongoDB genera el ID automáticamente
    resultado = usuarios_col.insert_one(user_dict)
    return {"id": str(resultado.inserted_id), "msg": "Usuario guardado en la nube"}

@app.get("/usuarios/")
async def obtener_usuarios():
    usuarios = []
    for user in usuarios_col.find():
        # IMPORTANTE: Convertir _id de Mongo a string
        user["_id"] = str(user["_id"])
        usuarios.append(user)
    return usuarios

@app.get("/usuarios/{id}")
async def obtener_usuario(id: str):
    # Siempre busca por "_id"
    user = usuarios_col.find_one({"_id": ObjectId(id)})
    if user:
        user["_id"] = str(user["_id"])
        return user
    raise HTTPException(status_code=404, detail="No encontrado")

@app.put("/usuarios/{id}")
async def actualizar_usuario(id: str, nuevos_datos: dict): # Corregido ': dict'
    resultado = usuarios_col.update_one(
        {"_id": ObjectId(id)},
        {"$set": nuevos_datos}
    )
    if resultado.modified_count == 1:
        return {"msg": "Actualizado con éxito"}
    raise HTTPException(status_code=404, detail="No se encontró o no hubo cambios")

@app.delete("/usuarios/{id}")
async def borrar_usuario(id: str):
    # delete_one devuelve un objeto con la cuenta de borrados
    resultado = usuarios_col.delete_one({"_id": ObjectId(id)})
    
    if resultado.deleted_count == 1:
        return {"msg": "Usuario eliminado correctamente"}
    
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

