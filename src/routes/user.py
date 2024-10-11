from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from models.admin import Admin
from schemas.user import UserCreate, UserOut, UserUpdate
from dependencies import (
    get_db,
    get_admin_user,
    get_read_write_user,
    get_read_only_user,
)
from utils import (
    get_password_hash,
    validate_curp,
    validate_rfc,
    validate_cp,
    validate_phone,
    validate_date,
)

router = APIRouter()

# Crear usuario
@router.post("/", response_model=UserOut)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_admin_user),
):

    # Validar CURP, RFC, CP, teléfono, y fecha
    if user.curp:
        validate_curp(user.curp)
    if user.rfc:
        validate_rfc(user.rfc)
    if user.cp:
        validate_cp(user.cp)
    if user.phone:
        validate_phone(user.phone)
    if user.date:
        validate_date(user.date)

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="el correo electrónico usado ya existe",
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        is_active=user.is_active,
        rfc=user.rfc,
        curp=user.curp,
        cp=user.cp,
        phone=user.phone,
        address=user.address,
        date=user.date,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Obtener lista de usuarios
@router.get("/", response_model=list[UserOut])
def read_users(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_read_only_user),
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users


# Obtener usuario por ID
@router.get("/{user_id}", response_model=UserOut)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_read_only_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado o inexistente",
        )
    return user


# Actualizar usuario
@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_read_write_user),
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado o inexistente",
        )

    # Validar campos antes de actualizar
    if user_update.curp:
        validate_curp(user_update.curp)
    if user_update.rfc:
        validate_rfc(user_update.rfc)
    if user_update.cp:
        validate_cp(user_update.cp)
    if user_update.phone:
        validate_phone(user_update.phone)
    if user_update.date:
        validate_date(user_update.date)

    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


# Eliminar usuario
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_admin_user),
):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado o inexistente",
        )

    db.delete(db_user)
    db.commit()
    return {"detail": "usuario eliminado exitosamente"}
