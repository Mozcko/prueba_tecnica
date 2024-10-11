from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.admin import Admin
from schemas.admin import AdminCreate, AdminOut, AdminUpdate
from dependencies import get_db, get_admin_user, create_access_token
from utils import get_password_hash, verify_password
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

# Token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Obtener todos los admins (solo accesible para admin)
@router.get("/", response_model=list[AdminOut])
def get_admins(
    db: Session = Depends(get_db), current_admin: Admin = Depends(get_admin_user)
):
    admins = db.query(Admin).all()
    return admins


# Actualizar un admin (solo accesible para admin)
@router.put("/{admin_id}", response_model=AdminOut)
def update_admin(
    admin_id: int,
    admin_update: AdminUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_admin_user),
):
    db_admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not db_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Admin no encontrado"
        )

    # Check if the new email already exists
    if admin_update.email and admin_update.email != db_admin.email:
        existing_admin = db.query(Admin).filter(Admin.email == admin_update.email).first()
        if existing_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El correo electrónico ya está en uso"
            )

    for key, value in admin_update.dict(exclude_unset=True).items():
        setattr(db_admin, key, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error de integridad al actualizar el administrador",
        )

    db.refresh(db_admin)
    return db_admin

# Eliminar un admin (solo accesible para admin)
@router.delete("/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(
    admin_id: int,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_admin_user),
):
    db_admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not db_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Admin no encontrado"
        )

    db.delete(db_admin)
    db.commit()
    return {"detail": "Admin eliminado exitosamente"}


# Login para obtener token de administrador
@router.post("/login", response_model=dict)
def login_for_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    # Buscar al administrador por su correo electrónico
    admin: Admin = db.query(Admin).filter(Admin.email == form_data.username).first()

    # Verificar si el administrador existe y si la contraseña es correcta
    if not admin or not verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario o contraseña incorrectos",
        )

    # Crear el token de acceso utilizando la función importada
    access_token = create_access_token(data={"sub": admin.email, "role": admin.role})

    return {"token_de_acceso": access_token}  # tipo de token "bearer"


# Crear un nuevo admin (solo accesible para admin)
@router.post("/register", response_model=AdminOut)
def create_admin(
    admin: AdminCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_admin_user),
):
    db_admin = db.query(Admin).filter(Admin.email == admin.email).first()
    if db_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Correo electrónico ya existente",
        )

    hashed_password = get_password_hash(admin.password)
    new_admin = Admin(
        name=admin.name,
        email=admin.email,
        hashed_password=hashed_password,
        role=admin.role,
        is_active=admin.is_active,
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin
