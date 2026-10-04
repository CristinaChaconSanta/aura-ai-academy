---
name: nuevo-taller
description: Crea el taller de práctica de un módulo con el subagente tallerista y lo verifica. Uso: /nuevo-taller N1-M3-T
disable-model-invocation: true
---

# /nuevo-taller <ID>

Toma el ID del mensaje (formato `N<k>-M<m>-T`). Si no hay ID, toma el primer módulo de `curriculum/malla.md` cuyas lecciones estén todas en 🔎 o ✅ y cuyo taller siga en ⬜. Dile cuál elegiste.

## Paso 1 de 3 — Preparar
1. Ejecuta `./init.sh`. Si falla, detente.
2. Si alguna lección del módulo sigue en ⬜ o 📝, avisa: "El taller usa lecciones que aún no existen" y pregunta si sigue igual. Espera respuesta.

## Paso 2 de 3 — Diseño
Delega al subagente `tallerista` con: "Diseña el taller <ID>."
Si responde `blocked`, detente e informa.

## Paso 3 de 3 — Verificación
1. Delega al subagente `verificador` con: "Verifica el taller <ID> en talleres/<carpeta>/. No es una lección: revisa que el README no use palabras técnicas sin explicar, que las pistas no regalen la respuesta, que el archivo inicial corra sin errores y que las pruebas se entiendan solas." Si pide correcciones, vuelve al `tallerista` (máximo 2 rondas).
2. Ejecuta `.venv/bin/python -m pytest -q tests/test_talleres.py` y `./init.sh`.
3. En `curriculum/malla.md`, cambia el estado de la fila del taller a 🔎.
4. Commit: `feat(talleres): add <ID> <slug>`.

## Mensaje final
```
Taller <ID> listo: <título> (<tipo>, ~<min> min).
Carpeta: talleres/<carpeta>/
Siguiente: escribe /taller <ID>
```
