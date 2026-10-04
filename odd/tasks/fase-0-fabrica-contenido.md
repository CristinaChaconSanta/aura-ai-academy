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

### Ronda 2 (aprobada por la usuaria el 2026-10-03)
Motivo: la usuaria pidió docente visible, investigación con Grok Bot, repo compartido en GitHub y pruebas contra los "textos raros" de Cursor.

- [x] T7 — Renombrar `/estudiar` a `/docente` y actualizar referencias. Ruta: inline (mecánico).
- [x] T8 — Verificador con modelo de otra familia (`claude-opus-5`). Ruta: inline (1 línea).
- [x] T9 — Integración con Grok Bot: `docs/grok-bot.md` (rutina de investigación + protocolo por rama `investigacion`) y paso 1 de `/nueva-leccion` que usa esa investigación si existe. Ruta: inline (prompts).
- [x] T10 — Controles de estilo en el validador: frases prohibidas (`docs/frases-prohibidas.txt`), largo de párrafo y de frase, rayas, exclamaciones, emojis. Ruta: delegada (writer trigger: validador + tests).
- [x] T11 — Lección de referencia `N1-M1-L01` escrita y verificada con fuentes, para que el redactor imite el tono. Ruta: inline (requiere investigación con fuentes).
- [x] T12 — Protocolo de calibración `docs/prueba-calibracion.md` (las "pruebas" para Cursor) y hoja de ruta con fases 2 = backend, 3 = frontend. Ruta: inline.
- [x] T13 — Repo privado en GitHub y push de la rama. Ruta: inline. Autorizado por la usuaria.

### Ronda 3 (feedback de la usuaria tras leer N1-M1-L01, 2026-10-03)
Motivo: "no entendí parámetros, anclas, esquema; no sé de dónde vienen esos nombres; pueden ser más extensas, no asumir que entiendo todo". Pide además un chat en vivo con Grok Bot.

- [x] T14 — Nueva sección obligatoria "Las palabras nuevas" (qué es, por qué se llama así, ejemplo) y límites más amplios (2.200 palabras, hasta 25 min). Validador: cada término del `glosario` debe tener su entrada en esa sección. Ruta: delegada (writer trigger: validador + tests).
- [x] T15 — Plantilla, reglas, redactor, verificador y docente: regla "cero conocimiento previo". Ruta: inline (prompts).
- [x] T16 — Reescribir N1-M1-L01 con el formato nuevo y el origen de cada nombre, con fuentes (RFC 3986, MDN). Ruta: inline (requiere fuentes).
- [x] T17 — Grok Bot "Docente Aura" para preguntas en vivo (texto y voz), en `docs/grok-bot.md`. Ruta: inline (prompt).

### Ronda 4 (talleres, aprobada por la usuaria el 2026-10-03)
Motivo: leer sobre código no enseña a codear; hace falta práctica con resultado visible.

- [x] T18 — Mini biblioteca de pruebas (Node + navegador), primer taller `N1-M1-T` "Desarma una URL" con solución de referencia, y test del arnés que corre cada taller contra su referencia. Ruta: delegada (writer trigger: varios archivos de código).
- [x] T19 — Prompts: subagente `tallerista`, skills `/taller` y `/nuevo-taller`, `talleres/README.md`, filas de taller en la malla, `como-usar.md` y `AGENTS.md`. Ruta: inline (prompts).

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

- Ronda 2: T10 delegada (62 tests en verde). Lección de referencia N1-M1-L01 validada (OK); prueba manual: el validador detecta 2 frases prohibidas, 4 rayas y 2 exclamaciones en una copia alterada.

- Ronda 3: T14 delegada; N1-M1-L01 reescrita (11 secciones, 11 términos con origen del nombre, 8 fuentes: MDN + RFC 3986). Validador OK; 72 tests en verde.

- Ronda 4: T18 delegada; referencia 10/10, archivo inicial 0/10 con mensajes legibles; verificado en navegador ("0 de 10 pruebas pasan"). 33 filas de taller en la malla. 75 tests en verde.

## Siguiente paso
La usuaria abre el proyecto en Cursor y sigue `docs/como-usar.md`.

## Estado del espejo en Engram
Pendiente: la sesión de Engram quedó registrada en otro proyecto (`session_project_mismatch`). Resincronizar en la próxima sesión abierta desde esta carpeta.

## Revisión (RDD)
`gentle-ai review assess` sobre `84f99df..904b612`: riesgo **high** (`process_boundary` en `scripts/validate_lessons.py`), `review_due: true`. Siguiente transición: `review.start`, esperando consentimiento de la usuaria.
