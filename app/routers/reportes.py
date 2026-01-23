from fastapi import APIRouter, Depends
from app.database import transferencias_col, usuarios_col
from app.services.report_service import ReportService
from app.auth.dependencies import obtener_usuario_actual

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/exportar-mis-transacciones")
async def exportar_csv(usuario: dict = Depends(obtener_usuario_actual)):
    # Buscamos su historial
    query = {"$or": [{"emisor": usuario["nombre"]}, {"receptor": usuario["nombre"]}]}
    historial = list(transferencias_col.find(query))
    
    archivo = ReportService.generar_csv_transacciones(historial)
    return {"status": "CSV Generado", "ruta": archivo}

@router.get("/admin/pdf-usuarios")
async def exportar_pdf(usuario: dict = Depends(obtener_usuario_actual)):
    # Solo un ejemplo: podrías poner seguridad para que solo el admin lo haga
    usuarios = list(usuarios_col.find({}, {"password": 0}))
    archivo = ReportService.generar_pdf_usuarios(usuarios)
    return {"status": "PDF Generado", "ruta": archivo}

