import os
from dotenv import load_dotenv
from fastapi import FastAPI

from routes import user, admin
from database import create_db_and_tables, get_db
from utils import create_admin_user
from contextlib import asynccontextmanager

from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        create_db_and_tables()
        db = next(get_db())
        create_admin_user(db)
        yield
    finally:
        pass

app = FastAPI(
    title=os.getenv("APP_TITLE"),
    description=os.getenv("APP_DESCRIPTION"),
    version=os.getenv("APP_VERSION"),
    lifespan=lifespan
)

allowed_hosts = os.getenv("ALLOWED_HOSTS").split(', ')


app.middleware(
    CORSMiddleware,
)

# app.add_middleware(
#     TrustedHostMiddleware,
#     allowed_hosts=allowed_hosts
# )


app.include_router(admin.router, prefix="/admin", tags=["admins"])
app.include_router(user.router, prefix="/users", tags=["users"])


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido a la API de Administración de Usuarios"}
