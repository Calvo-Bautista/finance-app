from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config.database import db
from app.config.settings import settings
from app.routes import auth

# Lifespan events: Reemplaza a @app.on_event("startup")
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicio: Conectar DB
    db.connect()
    yield
    # Cierre: Desconectar DB
    db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    lifespan=lifespan
)

# Configuración de CORS (Permitir frontend React)
origins = [
    "http://localhost:3000", # React local por defecto
    "http://localhost:5173", # Vite local por defecto
    # Añadir dominios de producción aquí
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Finanzas Personales", "docs": "/docs"}

# Aquí importaremos los routers en fases futuras
# app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])