---
name: nueva-leccion
description: Crea una lección verificada de la malla con el pipeline investigador → redactor → verificador. Uso: /nueva-leccion N1-M1-L01
disable-model-invocation: true
---

# /nueva-leccion <ID>

Toma el ID del mensaje de la aprendiz. Si no hay ID, toma la primera lección con ⬜ en `curriculum/malla.md` y dile cuál elegiste.

## Paso 0 — Preparar
1. Ejecuta `./init.sh`. Si falla, detente y muestra el error.
2. Confirma que el ID existe en `curriculum/malla.md`. Si no existe, detente.
3. Si ya existe `lecciones/N<k>/<ID>-*.md`, pregunta si quiere rehacerla. Espera respuesta.
4. Escribe en `progress/current.md`: tarea activa = `<ID>`, plan = los 4 pasos de abajo.

## Paso 1 de 4 — Investigación
1. Busca primero la investigación de Grok Bot (ver `docs/grok-bot.md`):
   ```
   git fetch origin investigacion
   git cat-file -e origin/investigacion:progress/investigacion_<ID>.md && git checkout origin/investigacion -- progress/investigacion_<ID>.md
   ```
   Si el archivo llegó, dile a la aprendiz "Paso 1 de 4: uso la investigación de Grok Bot" y sigue al paso 2.
2. Si no existe (o el `fetch` falla), delega al subagente `investigador` con: "Investiga la lección <ID>."
   Si responde `blocked`, detente e informa.

## Paso 2 de 4 — Redacción
Delega al subagente `redactor` con: "Redacta la lección <ID> a partir de progress/investigacion_<ID>.md."
Si responde con `falta: ...`, vuelve a delegar al `investigador` solo para ese dato y luego otra vez al `redactor`.

## Paso 3 de 4 — Verificación (ronda 1, máximo 3)
Delega al subagente `verificador` con: "Verifica la lección <ID>. Ronda <n>."
- `aprobar` → cambia `estado: borrador` a `estado: verificada` en la lección y sigue al paso 4.
- `corregir` y ronda < 3 → delega al `redactor`: "Corrige la lección <ID> según progress/verificacion_<ID>.md." Luego repite este paso con ronda + 1.
- `corregir` en ronda 3 → detente. Muestra a la aprendiz las correcciones pendientes y pregunta cómo seguir.

## Paso 4 de 4 — Cierre
1. En `curriculum/malla.md`, cambia el estado de la fila `<ID>` a 🔎.
2. Ejecuta `.venv/bin/python scripts/validate_lessons.py` y `./init.sh`. Ambos deben pasar.
3. Agrega los términos del campo `glosario` de la lección a `aprendizaje/glosario.md` (solo los que no estén).
4. Agrega una línea a `progress/history.md`: `- AAAA-MM-DD: lección <ID> verificada (rondas: n)`.
5. Vacía `progress/current.md` (deja la plantilla).
6. Commit: `docs(lecciones): add <ID> <slug>`.

## Mensaje final a la aprendiz
```
Lección <ID> lista y verificada: <título> (<duracion_min> min).
Archivo: lecciones/N<k>/<archivo>.md
Siguiente: escribe /docente <ID>
```
