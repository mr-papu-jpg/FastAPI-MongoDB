from fastapi import FastAPI
# 1. Importar la base de datos y colecciones primero
from app.database import usuarios_col, transferencias_col 
from app.routers import user_routes, auth_routes, transacciones

app = FastAPI()

# 2. Definir la función Seed (o importarla)
def ejecutar_seed():
    # Importación local para evitar errores de carga circular
    from app.auth.utils import obtener_password_hash 
    
    # Aquí ya existe usuarios_col porque lo importamos arriba
    if usuarios_col.count_documents({}) == 0:
        print("🌱 Sembrando datos iniciales (Seed)...")
        usuarios_de_prueba = [
            {
                "nombre": "Angstart",
                "dinero": 2000.0,
                "password": obtener_password_hash("password123"),
                "esta_activo": True
            },
            {
                "nombre": "UsuarioB",
                "dinero": 500.0,
                "password": obtener_password_hash("password123"),
                "esta_activo": True
            }
        ]
        usuarios_col.insert_many(usuarios_de_prueba)
        print("✅ Seed completado.")
    else:
        print("🌲 La base de datos ya tiene usuarios.")

# 3. Incluir los routers
app.include_router(user_routes.router)
app.include_router(auth_routes.router)
app.include_router(transacciones.router)

# 4. EJECUTAR EL SEED AL FINAL
# Esto garantiza que todo lo anterior ya cargó
ejecutar_seed()

@app.get("/")
def home():
    return {"message": "API Financiera con Seed Automático activa"}

