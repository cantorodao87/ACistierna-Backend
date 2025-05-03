from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, init_db
from . import models, crud
from datetime import date
from app.schemas import AsignacionRequest

app = FastAPI()

# Habilitar CORS (para conectar con React en localhost)
app.add_middleware(
    CORSMiddleware,
        allow_origins=[
        "https://a-cistierna-frontend.vercel.app",  # Dominio de producción
        "http://localhost:5173",                    # Dominio de desarrollo local
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas
Base.metadata.create_all(bind=engine)
init_db()

@app.get("/")
def read_root():
    return {"message": "La API de turnos está activa."}

@app.get("/trabajadores")
def listar_trabajadores():
    return crud.get_trabajadores()

@app.get("/turnos/{anio}/{mes}")
def listar_turnos(anio: int, mes: int):
    return crud.get_turnos_mes(anio, mes)

@app.get("/turnos_rango")
def turnos_rango(desde: date = Query(...), hasta: date = Query(...)):
    return crud.get_turnos_rango(desde, hasta)

@app.post("/asignar/")
def asignar_trabajador(request: AsignacionRequest):
    try:
        return crud.asignar_trabajador_a_casilla(
            fecha=request.fecha, casilla=request.casilla, trabajador_id=request.trabajador_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))