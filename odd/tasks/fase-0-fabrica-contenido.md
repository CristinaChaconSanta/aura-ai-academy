# Fase 0 — Fábrica de contenido y tutor en Cursor

## Objetivo
Montar en Cursor un sistema orquestador + subagentes que produce lecciones verificadas
de la malla y actúa como tutor, sin app todavía. Validar el formato de lección en 2–3 semanas de uso.

## Problema
La malla actual (Perplexity) tiene 4 estructuras distintas, errores factuales y está cortada.
Un agente que genere contenido sin plantilla ni verificación repetiría esos fallos.

## Alcance autorizado
- Arnés del proyecto (skill `nuevo-arnes`).
- Malla canónica única con IDs de lección.
- Plantilla de lección, reglas de contenido y perfil de aprendiz.
- Subagentes de Cursor (`.cursor/agents/`), regla de orquestación (`.cursor/rules/`) y skills invocables (`.cursor/skills/`).
- Validador de lecciones en Python + tests.
- Archivos de progreso de aprendizaje.

Fuera de alcance: app web, base de datos, despliegue (fases 1–4).

## Restricciones
- Contenido en español neutro; identificadores de código en inglés.
- Cada afirmación factual de una lección necesita fuente.
- Sin push, sin PR (decisión de la usuaria).

## Modo TDD
- Modo: off. Fuente: sin configuración de proyecto ni elección explícita. Runner: `.venv/bin/python -m pytest -q -x`.
- Se ejecutan checks funcionales (`./init.sh`) en cada tarea.

## Estrategia de entrega
`ask-on-risk`. Pronóstico: ~1.000 líneas, mayormente prompts y documentación en Markdown; el código es solo el validador.

## Tareas

- [x] T1 — Arnés del proyecto (`init.sh`, hooks, `CLAUDE.md`, `AGENTS.md`, `CHECKPOINTS.md`). Ruta: inline (plantilla mecánica).
- [x] T2 — Malla canónica `curriculum/malla.md` con IDs de lección. Ruta: inline (necesita el contexto de la revisión hecha en esta sesión).
- [x] T3 — Especificaciones de contenido: `docs/plantilla-leccion.md`, `docs/reglas-contenido.md`, `docs/perfil-aprendiz.md`. Ruta: inline (mismo contexto).
- [x] T4 — Subagentes, regla orquestadora y skills de Cursor. Ruta: inline (es el entregable pedido: "crea los prompts para Cursor").
- [x] T5 — Validador `scripts/validate_lessons.py` + tests. Ruta: delegada (writer trigger: 2 archivos no triviales de código, especificación cerrada).
- [x] T6 — Archivos de aprendizaje (`aprendizaje/`), glosario y guía de uso `docs/como-usar.md`; actualizar `AGENTS.md`. Ruta: inline.

## Criterios de aceptación
- `./init.sh` sale con 0 y el validador corre más de 0 tests.
- Una lección de ejemplo pasa el validador.
- La usuaria puede escribir `/nueva-leccion N1-M1-L01` en Cursor y el orquestador sigue el pipeline investigador → redactor → verificador.

## Cambios aceptados
- Se eliminó el subagente `diagramador`: el redactor hace el diagrama y el verificador lo revisa. Motivo: ahorro de tokens pedido por la usuaria.
- La lección de ejemplo no se escribe aquí: la primera lección real la produce el pipeline en Cursor (es la prueba de la fase 0). El esqueleto de `docs/plantilla-leccion.md` sí se validó contra el validador.

## Progreso y evidencia
- T1: commit `84f99df` en `chore/arnes-inicial`; `./init.sh` EXIT=0; 13 tests del arnés en verde.
- T5: delegada; 35 tests nuevos (34 pasan, 1 omitido sin lecciones). Suite completa: 47 passed, 1 skipped.
- Esqueleto de la plantilla validado: `validate_lessons.py` → OK, EXIT=0.
- T2–T6: commit de la rama `feat/fase-0-fabrica-contenido` (ver `git log`).
- Pendiente: prueba real en Cursor (`/nueva-leccion N1-M1-L01`), solo la puede hacer la usuaria.

## Siguiente paso
La usuaria abre el proyecto en Cursor y sigue `docs/como-usar.md`.
