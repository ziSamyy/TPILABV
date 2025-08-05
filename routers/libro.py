from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from schemas.book import Book, BookWithCategory
from config.database import get_db
from models.libros import Book as LibroModel
from models.categorias import Category as CategoriaModel
from middlewares.jwt_bearer import JWTBearer
from routers.categoria import categoria_router

libro_router = APIRouter()

@libro_router.post("/libros", tags=["Libros"], response_model=Book,
    dependencies=[Depends(JWTBearer())])
def create_libro(libro: Book, db: Session = Depends(get_db)):
    categoria = db.query(CategoriaModel).filter(CategoriaModel.id == libro.categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    newbook = LibroModel(
    title=libro.title,
    author=libro.author,
    isbn=libro.isbn,
    publisher=libro.publisher,
    category_id=libro.category_id,
    amount=libro.amount,
    image=libro.image
)
    db.add(newbook)
    db.commit()
    db.refresh(newbook)
    return newbook

@libro_router.get("/libros", tags=["Libros"], response_model=List[BookWithCategory])
def get_libros(db: Session = Depends(get_db)):
    libros = db.query(LibroModel).options(joinedload(LibroModel.categoria)).all()
    return libros
    
@libro_router.get("/libros/{libro_id}", tags=["Libros"], response_model=BookWithCategory)
def get_libro_por_id(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(LibroModel).options(joinedload(LibroModel.categoria)).filter(LibroModel.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@libro_router.put("/libros/{libro_id}", tags=["Libros"], response_model=Book,
    dependencies=[Depends(JWTBearer())])
def update_libro(libro_id: int, libro_update: Book, db: Session = Depends(get_db)):
    libro = db.query(LibroModel).filter(LibroModel.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    categoria = db.query(CategoriaModel).filter(CategoriaModel.id == libro_update.categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")

    libro.title = libro_update.title
    libro.author = libro_update.author
    libro.isbn = libro_update.isbn
    libro.publisher = libro_update.publisher
    libro.category_id = libro_update.category_id
    libro.amount = libro_update.amount
    libro.image = libro_update.image


    db.commit()
    db.refresh(libro)
    return libro
    
@libro_router.delete("/libros/{libro_id}", tags=["Libros"],
    dependencies=[Depends(JWTBearer())])
def delete_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = db.query(LibroModel).filter(LibroModel.id == libro_id).first()
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    db.delete(libro)
    db.commit()
    return {"msg": "Libro eliminado correctamente"}