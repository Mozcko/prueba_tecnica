import re
import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.admin import Admin
from sqlalchemy.orm import Session

load_dotenv()

CURP_REGEX = r"^[A-Z]{4}\d{6}[H|M][A-Z]{5}[A-Z0-9]{2}$"
RFC_REGEX = r"^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$"
CP_REGEX = r"^\d{5}$"
PHONE_REGEX = r"^\d{10}$"
DATE_REGEX = r"^\d{2}-\d{2}-\d{4}$"

pwd_context = CryptContext(schemes=["bcrypt"], default="bcrypt", deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> CryptContext:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> CryptContext:
    return pwd_context.hash(password)


def validate_curp(curp: str) -> None:
    if not re.match(CURP_REGEX, curp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El CURP no esta en el formato oficial",
        )


def validate_rfc(rfc: str) -> None:
    if not re.match(RFC_REGEX, rfc):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El RFC no esta en el formato oficial",
        )


def validate_cp(cp: str) -> None:
    if not re.match(CP_REGEX, cp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El código postal no esta en el formato oficial",
        )


def validate_phone(phone: str) -> None:
    if not re.match(PHONE_REGEX, phone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de teléfono no esta en el formato oficial",
        )


def validate_date(date: str) -> None:
    if not re.match(DATE_REGEX, date):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha no esta en el formato oficial",
        )


def handle_validate_error(message: str) -> None:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message,
    )


# Función para crear un usuario administrador hardcoded
def create_admin_user(db: Session) -> None:
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    admin_name = os.getenv("ADMIN_NAME")
    admin_role = os.getenv("ADMIN_ROLE")

    # Verificar si el usuario administrador ya existe
    existing_admin = db.query(Admin).filter(Admin.email == admin_email).first()
    if existing_admin is None:
        hashed_password = get_password_hash(admin_password)
        new_admin = Admin(
            name=admin_name,
            email=admin_email,
            hashed_password=hashed_password,
            role=admin_role,
            is_active=True,
        )
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
