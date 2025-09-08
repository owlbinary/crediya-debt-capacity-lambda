from pydantic import BaseModel
from typing import Optional, Any, List

class ErrorResponse(BaseModel):
    codigo: str
    mensaje: str
    timestamp: str
    path: str
    detalles: Optional[Any] = None