import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

URL_CLOUD = os.getenv("DATA_BASE_URL_CLOUD")
client = MongoClient(URL_CLOUD)
db = client["mi_proyecto_db"]

# Exportamos la colección para usarla en los routers
usuarios_col = db["usuarios"]

