import os
from pymongo import MongoClient
from dotenv import load_dotenv
import mongomock

# Esto crea una base de datos falsa que funciona IGUAL que la real
client = mongomock.MongoClient()
db = client["mi_proyecto_db"]
usuarios_col = db["usuarios"]


load_dotenv()

# Cambiamos a la variable local que ya tienes
URL_LOCAL = os.getenv("DATA_BASE_URL")

# Si por alguna razón el .env no carga, usamos el default de mongo
client = MongoClient(URL_LOCAL or "mongodb://localhost:27017/")
