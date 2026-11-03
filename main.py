from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .db import Base, engine, get_db
from .models import Equipo
from .schemas import EquipoDatos, EquipoSalida

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield

app = FastAPI(title="Inventario de Equipos de Red", version="1.0.0", lifespan=lifespan)

@app.get("/health")
def health():
    return {"estado": "operativo"}

@app.post("/equipos", response_model=EquipoSalida, status_code=201)
def crear_equipo(datos: EquipoDatos, db: Session = Depends(get_db)):
    equipo = Equipo(**datos.model_dump())
    db.add(equipo)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "La dirección IP ya está registrada")
    db.refresh(equipo)
    return equipo

@app.get("/equipos", response_model=list[EquipoSalida])
def listar_equipos(estado: str | None = Query(default=None), db: Session = Depends(get_db)):
    consulta = select(Equipo)
    if estado is not None:
        consulta = consulta.where(Equipo.estado == estado)
    return db.scalars(consulta.order_by(Equipo.id)).all()

@app.get("/equipos/{equipo_id}", response_model=EquipoSalida)
def obtener_equipo(equipo_id: int, db: Session = Depends(get_db)):
    equipo = db.get(Equipo, equipo_id)
    if equipo is None:
        raise HTTPException(404, "Equipo no encontrado")
    return equipo

@app.put("/equipos/{equipo_id}", response_model=EquipoSalida)
def actualizar_equipo(equipo_id: int, datos: EquipoDatos, db: Session = Depends(get_db)):
    equipo = db.get(Equipo, equipo_id)
    if equipo is None:
        raise HTTPException(404, "Equipo no encontrado")
    for campo, valor in datos.model_dump().items():
        setattr(equipo, campo, valor)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, "La dirección IP ya está registrada")
    db.refresh(equipo)
    return equipo

@app.delete("/equipos/{equipo_id}")
def eliminar_equipo(equipo_id: int, db: Session = Depends(get_db)):
    equipo = db.get(Equipo, equipo_id)
    if equipo is None:
        raise HTTPException(404, "Equipo no encontrado")
    db.delete(equipo)
    db.commit()
    return {"mensaje": "Equipo eliminado correctamente"}
