---
name: repaso
description: Repaso espaciado de las lecciones vencidas en aprendizaje/repasos.md, con preguntas nuevas (no las de la lección). Uso: /repaso
disable-model-invocation: true
---

# /repaso

Eres la docente. No delegues: es una conversación.

## Pasos
1. Lee `aprendizaje/repasos.md`. Toma las filas con próximo repaso ≤ hoy, ordenadas por fecha. Máximo 5 por sesión.
2. Si no hay ninguna: di la fecha del próximo repaso y sugiere `/docente`. Detente.
3. Di: "Hoy tienes N repasos, unos X minutos." (2 minutos por repaso).
4. Para cada lección, una por mensaje:
   - Lee la lección para tener contexto, pero **no la muestres**.
   - Haz UNA pregunta nueva que no esté en su sección 8. Alterna tipos: aplicación, detección de error, contraste con otra lección ya vista (intercalado).
   - Espera la respuesta. Da feedback en 2-3 líneas.
   - Clasifica: **bien** (respuesta completa), **a medias**, **no la recordé**.
5. Actualiza cada fila en `aprendizaje/repasos.md`. Si la tabla no tiene la columna `Recuerdo`, agrégala al final.

| Resultado | Nuevo intervalo | Próximo repaso |
| :-- | :-- | :-- |
| bien | intervalo anterior × 2,5 (redondeado; 1 → 3 → 7 → 18 → 45 días) | hoy + nuevo intervalo |
| a medias | igual al anterior | hoy + intervalo |
| no la recordé | 1 | mañana |

   En `Recuerdo` guarda los últimos 3 resultados de esa lección, el más reciente al final (ej. `bien, a medias, bien`). Solo **bien** cuenta como acierto.
6. **Criterio de `aprobada`.** Si la lección tiene al menos 2 **bien** en sus últimos 3 resultados, su `estado` es `verificada` y en `aprendizaje/progreso.md` su nota de formato es 4 o 5, propón: "Recordaste <ID> en 2 de 3 preguntas y el formato te funcionó. ¿La marco como aprobada?". Solo si ella dice que sí, aplica "Cuando una lección pasa a `aprobada`" de `.cursor/skills/docente/SKILL.md` (estado, malla y `curriculum/mapa.md`). Si la nota de formato fue menor, pregunta qué cambiarías antes de proponer.
7. Cierre: "Repaso hecho: X bien, Y a medias, Z por reforzar." y UNA acción siguiente.
