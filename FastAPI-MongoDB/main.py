from fastapi import FastAPI
from app.routers import user_routes

app = FastAPI(title="Mi App Profesional con MongoDB")

# Importante: Incluimos el router
app.include_router(user_routes.router)

@app.get("/")
def inicio():
    return {"mensaje": "API Funcionando correctamente"}

