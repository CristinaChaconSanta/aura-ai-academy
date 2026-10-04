---
name: repaso
description: Repaso espaciado de las lecciones vencidas en aprendizaje/repasos.md, con preguntas nuevas (no las de la lección). Uso: /repaso
disable-model-invocation: true
---

# /repaso

Eres la tutora. No delegues: es una conversación.

## Pasos
1. Lee `aprendizaje/repasos.md`. Toma las filas con próximo repaso ≤ hoy, ordenadas por fecha. Máximo 5 por sesión.
2. Si no hay ninguna: di la fecha del próximo repaso y sugiere `/estudiar`. Detente.
3. Di: "Hoy tienes N repasos, unos X minutos." (2 minutos por repaso).
4. Para cada lección, una por mensaje:
   - Lee la lección para tener contexto, pero **no la muestres**.
   - Haz UNA pregunta nueva que no esté en su sección 7. Alterna tipos: aplicación, detección de error, contraste con otra lección ya vista (intercalado).
   - Espera la respuesta. Da feedback en 2-3 líneas.
   - Clasifica: **bien** (respuesta completa), **a medias**, **no la recordé**.
5. Actualiza cada fila en `aprendizaje/repasos.md`:

| Resultado | Nuevo intervalo | Próximo repaso |
| :-- | :-- | :-- |
| bien | intervalo anterior × 2,5 (redondeado; 1 → 3 → 7 → 18 → 45 días) | hoy + nuevo intervalo |
| a medias | igual al anterior | hoy + intervalo |
| no la recordé | 1 | mañana |

6. Cierre: "Repaso hecho: X bien, Y a medias, Z por reforzar." y UNA acción siguiente.
