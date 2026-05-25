from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv
import os

# ------------------------------------------------------------
# load_dotenv() lee el archivo .env y carga las variables
# como variables de entorno del sistema.
# En Railway no hay .env — las variables se configuran directo
# en el dashboard y llegan igual via os.getenv().
# ------------------------------------------------------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tareas.db")

# ------------------------------------------------------------
# Railway a veces entrega la URL de PostgreSQL con el prefijo
# "postgres://" (viejo formato) en vez de "postgresql://".
# SQLAlchemy solo acepta "postgresql://", así que lo corregimos.
# ------------------------------------------------------------
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# ------------------------------------------------------------
# connect_args solo aplica a SQLite — PostgreSQL no lo necesita.
# ------------------------------------------------------------
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()