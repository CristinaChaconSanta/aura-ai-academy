# Prueba de calibración: ¿Cursor escribe bien?

Cursor a veces produce textos raros. Esta prueba mide si el pipeline escribe lecciones que te sirven, antes de producir decenas.

## Las tres capas de control

| Capa | Qué atrapa | Quién la hace |
| :-- | :-- | :-- |
| 1. Validador automático | Formato roto, frases típicas de IA, párrafos y frases largas, exceso de rayas, exclamaciones y emojis | `scripts/validate_lessons.py` |
| 2. Verificador | Datos falsos o sin fuente, más de un concepto, analogía débil | Subagente `verificador` (otro modelo) |
| 3. Tú | Si se entiende, si engancha, si suena humano | Esta prueba |

La capa 1 ya bloquea lo mecánico. Las capas 2 y 3 atrapan lo que una máquina de reglas no ve.

## La prueba (una vez, unos 45 minutos repartidos en 3 días)

1. Lee la lección de referencia: `lecciones/N1/N1-M1-L01-que-pasa-cuando-escribes-una-url.md`. Es el estándar. Si no te gusta, dilo primero: todo lo demás la imita.
2. En Cursor, ejecuta `/nueva-leccion N1-M1-L02`, luego `N1-M1-L03` y `N1-M1-L04`.
3. Estudia cada una con `/docente`.
4. Califica cada lección con la rúbrica de abajo en `aprendizaje/calibracion.md`.

## Rúbrica (1 a 3 por criterio)

| Criterio | 1 | 2 | 3 |
| :-- | :-- | :-- | :-- |
| **Suena humano** | Suena a folleto o a chatbot | Algunas frases raras | Suena a una colega que sabe |
| **Se entiende a la primera** | Tuve que releer varias veces | Releí una parte | Lo entendí leyendo una vez |
| **La analogía ayuda** | Me confundió más | Correcta pero fría | Me quedó grabada |
| **El diagrama ayuda** | No lo entendí | Lo entendí con la lección | Lo entendí solo |
| **Duración real** | Más de 25 min | 15 a 25 min | 15 min o menos |

**Aprobado:** promedio ≥ 2,5 en las 3 lecciones y ningún 1 en "Suena humano".

## Si no aprueba

Pídele a Cursor:

```
Lee aprendizaje/calibracion.md. Muéstrame las 3 frases peores de cada lección y propón UNA regla nueva para docs/reglas-contenido.md o una frase nueva para docs/frases-prohibidas.txt. No apliques nada todavía.
```

Repite la prueba con 2 lecciones nuevas después de cada ajuste.

## Bitácora (`aprendizaje/calibracion.md`)

| Fecha | Lección | Humano | Se entiende | Analogía | Diagrama | Duración | Frase más rara |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
