import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import os

# Configuración de rutas absoluta para Termux
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CSV_DIR = os.path.join(BASE_DIR, "static", "reportes", "csv")
PDF_DIR = os.path.join(BASE_DIR, "static", "reportes", "pdf")

# Aseguramos que las carpetas existan al importar el servicio
os.makedirs(CSV_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

class ReportService:
    
    @staticmethod
    def generar_csv_transacciones(historial):
        if not historial:
            print("⚠️ DEBUG: No hay historial para exportar CSV.")
            return None
        
        # Limpieza de datos (quitar _id de Mongo)
        datos = []
        for t in historial:
            item = t.copy()
            item.pop('_id', None)
            datos.append(item)
            
        df = pd.DataFrame(datos)
        filename = f"transacciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(CSV_DIR, filename)
        
        df.to_csv(filepath, index=False)
        print(f"✅ CSV Creado en: {filepath}")
        return filepath

    @staticmethod
    def generar_pdf_usuarios(usuarios):
        """Crea un PDF con la lista de usuarios y su saldo."""
        filename = f"reporte_usuarios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(PDF_DIR, filename)
        
        try:
            c = canvas.Canvas(filepath, pagesize=letter)
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, 750, "REPORTE GENERAL DE USUARIOS")
            
            c.setFont("Helvetica", 12)
            c.drawString(100, 730, f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            c.line(100, 720, 500, 720)
            
            y = 690
            for u in usuarios:
                texto = f"Usuario: {u['nombre']} | Saldo: ${u.get('dinero', 0)}"
                c.drawString(100, y, texto)
                y -= 20
                if y < 50:
                    c.showPage()
                    y = 750
            
            c.save()
            print(f"✅ PDF Creado en: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Error creando PDF: {e}")
            return None

