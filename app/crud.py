from .database import SessionLocal
from .models import Trabajador, TurnoDia
from datetime import date
from calendar import monthrange

# Devuelve todos los trabajadores como lista de dicts
def get_trabajadores():
    db = SessionLocal()
    trabajadores = db.query(Trabajador).all()
    db.close()
    return [{"id": t.id, "nombre": t.nombre, "puesto": t.puesto} for t in trabajadores]


# Devuelve todos los turnos de un mes
def get_turnos_mes(anio: int, mes: int):
    db = SessionLocal()
    start = date(anio, mes, 1)
    end = date(anio, mes, monthrange(anio, mes)[1])
    turnos = db.query(TurnoDia).filter(TurnoDia.fecha >= start, TurnoDia.fecha <= end).all()
    result = []
    for t in turnos:
        result.append({
            "fecha": t.fecha.isoformat(),
            "manana_id": t.manana_id,
            "sc_manana_id": t.sc_manana_id,
            "tarde_id": t.tarde_id,
            "sc_tarde_id": t.sc_tarde_id,
            "int_manana_id": t.int_manana_id,
            "int_tarde_id": t.int_tarde_id,
        })
    db.close()
    return result


def get_turnos_rango(desde: date, hasta: date):
    db = SessionLocal()
    turnos = db.query(TurnoDia).filter(TurnoDia.fecha >= desde, TurnoDia.fecha <= hasta).all()
    result = []
    for t in turnos:
        result.append({
            "fecha": t.fecha.isoformat(),
            "manana_id": t.manana_id,
            "sc_manana_id": t.sc_manana_id,
            "tarde_id": t.tarde_id,
            "sc_tarde_id": t.sc_tarde_id,
            "int_manana_id": t.int_manana_id,
            "int_tarde_id": t.int_tarde_id,
        })
    db.close()
    return result


# Asigna un trabajador a una casilla específica en una fecha dada
def asignar_trabajador_a_casilla(fecha: date, casilla: str, trabajador_id: int):
    db = SessionLocal()
    try:
        turno = db.query(TurnoDia).filter(TurnoDia.fecha == fecha).first()
        if not turno:
            turno = TurnoDia(fecha=fecha)
            db.add(turno)
        
        if not hasattr(turno, casilla):
            raise ValueError(f"Casilla '{casilla}' no válida")
        
        try:
            trabajador_id_int = int(trabajador_id)
        except (ValueError, TypeError):
            trabajador_id_int = None

        if trabajador_id_int == 0:
            setattr(turno, casilla, None)
        else:
            setattr(turno, casilla, trabajador_id_int)

        db.commit()
        return {"success": True, "message": "Turno asignado correctamente"}
    finally:
        db.close()