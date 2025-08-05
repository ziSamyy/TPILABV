from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from config.database import get_db
from schemas.prestamo import Lending
from models.prestamos import Lending as LendingModel
from middlewares.jwt_bearer import JWTBearer
from utils.jwt_manager import validate_token
from models.libros import Book as LibroModel


prestamo_router = APIRouter()

@prestamo_router.post("/prestamos", tags=["Préstamos"], response_model=Lending,
    dependencies=[Depends(JWTBearer())])
def crear_prestamo(prestamo: Lending, db: Session = Depends(get_db)):
    libro = db.query(LibroModel).filter(LibroModel.id == prestamo.book_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    if libro.cantidad == 0:
        raise HTTPException(status_code=400, detail="El libro ya está prestado")

    newlending = LendingModel(
        book_id=prestamo.book_id,
        user_id=prestamo.user_id,
        lending_date=prestamo.lending_date,
        return_date=prestamo.return_date
    )
    db.add(newlending)

    libro.amount = 0

    db.commit()
    db.refresh(newlending)

    return newlending


@prestamo_router.get("/prestamos", tags=["Prestamos"], response_model=List[Lending])
def obtenerPrestamos(
    request: Request,
    usuario_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Token no proporcionado")

    token = auth_header.split(" ")[1]
    datos_token = validate_token(token)
    id_token = datos_token.get("id")
    rol = datos_token.get("rol", "").lower()

    if rol == "bibliotecario":
        if usuario_id is not None:
            return db.query(LendingModel).filter(LendingModel.user_id == usuario_id).all()
        return db.query(LendingModel).all()


    if usuario_id is not None and usuario_id != id_token:
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a estos préstamos")

    return db.query(LendingModel).filter(LendingModel.user_id == id_token).all()


@prestamo_router.get("/prestamos/{prestamoId}", tags=["Prestamos"], response_model=Lending, dependencies=[Depends(JWTBearer())])
def obtenerPrestamoPorId(prestamoId: int, db: Session = Depends(get_db)):
    prestamo = db.query(LendingModel).filter(LendingModel.id == prestamoId).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return prestamo

@prestamo_router.put("/prestamos/{prestamoId}", tags=["Prestamos"], dependencies=[Depends(JWTBearer())])
def actualizarPrestamo(prestamoId: int, prestamoActualizado: Lending, db: Session = Depends(get_db)):
    prestamo = db.query(LendingModel).filter(LendingModel.id == prestamoId).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    prestamo.book_id = prestamoActualizado.book_id
    prestamo.user_id = prestamoActualizado.user_id
    prestamo.lending_date = prestamoActualizado.lending_date
    prestamo.return_date = prestamoActualizado.return_date

    db.commit()
    db.refresh(prestamo)
    return {"msg": "Préstamo actualizado correctamente", "prestamo": prestamo}

@prestamo_router.delete("/prestamos/{prestamoId}", tags=["Prestamos"], dependencies=[Depends(JWTBearer())])
def eliminarPrestamo(prestamoId: int, db: Session = Depends(get_db)):
    prestamo = db.query(LendingModel).filter(LendingModel.id == prestamoId).first()
    if not prestamo:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

    libro = db.query(LibroModel).filter(LibroModel.id == prestamo.book_id).first()
    if libro:
        libro.amount = 1

    db.delete(prestamo)
    db.commit()

    return {"msg": "Préstamo eliminado correctamente y libro restablecido"}
