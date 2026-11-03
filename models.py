from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class Equipo(Base):
    __tablename__ = "equipos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80))
    tipo: Mapped[str] = mapped_column(String(40))
    ip: Mapped[str] = mapped_column(String(45), unique=True)
    ubicacion: Mapped[str] = mapped_column(String(100))
    estado: Mapped[str] = mapped_column(String(30))
