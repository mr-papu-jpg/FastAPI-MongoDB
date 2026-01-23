from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import TransferenciaEsquema
from app.database import usuarios_col, transferencias_col
from app.auth.dependencies import obtener_usuario_actual
from datetime import datetime

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

@router.post("/enviar")
async def ejecutar_transferencia(
    datos: TransferenciaEsquema, 
    usuario_emisor: dict = Depends(obtener_usuario_actual)
):
    # 1. No permitir enviarse dinero a uno mismo
    if usuario_emisor["nombre"] == datos.receptor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No puedes enviarte dinero a ti mismo."
        )

    # 2. Verificar que el emisor tenga saldo suficiente
    if usuario_emisor["dinero"] < datos.monto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Saldo insuficiente. Tienes {usuario_emisor['dinero']} y quieres enviar {datos.monto}"
        )

    # 3. Verificar que el receptor exista en la base de datos
    receptor = usuarios_col.find_one({"nombre": datos.receptor})
    if not receptor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El usuario receptor no existe."
        )

    # --- INICIO DE LA OPERACIÓN ---

    # 4. Restar dinero al emisor
    usuarios_col.update_one(
        {"_id": usuario_emisor["_id"]},
        {"$inc": {"dinero": -datos.monto}}
    )

    # 5. Sumar dinero al receptor
    usuarios_col.update_one(
        {"_id": receptor["_id"]},
        {"$inc": {"dinero": datos.monto}}
    )

    # 6. Crear el registro del historial (Audit Log)
    nueva_transferencia = {
        "emisor": usuario_emisor["nombre"],
        "receptor": datos.receptor,
        "monto": datos.monto,
        "comentario": datos.comentario,
        "fecha": datetime.utcnow()
    }
    
    # Guardamos en la colección de transferencias
    transferencias_col.insert_one(nueva_transferencia)

    return {
        "status": "success",
        "message": f"Transferencia exitosa de {datos.monto} a {datos.receptor}",
        "nuevo_saldo": usuario_emisor["dinero"] - datos.monto
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
    # .sort("fecha", -1) para ver las más recientes primero
    historial = list(transferencias_col.find(query).sort("fecha", -1))
    
    # Limpiamos los IDs de MongoDB para que sean JSON serializables
    for t in historial:
        t["_id"] = str(t["_id"])
        
    return {"total": len(historial), "transacciones": historial}

