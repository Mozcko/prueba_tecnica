from sqlalchemy import Column, Integer, String, Boolean

from database import Base, engine


class User(Base):
    __tablename__ = "user"
    

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    rfc = Column(String, unique=True, index=True)
    curp = Column(String, unique=True, index=True)
    cp = Column(String, index=True)
    phone = Column(String, index=True)
    address = Column(String, index=True)
    date = Column(String, index=True)
    


Base.metadata.create_all(bind=engine)
