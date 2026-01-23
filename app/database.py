'''

import socket

# ESTO ES MAGIA NEGRA PARA DNS
# Mapeamos el nombre del servidor directamente a la IP que sabemos que funciona
def resolver_atlas():
    hosts = [
        "cluster0-shard-00-00.4rsloai.mongodb.net",
        "cluster0-shard-00-01.4rsloai.mongodb.net",
        "cluster0-shard-00-02.4rsloai.mongodb.net"
    ]
    ip_conocida = "18.213.121.217"
    
    old_getaddrinfo = socket.getaddrinfo
    def new_getaddrinfo(*args, **kwargs):
        if args[0] in hosts:
            return old_getaddrinfo(ip_conocida, *args[1:], **kwargs)
        return old_getaddrinfo(*args, **kwargs)
    
    socket.getaddrinfo = new_getaddrinfo

resolver_atlas()
'''
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
URL_CLOUD = os.getenv("DATA_BASE_URL_CLOUD")
usuarios_col = None

try:
    # Aumentamos el tiempo de espera a 10 segundos por si la VPN es lenta
    client = MongoClient(URL_CLOUD, serverSelectionTimeoutMS=10000)
    
    # Probamos la conexión
    client.admin.command('ping')
    
    db = client["mi_proyecto_db"]
    usuarios_col = db["usuarios"]
    transferencias_col = db["transferencias"]
    print("✅ ¡LOGRADO! Conectado a Atlas.")

except Exception as e:
    print(f"❌ Error: {e}")
    import mongomock
    client = mongomock.MongoClient()
    db = client["mi_proyecto_db"]
    usuarios_col = db["usuarios"]
    transferencias_col = db["transferencias"]
    print("⚠️ Usando MONGOMOCK de respaldo.")

