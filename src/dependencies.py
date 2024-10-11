import os
from dotenv import load_dotenv
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models.user import User
from models.admin import Admin
from database import get_db
from utils import get_password_hash

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No se pudieron validar los credenciales",
    headers=(),
)


def create_access_token(data: dict) -> str:
    import time

    to_encode: dict = data.copy()
    expire: int = int(time.time()) + ACCESS_TOKEN_EXPIRE_MINUTES * 60
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_admin(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Admin:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        role: str = payload.get("role")
        if role is None or role != "admin":
            raise credentials_exception
        admin = db.query(Admin).filter(Admin.email == email).first()
        if admin is None:
            # Create the admin if it doesn't exist
            admin = Admin(
                name="Admin",
                email=email,
                hashed_password=get_password_hash("password123"),
                role=role,
                is_active=True,
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
        return admin
    except JWTError:
        raise credentials_exception


def get_admin_user(current_user: User = Depends(get_current_admin)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="No hay permisos de admin"
        )
    return current_user


def get_read_write_user(current_user: User = Depends(get_current_admin)) -> User:
    if current_user.role not in ["admin", "read_write"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No hay permisos suficientes para poder usar Read and Write",
        )
    return current_user


def get_read_only_user(current_user: User = Depends(get_current_admin)) -> User:
    if current_user.role not in ["admin", "read_write", "read"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="No hay permisos"
        )
    return current_user


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()  # type: ignore
