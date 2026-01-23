from fastapi import APIRouter, Depends, HTTPException
from app.schemas import TransferenciaEsquema # <-- AQUÍ IMPORTAMOS EL ESQUEMA
from app.database import usuarios_col, transferencias_col
from app.auth.dependencies import obtener_usuario_actual

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

# Aquí crearemos el endpoint POST en el siguiente paso...

