from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db import Base, get_db
from app.main import app

engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def db_prueba():
    with Session() as db:
        yield db

app.dependency_overrides[get_db] = db_prueba
client = TestClient(app)

def datos(ip="192.168.28.10"):
    return {"nombre":"Switch laboratorio", "tipo":"switch", "ip":ip, "ubicacion":"Rack A", "estado":"activo"}

def test_crud_y_filtro():
    creado = client.post("/equipos", json=datos())
    assert creado.status_code == 201
    identificador = creado.json()["id"]
    assert client.get(f"/equipos/{identificador}").status_code == 200
    assert len(client.get("/equipos?estado=activo").json()) >= 1
    cambio = datos(); cambio["estado"] = "mantenimiento"
    assert client.put(f"/equipos/{identificador}", json=cambio).json()["estado"] == "mantenimiento"
    assert client.delete(f"/equipos/{identificador}").status_code == 200
    assert client.get(f"/equipos/{identificador}").status_code == 404

def test_validaciones():
    assert client.post("/equipos", json=datos("ip-invalida")).status_code == 422
    assert client.post("/equipos", json=datos("192.168.28.11")).status_code == 201
    assert client.post("/equipos", json=datos("192.168.28.11")).status_code == 409
