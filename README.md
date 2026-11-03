# Inventario de Equipos de Red — API REST

## Descripción
Proyecto académico original para administrar equipos de un laboratorio de redes mediante FastAPI y SQLite. Permite registrar, consultar, actualizar y eliminar routers, switches, computadoras y puntos de acceso.

## Objetivo
Implementar una API REST con persistencia y validación de datos, documentar sus endpoints y comprobar sus respuestas mediante pruebas automatizadas.

## Tecnologías
Python, FastAPI, SQLAlchemy, SQLite, Pytest y Swagger UI.

## Instalación
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abrir http://127.0.0.1:8000/docs

## Endpoints
| Método | Ruta | Función |
|---|---|---|
| GET | /health | Estado del servicio |
| POST | /equipos | Registrar equipo |
| GET | /equipos | Listar equipos (filtro opcional `estado`) |
| GET | /equipos/{equipo_id} | Consultar uno |
| PUT | /equipos/{equipo_id} | Actualizar |
| DELETE | /equipos/{equipo_id} | Eliminar |

## Ejemplo para POST /equipos
```json
{
  "nombre": "Switch Cisco 2960",
  "tipo": "switch",
  "ip": "192.168.28.10",
  "ubicacion": "Laboratorio de redes - Rack A",
  "estado": "activo"
}
```
Estados admitidos: `activo`, `mantenimiento`, `inactivo`.

## Pruebas
```bash
pytest -v
```

## Evidencias
Consultar `evidencias/README.md` para las nueve capturas requeridas. Las capturas se añaden después de ejecutar el proyecto.

## Estructura
- `app/main.py`: endpoints y reglas HTTP.
- `app/db.py`: conexión SQLite.
- `app/models.py`: tabla equipos.
- `app/schemas.py`: validación de datos.
- `tests/test_api.py`: pruebas de operaciones y errores.
- `evidencias/`: capturas de la práctica.

## Resultados y conclusión
Completar esta sección con los resultados observados en la ejecución real, dificultades encontradas y aprendizajes personales.

## Autoría
Nombre: [Escribe tu nombre]
Asignatura: [Escribe tu asignatura]
Grupo: [Escribe tu grupo]
Fecha: [Fecha de realización]
