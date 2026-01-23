from fastapi import HTTPException, status
from app.database import usuarios_col, transferencias_col
from datetime import datetime

class FinanceService:
    @staticmethod
    def procesar_transferencia(emisor_doc, receptor_nombre, monto, comentario):
        # 1. Validaciones
        if emisor_doc["nombre"] == receptor_nombre:
            raise HTTPException(status_code=400, detail="Autotransferencia no permitida")
        
        if emisor_doc["dinero"] < monto:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")
            
        receptor = usuarios_col.find_one({"nombre": receptor_nombre})
        if not receptor:
            raise HTTPException(status_code=404, detail="Receptor no existe")

        # 2. Ejecución
        usuarios_col.update_one({"_id": emisor_doc["_id"]}, {"$inc": {"dinero": -monto}})
        usuarios_col.update_one({"_id": receptor["_id"]}, {"$inc": {"dinero": monto}})

        # 3. Registro
        registro = {
            "emisor": emisor_doc["nombre"],
            "receptor": receptor_nombre,
            "monto": monto,
            "comentario": comentario,
            "fecha": datetime.utcnow()
        }
        transferencias_col.insert_one(registro)
        return emisor_doc["dinero"] - monto

