from datetime import date, datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .models import Base, Trabajador, TurnoDia

SQLALCHEMY_DATABASE_URL = "sqlite:///./asigna_turnos.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)

    # Insertar trabajadores de prueba solo si la tabla está vacía
    db = SessionLocal()
    if db.query(Trabajador).count() == 0:
        trabajadores = [
            Trabajador(nombre="Carlos", puesto="Maquinista"),
            Trabajador(nombre="Luis", puesto="Maquinista"),
            Trabajador(nombre="Diego", puesto="Maquinista"),
            Trabajador(nombre="Minerva", puesto="Maquinista"),
            Trabajador(nombre="Juan Daniel", puesto="Maquinista"),
            Trabajador(nombre="Blanco", puesto="Maquinista"),
            Trabajador(nombre="Carrera", puesto="Maquinista"),
            Trabajador(nombre="Noelia", puesto="Maquinista"),
            Trabajador(nombre="Sergio", puesto="Maquinista"),
            Trabajador(nombre="Chamorro", puesto="Maquinista"),
            Trabajador(nombre="Seco", puesto="Maquinista"),
            Trabajador(nombre="Dario", puesto="Maquinista"),
            Trabajador(nombre="Sonia", puesto="Maquinista"),

            Trabajador(nombre="Ruben", puesto="Interventor"),
            Trabajador(nombre="Carmen", puesto="Interventor"),
            Trabajador(nombre="Perez", puesto="Interventor"),
            Trabajador(nombre="Canton", puesto="Interventor"),
        ]
        db.add_all(trabajadores)
        db.commit()
    db.close()



def obtener_turno_dia(db, fecha: date) -> TurnoDia:
    turno = db.query(TurnoDia).filter(TurnoDia.fecha == fecha).first()
    if not turno:
        turno = TurnoDia(fecha=fecha)
        db.add(turno)
        db.commit()
        db.refresh(turno)
    return turno



def asignar_trabajador_a_casilla(db, fecha: date, casilla: str, trabajador_id: int):
    turno = obtener_turno_dia(db, fecha)
    if not hasattr(turno, casilla):
        raise ValueError(f"Casilla no válida: {casilla}")
    setattr(turno, casilla, trabajador_id)
    db.commit()
    db.refresh(turno)
    return turno



def obtener_turnos_mes(db, year: int, month: int):
    from calendar import monthrange
    first_day = date(year, month, 1)
    last_day = date(year, month, monthrange(year, month)[1])
    turnos = db.query(TurnoDia).filter(TurnoDia.fecha >= first_day, TurnoDia.fecha <= last_day).all()
    return turnos