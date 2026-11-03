from ipaddress import ip_address
from pydantic import BaseModel, ConfigDict, Field, field_validator

class EquipoDatos(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    tipo: str = Field(min_length=2, max_length=40)
    ip: str
    ubicacion: str = Field(min_length=2, max_length=100)
    estado: str = Field(pattern="^(activo|mantenimiento|inactivo)$")

    @field_validator("ip")
    @classmethod
    def validar_ip(cls, value: str) -> str:
        return str(ip_address(value))

class EquipoSalida(EquipoDatos):
    id: int
    model_config = ConfigDict(from_attributes=True)
