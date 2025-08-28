from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.usuario import usuario_router
from fastapi.middleware.cors import CORSMiddleware
from routers.libro import libro_router
from routers.categoria import categoria_router
from routers.prestamo import prestamo_router

app = FastAPI()
app.title = "Mi aplicación con  FastAPI"
app.version = "0.0.1"

origins = [
    "http://127.0.0.1:5500",    # Live Server común
    "http://localhost:5500",     # Live Server localhost
    "http://127.0.0.1:5501",    # Live Server puerto alternativo
    "http://localhost:5501",     # Live Server localhost alternativo
    "http://127.0.0.1:5502",    # Tu puerto original
    "http://localhost:5502",     # Localhost variante
    "http://127.0.0.7:5502",    # Tu configuración original
    "http://localhost:3000",     # React común
    "http://127.0.0.1:3000",    # React 127.0.0.1
    "http://localhost:8080",     # Otro puerto común
    "http://127.0.0.1:8080",    # 8080 en 127.0.0.1
    "null",                      # Para archivos file://
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ErrorHandler)

app.include_router(usuario_router)
app.include_router(libro_router)
app.include_router(categoria_router)
app.include_router(prestamo_router)

Base.metadata.create_all(bind=engine)

