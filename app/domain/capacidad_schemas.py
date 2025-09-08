
from pydantic import BaseModel, Field
from typing import Optional, List

class PlanPagoCuota(BaseModel):
    numeroCuota: int = Field(..., description="Número de la cuota", alias="numero_cuota")
    cuota: float = Field(..., description="Valor de la cuota", alias="cuota")
    abonoCapital: float = Field(..., description="Abono a capital", alias="abono_capital")
    interes: float = Field(..., description="Interés de la cuota", alias="interes")
    saldoRestante: float = Field(..., description="Saldo restante después de la cuota", alias="saldo_restante")

    class Config:
        allow_population_by_field_name = True

class CalcularCapacidadRequest(BaseModel):
    solicitudId: str
    salarioBase: float
    tipoPrestamo: Optional[dict] = None
    plazo: int
    monto: float
    documentoIdentidad: str
    deudaTotalMensual: Optional[float] = None
    token: str


class CalcularCapacidadResponse(BaseModel):
    solicitudId: str = Field(..., alias="solicitud_id")
    decision: str
    planPago: Optional[List[PlanPagoCuota]] = Field(None, alias="plan_pago")

    class Config:
        allow_population_by_field_name = True