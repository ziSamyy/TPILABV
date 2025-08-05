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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.7:5502"],  
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

