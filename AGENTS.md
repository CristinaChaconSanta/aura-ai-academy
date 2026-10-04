# AGENTS.md — Mapa del repositorio de Aura AI Academy

Este archivo es un mapa, no un reglamento. Dice dónde está cada cosa y cuándo
leerla. Las reglas del proyecto viven en `CLAUDE.md` y `docs/`.

## 1. Antes de empezar

1. Ejecuta `./init.sh`. Si sale con código distinto de 0, para y arréglalo.
2. Lee el documento activo en `odd/tasks/` (estado real de la tarea).
3. Trabaja una tarea a la vez; no abras la siguiente sin cerrar la actual.

## 2. Mapa del repositorio

| Archivo o carpeta | Qué contiene | Cuándo leerlo |
|---|---|---|
| `CLAUDE.md` | Identidad, propósito y arranque (carga en cada sesión) | Siempre |
| `odd/tasks/` | Documentos de tarea (estado, checklist, evidencias) | Al empezar y al cerrar cada tarea |
| `progress/` | `current.md` (sesión activa) e `history.md` (bitácora) | Al delegar o cerrar sesión |
| `init.sh` | Puerta de inicio y cierre (entorno, archivos, pruebas, seguridad) | Al empezar y antes de dar algo por hecho |
| `.claude/` | `harness.env`, `settings.json` y hooks | Al ajustar el arnés |
| `.cursor/` | Regla del arnés y hook de cierre para Cursor | Al ajustar el arnés en Cursor |
| `CHECKPOINTS.md` | Lista verificable de cierre | Antes de cerrar la sesión |
| `docs/referencia/` | Documento original de Perplexity y su revisión | Solo como fuente de temas; contiene errores señalados en la revisión |
| `curriculum/malla.md` | Malla canónica: niveles, módulos, IDs y estado de cada lección | Antes de crear o estudiar una lección |
| `docs/plantilla-leccion.md` | Formato obligatorio de una lección | Al redactar o verificar |
| `docs/reglas-contenido.md` | Fuentes, errores conocidos, diseño TDAH, verificación | Al investigar, redactar o verificar |
| `docs/perfil-aprendiz.md` | Quién aprende y cómo | Al redactar o tutorar |
| `docs/como-usar.md` | Guía de uso en Cursor y prompts útiles | La aprendiz, al empezar |
| `lecciones/N<k>/` | Lecciones (una por archivo) | Al estudiar o verificar |
| `aprendizaje/` | Progreso, repasos espaciados, glosario, preguntas abiertas | En `/docente` y `/repaso` |
| `.cursor/agents/` | Subagentes: `investigador`, `redactor`, `verificador`, `tallerista` | Al ajustar el pipeline |
| `.cursor/rules/orquestador.mdc` | Rol del agente principal | Siempre (se aplica solo) |
| `.cursor/skills/` | Flujos `/nueva-leccion`, `/docente`, `/repaso`, `/nuevo-taller`, `/taller` | Al invocarlos |
| `talleres/` | Talleres de práctica por módulo; formato en `talleres/README.md` | Al crear o resolver un taller |
| `tests/test_talleres.py` | Corre cada taller contra su solución de referencia | Después de crear un taller |
| `scripts/validate_lessons.py` | Valida formato y estilo de las lecciones | Después de escribir una lección |
| `docs/frases-prohibidas.txt` | Frases típicas de IA que el validador rechaza | Al redactar; agrega frases nuevas aquí |
| `docs/grok-bot.md` | Grok Bot como investigador vía la rama `investigacion` | Al configurar o depurar la investigación |
| `docs/prueba-calibracion.md` | Rúbrica para saber si Cursor escribe bien | Antes de producir muchas lecciones |
| `docs/hoja-de-ruta.md` | Fases 0 a 4 y cuándo nacen los agentes de backend y frontend | Al cambiar de fase |
| `lecciones/N1/N1-M1-L01-*.md` | Lección de referencia (tono y nivel) | El redactor, siempre |

## 3. Reglas duras

- Ninguna tarea está terminada sin `./init.sh` en verde.
- Cero secretos en commits: `.env` está en `.gitignore`.
- Nunca inventar datos.
- Toda lección pasa `scripts/validate_lessons.py` y la revisión del `verificador` antes de quedar `verificada`.
- Solo la aprendiz marca una lección como `aprobada`.

## 4. Subagentes

- El orquestador delega; los subagentes ejecutan una unidad acotada.
- Cada subagente escribe su resultado en `progress/<tipo>_<tema>.md` y
  responde solo `done -> progress/<archivo>` o `blocked -> <motivo>`.
- El estado de las tareas vive en `odd/tasks/`, no en `progress/`.

## 5. Cierre de sesión

1. `./init.sh` en verde.
2. Actualizar los checkboxes de `odd/tasks/` con evidencia (comando y resultado, hash de commit).
3. Añadir una línea a `progress/history.md`.
4. Commit por unidad de trabajo con Conventional Commits.
