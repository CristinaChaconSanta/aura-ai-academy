# Hoja de ruta

| Fase | Qué es | Agentes nuevos | Condición para empezar |
| :-- | :-- | :-- | :-- |
| **0. Fábrica y docente** (actual) | Lecciones verificadas en Cursor, docente y repasos | `investigador` (Grok Bot + respaldo en Cursor), `redactor`, `verificador` | — |
| **1. Calibración** | 3 lecciones aprobadas con la rúbrica de `docs/prueba-calibracion.md` | Ninguno | Fase 0 instalada |
| **2. Datos y backend de progreso** | Modelo de datos, base de datos (Supabase), login, progreso y repasos guardados | `backend` | Calibración aprobada |
| **3. Frontend** | App para leer lecciones, ver la malla y el progreso | `frontend` (con tus referencias visuales) | Backend con sus pruebas en verde |
| **4. Docente dentro de la app** | Chat que conoce la lección en la que estás y tu historial | Ninguno (se reutiliza `/docente`) | Frontend publicado |

## Por qué backend antes que frontend

Primero se decide qué datos existen: lección, intento, repaso, término del glosario.
La interfaz se diseña sobre esos datos.
Al revés, la interfaz promete cosas que la base de datos no sabe guardar.

## Por qué frontend y backend todavía no tienen agente

Un agente sin tarea concreta inventa trabajo. Se crean al empezar su fase, con su propio documento en `odd/tasks/`.
Para el frontend, deja tus referencias visuales en `docs/referencias-frontend/` cuando las tengas.
