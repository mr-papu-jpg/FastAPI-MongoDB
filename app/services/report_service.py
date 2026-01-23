import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

# Rutas base
STATIC_DIR = "static/reportes"

class ReportService:
    
    @staticmethod
    def generar_csv_transacciones(historial):
        """Convierte una lista de transacciones en un archivo CSV."""
        if not historial:
            return None
        
        # Limpiamos los datos para el CSV (quitamos el _id de MongoDB)
        for t in historial:
            t.pop('_id', None)
        
        df = pd.DataFrame(historial)
        filename = f"transacciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(STATIC_DIR, "csv", filename)
        
        df.to_csv(filepath, index=False)
        return filepath

    @staticmethod
    def generar_pdf_usuarios(usuarios):
        """Crea un PDF con la lista de usuarios y su dinero actual."""
        filename = f"reporte_usuarios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(STATIC_DIR, "pdf", filename)
        
        c = canvas.Canvas(filepath, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, 750, "REPORTE GENERAL DE USUARIOS")
        c.setFont("Helvetica", 12)
        c.drawString(100, 730, f"Fecha de creación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.line(100, 720, 500, 720)
        
        y = 690
        for u in usuarios:
            texto = f"Usuario: {u['nombre']} | Saldo: ${u['dinero']}"
            c.drawString(100, y, texto)
            y -= 20 # Bajar una línea
            if y < 50: # Crear página nueva si se acaba el espacio
                c.showPage()
                y = 750
        
        c.save()
        return filepath

