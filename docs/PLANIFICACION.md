# Planificación: historias de usuario e Issues

## Historias de usuario
**HU1 Registrar tareas.** Como usuario del sistema, quiero registrar nuevas tareas para organizar mis actividades.
Criterios: ingresar nombre; agregar descripción; seleccionar prioridad; guardar la tarea; mostrar mensaje de confirmación.

**HU2 Consultar tareas.** Como usuario, quiero ver todas las tareas registradas para conocer mi trabajo pendiente.
Criterios: mostrar listado con nombre, descripción, estado y prioridad; mostrar mensaje si no hay tareas.

**HU3 Editar tareas.** Como usuario, quiero modificar una tarea para corregir o actualizar su información.
Criterios: cargar los datos actuales en el formulario; guardar los cambios; reflejarlos en el listado; validar que el nombre no quede vacío.

**HU4 Eliminar tareas.** Como usuario, quiero eliminar una tarea para quitar actividades que ya no se necesitan.
Criterios: pedir confirmación; la tarea desaparece del listado; mostrar mensaje de confirmación.

**HU5 Cambiar estado.** Como usuario, quiero cambiar el estado de una tarea para conocer su progreso.
Criterios: seleccionar pendiente, en proceso o terminada; el cambio se refleja en el listado.

**HU6 Asignar prioridad.** Como usuario, quiero clasificar tareas como alta, media o baja para atender primero lo urgente.
Criterios: seleccionar la prioridad al crear o editar; se guarda; se distingue visualmente en el listado.

## Issues (campos: Responsable / Estado / Prioridad / Estimación h / Fase DevOps / Fecha límite)
| # | Issue | Fase DevOps | Prioridad | Horas |
|---|---|---|---|---|
| 1 | Crear la estructura inicial del proyecto | Plan | Alta | 2 |
| 2 | Diseñar la interfaz del sistema | Code | Media | 4 |
| 3 | Implementar el registro de tareas (RF01) | Code | Alta | 3 |
| 4 | Implementar la consulta de tareas (RF02) | Code | Alta | 2 |
| 5 | Implementar la edición de tareas (RF03) | Code | Alta | 3 |
| 6 | Implementar la eliminación de tareas (RF04) | Code | Media | 2 |
| 7 | Implementar cambio de estado y prioridad (RF05, RF06) | Code | Alta | 3 |
| 8 | Implementar las pruebas unitarias | Test | Alta | 4 |
| 9 | Configurar GitHub Actions (ci.yml) | Build | Alta | 2 |
| 10 | Ejecutar la matriz de pruebas funcionales (CP01 a CP07) | Test | Media | 3 |
| 11 | Crear el Release v1.0.0 y el workflow de entrega | Release | Media | 2 |
| 12 | Desplegar en Render | Deploy | Alta | 3 |
| 13 | Monitoreo e incidencias | Monitor | Media | 2 |
| 14 | Documento de resultados y conclusiones | Operate | Media | 3 |
