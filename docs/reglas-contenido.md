# Reglas de contenido y verificación

Estas reglas existen porque el documento original (generado con Perplexity) tenía errores
factuales y se cortó a la mitad. Ver `docs/referencia/revision-malla.md`, sección A.

## 1. Fuentes

**Jerarquía (usar la más alta disponible):**

| Prioridad | Tipo | Ejemplos |
| :-- | :-- | :-- |
| 1 | Documentación oficial o especificación | MDN, docs de Anthropic/OpenAI/AWS/Stripe, RFC, OWASP, texto de la ley |
| 2 | Paper original | arXiv (ReAct, Reflexion, Transformer) |
| 3 | Autor reconocido con trayectoria verificable | Karpathy, Simon Willison, Chip Huyen, Hamel Husain |
| 4 | Medio técnico serio | Ars Technica, The Pragmatic Engineer |
| ✗ | No usar como fuente única | Hilos de X, blogs de SEO, contenido generado por IA, Medium sin autor identificable |

- Mínimo 2 fuentes por lección; al menos 1 de prioridad 1 o 2.
- Toda cifra, fecha, nombre de producto o cita lleva fuente.
- Si una afirmación no se puede verificar: se elimina o se marca "(no verificado)".
- Temas que cambian rápido (precios, modelos, leyes, versiones): se anota la fecha de consulta.
- Contexto Colombia (leyes, DIAN, pasarelas): solo fuentes oficiales colombianas o del proveedor.

## 2. Errores ya conocidos (no repetir)

- InstructDiffusion **no** es un modelo de acciones (es edición de imágenes).
- La arquitectura de GPT-4 **no** está confirmada por OpenAI.
- CLIP es un modelo de embeddings, **no** un VLM conversacional.
- "Cross-prompt injection" no es un término estándar; usar "prompt injection indirecta".
- Evaluator-Optimizer y Orchestrator-Workers vienen de "Building effective agents" (Anthropic, dic. 2024); ReAct y Reflexion son papers.

## 3. Diseño para TDAH

- **Cero conocimiento previo.** Si una palabra técnica no se explicó en esta lección o en un prerequisito, se explica en la sección 3. Ante la duda, se explica.
- **Explica el origen de los nombres.** La aprendiz es periodista: entender de dónde viene una palabra la fija en la memoria. El origen también lleva fuente.

- Un concepto por lección, pero explicado completo: más vale una lección de 20 minutos clara que una de 10 que asume cosas. Si aparece un segundo concepto, se menciona en una línea y se enlaza a su lección.
- Frases cortas. Párrafos de máximo 4 líneas.
- Negrita solo para la idea clave de cada sección.
- Nada de "como vimos antes" sin enlace: la aprendiz no tiene que recordar.
- Cada lección termina con una acción concreta (sección 9).
- Sin relleno motivacional ("¡Excelente!", "Es muy fácil").

## 4. Lenguaje

- Español neutro. Tuteo.
- Término técnico en inglés: la primera vez, en negrita con explicación entre paréntesis. Ej.: **commit** (versión guardada con descripción).
- Cada término técnico nuevo va al campo `glosario` del frontmatter.
- Analogías preferidas: redacción de un periódico, edición, entrevistas, construcción, restaurante, oficina.

## 5. Diagramas

- Mermaid siempre (flowchart, sequenceDiagram, classDiagram, mindmap, erDiagram).
- Máximo 10 nodos.
- Nada de imágenes generadas por IA para explicar conceptos: escriben mal el texto y dibujan flechas sin sentido.
- El diagrama debe poder entenderse sin leer la lección.

## 6. Verificación (lo que hace el verificador)

Para cada lección, el verificador entrega un reporte con:

1. **Afirmaciones revisadas:** tabla `afirmación | fuente | veredicto (✅ correcta / ⚠️ imprecisa / ❌ falsa / ❓ sin fuente)`.
2. **Formato:** salida de `.venv/bin/python scripts/validate_lessons.py <ruta>`.
3. **Diseño:** ¿un solo concepto?, ¿toda palabra técnica tiene entrada en la sección 3?, ¿la analogía dice dónde se rompe?, ¿el diagrama tiene ≤ 10 nodos?
4. **Veredicto final:** `aprobar` (pasa a `verificada`) o `corregir` (con lista de cambios).

Máximo 2 rondas de corrección. Si a la tercera sigue fallando: se detiene y se pregunta a la aprendiz.
