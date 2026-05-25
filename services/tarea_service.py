from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from models.tarea import Tarea
from schemas.tarea import TareaCrear, TareaActualizar

# ------------------------------------------------------------
# El service contiene toda la lógica de negocio.
# Las rutas no saben nada de la DB — solo llaman al service.
# Es el equivalente al @Service de Spring Boot.
#
# Cada función recibe "db: Session" — la sesión de SQLAlchemy
# que viene inyectada desde el endpoint via Depends(get_db).
# ------------------------------------------------------------

def obtener_todas(db: Session) -> list[Tarea]:
    """Retorna todas las tareas de la base de datos."""
    # db.query(Tarea) → SELECT * FROM tareas
    # .all() ejecuta la query y devuelve una lista
    return db.query(Tarea).all()


def crear(datos: TareaCrear, db: Session) -> Tarea:
    """Crea una nueva tarea y la guarda en la DB."""
    # Creamos la instancia del modelo ORM (no del schema)
    nueva = Tarea(
        titulo=datos.titulo,
        descripcion=datos.descripcion,
        completada=False,
        creada_en=datetime.now().strftime("%d/%m/%Y %H:%M"),
    )
    db.add(nueva)      # INSERT — agrega el objeto a la sesión
    db.commit()        # guarda los cambios en la DB
    db.refresh(nueva)  # recarga el objeto desde la DB para obtener el id generado
    return nueva


def actualizar(id: int, datos: TareaActualizar, db: Session) -> Tarea:
    """Actualiza solo los campos enviados de una tarea."""
    # db.query(Tarea).filter(Tarea.id == id) → SELECT * FROM tareas WHERE id = ?
    # .first() devuelve el primer resultado o None
    tarea = db.query(Tarea).filter(Tarea.id == id).first()

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # exclude_unset=True → solo incluye los campos que el cliente realmente mandó
    # Así un PATCH con solo {"completada": true} no pisa titulo ni descripcion
    cambios = datos.model_dump(exclude_unset=True)

    for campo, valor in cambios.items():
        # setattr(objeto, "campo", valor) es equivalente a objeto.campo = valor
        # pero funciona con nombres de campo dinámicos (strings)
        setattr(tarea, campo, valor)

    db.commit()
    db.refresh(tarea)
    return tarea


def eliminar(id: int, db: Session) -> None:
    """Elimina una tarea por id."""
    tarea = db.query(Tarea).filter(Tarea.id == id).first()

    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    db.delete(tarea)  # DELETE FROM tareas WHERE id = ?
    db.commit()