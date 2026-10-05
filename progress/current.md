# Sesión activa: resumen para continuar en un chat nuevo

Última actualización: 2026-10-04

## Contexto
- Aprendiz: comunicadora y periodista, vibecoder, TDAH, aprende con contrastes, analogías y diagramas. Quiere ir de vibecoder a AI Engineer y luego Chief AI Officer.
- Origen: documento de Perplexity revisado (`docs/referencia/`). Tenía 4 mallas distintas, errores factuales y se cortó a la mitad.
- Repo: `Desktop/proyectos-aura/aura-ai-academy`, privado en https://github.com/CristinaChaconSanta/aura-ai-academy
- Ramas: `feat/fase-0-fabrica-contenido` (por defecto en GitHub) e `investigacion` (Grok Bot). No existe `main` todavía.

## Qué está construido (fase 0)
- **Malla única** `curriculum/malla.md`: 7 niveles (N1 máquina → N7 Chief AI Officer), ~200 lecciones y 33 talleres.
- **Formato de lección** `docs/plantilla-leccion.md`: 11 secciones, incluida "Las palabras nuevas" (qué es, por qué se llama así, ejemplo). Regla: cero conocimiento previo. 15–25 min, máx. 2.200 palabras.
- **Validador** `scripts/validate_lessons.py`: formato + estilo (frases típicas de IA en `docs/frases-prohibidas.txt`, párrafos, frases largas, rayas, exclamaciones, emojis) + cada término del glosario explicado.
- **Lección de referencia** `lecciones/N1/N1-M1-L01-las-partes-de-una-url.md`. La antigua "Qué pasa cuando escribes una URL" (verificada con MDN y RFC 3986; a la aprendiz le gustó) se partió en N1-M1-L01, L02 y L03 por la regla de máximo 5 términos; están en `borrador` hasta la verificación T23.
- **Cursor**: orquestador (`.cursor/rules/orquestador.mdc`), subagentes `investigador`, `redactor`, `verificador` (modelo `claude-opus-5`), `tallerista`; skills `/nueva-leccion`, `/docente`, `/repaso`, `/nuevo-taller`, `/taller`.
- **Grok Bot** (`docs/grok-bot.md`): bot "Investigador Aura" sube investigaciones a la rama `investigacion`; bot "Docente Aura" responde dudas en vivo (texto o voz) y anota huecos de las lecciones. Grok Bot tiene uso propio, aparte del cupo de Cursor.
- **Talleres** (`talleres/`): primero listo, `N1-M1-T` "Desarma una URL" (10 pruebas, se ve en el navegador con `index.html`).
- **Pruebas de calidad**: `docs/prueba-calibracion.md` (rúbrica para calificar 3 lecciones de Cursor).
- **Hoja de ruta** `docs/hoja-de-ruta.md`: fase 1 calibración → fase 2 backend → fase 3 frontend (con referencias en `docs/referencias-frontend/`) → fase 4 docente en la app.
- Estado: `./init.sh` en verde, 75 tests pasan. Tareas y evidencia en `odd/tasks/fase-0-fabrica-contenido.md`.

## Ronda 5 (2026-10-04)
- Plantilla nueva basada en evidencia: 13 secciones con ⏱, predicción, "¿Cuál falla?", máx. 5 palabras nuevas, 15–32 min, "Cómo se conecta" (obligatoria desde N2) y mapa global `curriculum/mapa.md`. "Aprobada" exige recordar 2 de 3 en `/repaso`.
- La lección de la URL se partió en N1-M1-L01/L02/L03 (verificadas 🔎); N1-M1 renumerado (L04–L09).

## Decisiones pendientes (de la aprendiz)
1. **Cuándo construir la app.** Opciones: A) backend ya, en paralelo con calibrar 2–3 lecciones (recomendada); B) app primero sin calibrar; C) calibrar primero.
2. **Revisión automática** (gentle-ai, riesgo alto por el validador que ejecuta procesos): pendiente de su permiso explícito.
3. **Crear rama `main`.**

## Pendientes técnicos
- Espejo en Engram del documento de tareas: pendiente (la sesión quedó ligada a otra carpeta).
- No se probó dentro de Cursor que el ID de modelo `claude-opus-5` sea válido; si falla, usar `model: inherit` (ver `docs/como-usar.md`).
- No se configuró aún Grok Bot (lo hace la aprendiz con los prompts de `docs/grok-bot.md`).

## Cómo retomar en un chat nuevo
Pega esto:

```
Retomo el proyecto aura-ai-academy. Lee progress/current.md, AGENTS.md y odd/tasks/fase-0-fabrica-contenido.md. Dime en 3 líneas dónde estamos y la decisión pendiente número 1.
```
