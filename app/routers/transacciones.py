from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import TransferenciaEsquema
from app.database import usuarios_col, transferencias_col
from app.auth.dependencies import obtener_usuario_actual
from datetime import datetime
from app.services.finance_service import FinanceService

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

@router.post("/enviar")
async def ejecutar_transferencia(
    datos: TransferenciaEsquema, 
    usuario_emisor: dict = Depends(obtener_usuario_actual)
):

     # ¡Toda la lógica ahora vive en una sola línea!
    nuevo_saldo = FinanceService.procesar_transferencia(
        usuario_emisor, datos.receptor, datos.monto, datos.comentario
    )

    return {
        "status": "success",
        "message": f"Transferencia exitosa a {datos.receptor}",
        "nuevo_saldo": nuevo_saldo
    }

@router.get("/historial")
async def ver_mi_historial(usuario: dict = Depends(obtener_usuario_actual)):
    # Buscamos donde el usuario sea emisor O receptor
    query = {
        "$or": [
            {"emisor": usuario["nombre"]},
            {"receptor": usuario["nombre"]}
        ]
    }
    historial = list(transferencias_col.find(query).sort("fecha", -1))
    
    for t in historial:
        t["_id"] = str(t["_id"])
        
    return {"total": len(historial), "transacciones": historial}

