# Taller N1-M1: Desarma una URL

**Practicas:** la lección [Qué pasa cuando escribes una URL](../../lecciones/N1/N1-M1-L01-que-pasa-cuando-escribes-una-url.md).
**Tiempo:** unos 25 minutos.
**Editas:** solo `solucion.js`.

## Qué vas a hacer
Vas a escribir código que toma una URL y la separa en sus cinco partes: esquema, dominio, ruta, parámetros y ancla.
Las pruebas ya están escritas. Tu meta es ponerlas en verde.

## Dos ideas antes de empezar
- **Función:** una receta con nombre. Le das algo (la URL) y hace un trabajo con eso.
- **`return`:** la palabra con la que la función entrega su resultado. Lo que va después de `return` es lo que sale.

`new URL(texto)` es una herramienta que JavaScript ya trae: recibe una URL y la desarma por ti.
Tú solo tienes que pedirle cada parte. Su documentación: [URL en MDN](https://developer.mozilla.org/en-US/docs/Web/API/URL).

## Cómo correr las pruebas
Elige una de las dos formas.

**A. En Chrome (la más visual)**
1. Haz doble clic en `index.html` (o ábrelo con Chrome).
2. Cada vez que cambies `solucion.js`: guarda y recarga la página.

**B. En la terminal**
Desde la carpeta principal del repositorio:

```bash
node talleres/N1-M1-T-desarma-una-url/pruebas.js
```

✅ es una prueba que pasa. ❌ es una que falta, con una pista de qué esperaba.

## Metas
- **Nivel 1:** las 8 primeras pruebas en verde (función `partesDeUrl`).
- **Nivel 2 (reto):** las pruebas que empiezan con "Reto:" en verde (función `parametro`).

Al empezar, todo sale en rojo. Es normal: todavía no has escrito nada.
Ve de a una prueba. Cambia un `null`, guarda, mira qué se puso verde.

## Si te atascas
En Cursor escribe `/taller N1-M1-T`. El docente te da pistas, no la respuesta.
