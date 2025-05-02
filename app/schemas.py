from datetime import date
from typing import Optional
from pydantic import BaseModel

class TrabajadorBase(BaseModel):
    nombre: str
    puesto: str

class TrabajadorCreate(TrabajadorBase):
    pass

class TrabajadorRead(TrabajadorBase):
    id: int

    class Config:
        orm_mode = True

class TurnoDiaBase(BaseModel):
    fecha: date
    manana_id: Optional[int] = None
    sc_manana_id: Optional[int] = None
    tarde_id: Optional[int] = None
    sc_tarde_id: Optional[int] = None
    int_manana_id: Optional[int] = None
    int_tarde_id: Optional[int] = None

class TurnoDiaCreate(TurnoDiaBase):
    pass

class TurnoDiaRead(TurnoDiaBase):
    id: int

    class Config:
        orm_mode = True


class AsignacionRequest(BaseModel):
    fecha: date
    casilla: str
    trabajador_id: int