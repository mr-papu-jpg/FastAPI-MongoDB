from pydantic import BaseModel
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str
    dinero: int
    esta_activo: Optional[bool] = True

class UsuarioCreate(UsuarioBase):
    password: str  # Solo se pide al crear el usuario

class UsuarioResponse(UsuarioBase):
    id: str  # Para devolver el _id como string

