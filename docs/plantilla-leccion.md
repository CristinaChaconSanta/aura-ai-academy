# Plantilla de lección

Toda lección sigue esta forma exacta. `scripts/validate_lessons.py` la comprueba; si no pasa, la lección no existe.

**Ruta:** `lecciones/N<k>/<ID>-<slug>.md`
Ejemplo: `lecciones/N1/N1-M1-L01-que-pasa-cuando-escribes-una-url.md`

**Límites:** 1 concepto, 10–15 minutos, máximo 1.400 palabras (sin contar código ni diagramas).

---

## Esqueleto (copiar tal cual)

````markdown
---
id: N1-M1-L01
titulo: Qué pasa cuando escribes una URL
nivel: 1
duracion_min: 12
estado: borrador
prerequisitos: []
fuentes:
  - https://developer.mozilla.org/...
  - https://...
glosario: [URL, DNS, servidor]
---

## 1. El gancho
Una situación o pregunta concreta que la aprendiz ya vivió. 2–4 frases. Nada de definiciones aquí.

## 2. La idea en una frase
Una sola frase, en negrita. Si no cabe en una frase, la lección tiene dos conceptos: divídela.

## 3. La analogía
Una analogía del mundo del periodismo, la comunicación o la vida cotidiana.
Cierra con una línea "**Dónde se rompe la analogía:** ..." (toda analogía falla en algún punto).

## 4. Contraste
Tabla de 2 o 3 columnas que compara el concepto con su opuesto o con algo que se confunde con él.

| | Opción A | Opción B |
| :-- | :-- | :-- |
| ... | ... | ... |

## 5. Diagrama
Un diagrama Mermaid. Máximo 10 nodos. Etiquetas en español, cortas.

```mermaid
flowchart LR
  A[Tú] --> B[Navegador]
```

Debajo, una frase que diga qué mirar primero en el diagrama.

## 6. Bueno vs. malo
Un ejemplo concreto de cómo se hace bien y cómo se hace mal (código, configuración o decisión).
Si hay código: máximo 15 líneas por bloque, con comentarios en español.

## 7. Ponte a prueba
1. Pregunta de recuerdo (¿qué es...?)
<details><summary>Respuesta</summary>...</details>

2. Pregunta de aplicación (¿qué harías si...?)
<details><summary>Respuesta</summary>...</details>

3. Pregunta de detección (¿qué está mal en...?)
<details><summary>Respuesta</summary>...</details>

## 8. Mini ejercicio
Una acción de 5–10 minutos con resultado visible: abrir algo, ejecutar un comando, dibujar, pedirle algo a la IA y revisar la respuesta.
Termina con "**Sabrás que lo lograste cuando:** ...".

## 9. Cómo te ayuda a revisar a la IA
2–4 viñetas: qué error típico comete un agente de código con este concepto y cómo detectarlo.

## 10. Fuentes
- [Título de la fuente](https://...) — qué se tomó de ella
- [Título](https://...) — ...
````

---

## Estados

| Estado | Quién lo pone | Significa |
| :-- | :-- | :-- |
| `borrador` | redactor | Escrita, sin verificar. |
| `verificada` | verificador | Cada afirmación revisada contra fuentes; pasa el validador. |
| `aprobada` | solo la aprendiz | La estudió y el formato le funcionó. |
