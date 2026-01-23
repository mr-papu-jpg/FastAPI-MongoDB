from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TransferenciaEsquema(BaseModel):
    emisor: Optional[str] = None
    receptor: str
    monto: float = Field(..., gt=0) # gt=0 significa "Greater Than 0"
    fecha: datetime = Field(default_factory=datetime.utcnow)
    comentario: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "emisor": "Angstart",
                "receptor": "Usuario_B",
                "monto": 500.0,
                "comentario": "Pago de servicios"
            }
        }

