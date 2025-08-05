from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.jwt_manager import create_token
from schemas.usuario import UserLogin, UserAuth, User
from config.database import get_db
from models.usuarios import User as UserModel
import bcrypt
from middlewares.jwt_bearer import JWTBearer


usuario_router = APIRouter()


@usuario_router.post("/login", tags=["Auth"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if not bcrypt.checkpw(
        user.password.get_secret_value().encode("utf-8"),
        db_user.password.encode("utf-8"),
    ):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token_data = {"id": db_user.id, "email": db_user.email, "rol": db_user.rol}
    token = create_token(token_data)
    return {
        "token": token,
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "rol": db_user.rol,
            "name": db_user.name,
        }
    }


@usuario_router.post("/usuarios", tags=["Usuarios"])
def register(user: UserAuth, db: Session = Depends(get_db)):
    existing_user = (
        db.query(UserModel).filter(UserModel.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    hashed_password = bcrypt.hashpw(
        user.password.get_secret_value().encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    newuser = UserModel(
        name=user.name, email=user.email, password=hashed_password, rol=user.rol
    )

    db.add(newuser)
    db.commit()
    db.refresh(newuser)

    token_data = {"id": newuser.id, "email": newuser.email, "rol": newuser.rol}

    token = create_token(token_data)
    return {
    "token": token,
    "user": newuser
}


@usuario_router.get(
    "/usuarios",
    tags=["Usuarios"],
    response_model=List[User],
    dependencies=[Depends(JWTBearer())],
)
def get_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(UserModel).all()
    return usuarios


@usuario_router.get(
    "/usuarios/{usuario_id}",
    tags=["Usuarios"],
    response_model=User,
    dependencies=[Depends(JWTBearer())],
)
def get_usuario_por_id(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UserModel).filter(UserModel.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@usuario_router.put(
    "/usuarios/{usuario_id}",
    tags=["Usuarios"],
    response_model=User,
    dependencies=[Depends(JWTBearer())],
)
def update_usuario(
    usuario_id: int, user_update: UserAuth, db: Session = Depends(get_db)
):
    usuario = db.query(UserModel).filter(UserModel.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    hashed_password = bcrypt.hashpw(
        user_update.password.get_secret_value().encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    usuario.name = user_update.name
    usuario.email = user_update.email
    usuario.password = hashed_password
    usuario.rol = user_update.rol

    db.commit()
    db.refresh(usuario)

    return usuario


@usuario_router.delete(
    "/usuarios/{usuario_id}", tags=["Usuarios"], dependencies=[Depends(JWTBearer())]
)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(UserModel).filter(UserModel.id == usuario_id).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()

    return {"msg": "Usuario eliminado correctamente"}
