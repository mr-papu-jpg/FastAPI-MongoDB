import json
import os
from mongomock import MongoClient

# Ruta del archivo donde guardaremos los datos
DB_FILE = "database_persistence.json"

client = MongoClient()
db = client["billetera_db"]
usuarios_col = db["usuarios"]
transferencias_col = db["transferencias"]

def guardar_datos_a_disco():
    """Vuelca el contenido de mongomock a un archivo JSON."""
    datos = {
        "usuarios": list(usuarios_col.find({}, {"_id": 0})),
        "transferencias": list(transferencias_col.find({}, {"_id": 0}))
    }
    with open(DB_FILE, "w") as f:
        json.dump(datos, f, indent=4)
    print("💾 Datos guardados en disco.")

def cargar_datos_desde_disco():
    """Carga los datos del archivo JSON a mongomock al arrancar."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            datos = json.load(f)
            if datos["usuarios"]:
                usuarios_col.insert_many(datos["usuarios"])
            if datos["transferencias"]:
                transferencias_col.insert_many(datos["transferencias"])
        print(f"📂 Datos cargados desde {DB_FILE}")
    else:
        print("🆕 No hay base de datos previa. Iniciando limpia.")

# Cargar al importar el módulo
cargar_datos_desde_disco()

