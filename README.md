# TaskManager-DevOps

Sistema web para la gestión de tareas de TechSolutions (Flask + SQLite).

## Funcionalidades
RF01 registrar, RF02 consultar, RF03 editar, RF04 eliminar, RF05 cambiar estado (Pendiente, En proceso, Terminada) y RF06 asignar prioridad (Alta, Media, Baja).

## Ejecutar localmente
```bash
pip install -r requirements.txt
python app.py        # http://127.0.0.1:5000
pytest               # pruebas
```

## API
| Método | Ruta | Descripción |
|---|---|---|
| GET | /api/tareas | Lista las tareas |
| POST | /api/tareas | Crea una tarea |
| PUT | /api/tareas/<id> | Edita una tarea |
| PATCH | /api/tareas/<id>/estado | Cambia el estado |
| DELETE | /api/tareas/<id> | Elimina una tarea |

## Flujo DevOps
Plan (Projects e Issues) · Code (ramas y Pull Requests) · CI (`.github/workflows/ci.yml`) · Release `v1.0.0` y artefacto (`entrega.yml`) · Deploy en Render con `gunicorn app:app`.

## Equipo
- [Integrante 1] · [Integrante 2] · [Integrante 3]
