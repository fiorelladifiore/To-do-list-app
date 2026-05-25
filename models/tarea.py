from sqlalchemy import Column, Integer, String, Boolean
from database import Base

# ------------------------------------------------------------
# Esta clase representa la tabla "tareas" en SQLite.
# Es el equivalente a una @Entity en JPA/Spring Boot.
# Cada atributo Column es una columna de la tabla.
# ------------------------------------------------------------
class Tarea(Base):
    __tablename__ = "tareas"

    # primary_key=True → clave primaria, autoincremental por defecto en SQLite
    id = Column(Integer, primary_key=True, index=True)

    # nullable=False → equivalente a @Column(nullable=false) en JPA
    titulo = Column(String, nullable=False)

    # nullable=True es el default, la descripción es opcional
    descripcion = Column(String, nullable=True)

    # default=False → si no se especifica, la tarea arranca como no completada
    completada = Column(Boolean, default=False)

    # Guardamos la fecha como string formateado (simple para este proyecto)
    creada_en = Column(String, nullable=False)