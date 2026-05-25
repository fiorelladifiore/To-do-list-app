from pydantic import BaseModel
from typing import Optional

# ------------------------------------------------------------
# Los schemas son los DTOs — definen qué datos entran y salen
# de la API. Son distintos del modelo ORM (models/tarea.py)
# porque lo que exponés no siempre es igual a lo que guardás.
# Por ejemplo: nunca devolverías una contraseña aunque esté en la tabla.
# ------------------------------------------------------------

class TareaBase(BaseModel):
    """Campos comunes a crear y responder."""
    titulo: str
    descripcion: Optional[str] = None


class TareaCrear(TareaBase):
    """
    Schema de entrada para POST /tareas.
    Hereda titulo y descripcion de TareaBase.
    El pass significa que no agrega nada nuevo — solo renombra
    la clase para dejar clara la intención.
    """
    pass


class TareaActualizar(BaseModel):
    """
    Schema de entrada para PATCH /tareas/{id}.
    Todos los campos son opcionales porque en un PATCH
    solo se envían los campos que se quieren modificar.
    """
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    completada: Optional[bool] = None


class TareaRespuesta(TareaBase):
    """
    Schema de salida — lo que devuelve la API al cliente.
    Incluye los campos que genera el servidor: id, completada, creada_en.

    model_config con from_attributes=True le dice a Pydantic que puede
    leer datos desde un objeto ORM de SQLAlchemy (que no es un dict).
    Sin esto, al intentar serializar un objeto Tarea de SQLAlchemy daría error.
    En versiones anteriores de Pydantic esto se llamaba class Config: orm_mode = True
    """
    id: int
    completada: bool
    creada_en: str

    model_config = {"from_attributes": True}