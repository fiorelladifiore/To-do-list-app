from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from database import engine, Base
from routes import tareas

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API")

# ------------------------------------------------------------
# En producción, FRONTEND_URL viene de la variable de entorno
# que configurás en Railway con la URL de tu app en Vercel.
# En local usa localhost como fallback.
# Ejemplo en Railway: FRONTEND_URL=https://mi-todo.vercel.app
# ------------------------------------------------------------
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        frontend_url,
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tareas.router)

@app.get("/")
def raiz():
    return {"mensaje": "API de tareas funcionando ✓", "docs": "/docs"}