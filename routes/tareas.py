from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.tarea import TareaCrear, TareaActualizar, TareaRespuesta
from services import tarea_service

# ------------------------------------------------------------
# APIRouter es como un @RestController de Spring.
# prefix="/tareas" → todas las rutas de este archivo arrancan con /tareas
# tags=["tareas"]  → agrupa los endpoints en el Swagger bajo "tareas"
# ------------------------------------------------------------
router = APIRouter(prefix="/tareas", tags=["tareas"])


# ------------------------------------------------------------
# Depends(get_db) es la inyección de dependencias de FastAPI.
# Equivale al @Autowired de Spring — FastAPI crea la sesión,
# la pasa al endpoint, y la cierra al terminar automáticamente.
# ------------------------------------------------------------

@router.get("/", response_model=list[TareaRespuesta])
def listar_tareas(db: Session = Depends(get_db)):
    """GET /tareas — retorna todas las tareas."""
    return tarea_service.obtener_todas(db)


@router.post("/", response_model=TareaRespuesta, status_code=201)
def crear_tarea(datos: TareaCrear, db: Session = Depends(get_db)):
    """POST /tareas — crea una nueva tarea."""
    return tarea_service.crear(datos, db)


@router.patch("/{id}", response_model=TareaRespuesta)
def actualizar_tarea(id: int, datos: TareaActualizar, db: Session = Depends(get_db)):
    """PATCH /tareas/{id} — actualiza campos de una tarea."""
    return tarea_service.actualizar(id, datos, db)


@router.delete("/{id}", status_code=204)
def eliminar_tarea(id: int, db: Session = Depends(get_db)):
    """DELETE /tareas/{id} — elimina una tarea."""
    tarea_service.eliminar(id, db)