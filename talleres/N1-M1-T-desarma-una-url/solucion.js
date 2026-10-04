// ============================================================
//  Taller N1-M1: Desarma una URL
//  Este es TU archivo. Solo edita aquí.
//  Cuando termines un cambio: guarda y corre las pruebas.
// ============================================================

// ------------------------------------------------------------
// NIVEL 1
// ------------------------------------------------------------
// Esta función recibe una URL escrita como texto, por ejemplo:
//   "https://tienda.com/productos?categoria=libros#resenas"
// y debe devolver (con return) sus cinco partes.
function partesDeUrl(texto) {
  // Esta línea ya está hecha. `new URL(texto)` es una herramienta
  // que JavaScript trae de fábrica: desarma la URL por ti.
  // Guarda el resultado en una caja llamada `url`.
  // Lo que hay dentro de `url`: https://developer.mozilla.org/en-US/docs/Web/API/URL
  const url = new URL(texto);

  // Tu trabajo: cambiar cada `null` por la parte correcta.
  // Para leer una parte se escribe: url.nombreDeLaParte
  return {
    // Pista: en MDN se llama `protocol`.
    // Ojo: viene con un ":" de más al final ("https:").
    // Quítalo con .replace(...). Busca cómo se usa:
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/String/replace
    esquema: null,

    // Pista: en MDN se llama `hostname`. Este viene limpio.
    dominio: null,

    // Pista: en MDN se llama `pathname`. Este también viene limpio.
    ruta: null,

    // Pista: en MDN se llama `search`.
    // Ojo: viene con un "?" de más al inicio. También se quita con .replace(...).
    parametros: null,

    // Pista: en MDN se llama `hash`.
    // Ojo: viene con un "#" de más al inicio.
    ancla: null,
  };
}

// ------------------------------------------------------------
// NIVEL 2 (reto, solo si el Nivel 1 ya está en verde)
// ------------------------------------------------------------
// Esta función recibe una URL y el nombre de UN parámetro,
// y devuelve su valor. Ejemplo:
//   parametro("https://tienda.com/productos?categoria=libros", "categoria")
//   debe devolver "libros"
function parametro(texto, nombre) {
  const url = new URL(texto);

  // Pista: `url.searchParams` guarda los parámetros ya separados.
  // Tiene un método `.get(...)` que recibe un nombre.
  // Si el parámetro no existe, `.get(...)` ya devuelve null solito.
  // https://developer.mozilla.org/en-US/docs/Web/API/URLSearchParams/get
  return null;
}

// No toques esta línea: deja que las pruebas encuentren tus funciones.
if (typeof module !== "undefined") module.exports = { partesDeUrl, parametro };
