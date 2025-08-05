from typing import  List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.category import Category
from models.categorias import Category as CategoryModel
from config.database import get_db
from middlewares.jwt_bearer import JWTBearer

categoria_router = APIRouter()

@categoria_router.post("/categorias", tags=["Categorias"], response_model=Category, dependencies=[Depends(JWTBearer())])
def create_categoria(categoria: Category, db: Session = Depends(get_db)):
    existing_categoria = db.query(CategoryModel).filter(CategoryModel.name == categoria.name).first()
    if existing_categoria:
        raise HTTPException(status_code=400, detail="La categoria ya está registrada")
    new_category = CategoryModel(
        name = categoria.name,
        description = categoria.description
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@categoria_router.put("/categorias/{categorias_id}", tags=["Categorias"],
    dependencies=[Depends(JWTBearer())])
def update_categoria(categoria_id: int, categoria_update: Category, db: Session = Depends(get_db)):
    categoria = db.query(CategoryModel).filter(CategoryModel.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    categoria.name = categoria_update.name
    categoria.description = categoria_update.description
    db.commit()
    db.refresh(categoria)
    return {"msg": "Categoria actualizado correctamente", "categoria": categoria}


@categoria_router.get("/categorias", tags=["Categorias"], response_model=List[Category])
def get_categoria( db: Session = Depends(get_db)):
    categoria = db.query(CategoryModel).all()
    return categoria


@categoria_router.get("/categorias/{categoria_id}", tags=["Categorias"], response_model=Category)
def get_categoria_por_id(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(CategoryModel).filter(CategoryModel.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria


@categoria_router.delete("/categorias/{categoria_id}", tags=["Categorias"],
    dependencies=[Depends(JWTBearer())])
def delete_categoria(categoria_id: int , db: Session = Depends(get_db)):
    categoria = db.query(CategoryModel).filter(CategoryModel.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrado")
    db.delete(categoria)
    db.commit()
    return {"msg": "Categoria eliminado correctamente"}