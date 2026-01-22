from fastapi import FastAPI
from app.routers import user_routes, auth_routers

app = FastAPI(title="Mi App Profesional con MongoDB")

# Importante: Incluimos el router
app.include_router(user_routes.router)
app.include_router(auth_routers.router)

@app.get("/")
def inicio():
    return {"mensaje": "API Funcionando correctamente"}

