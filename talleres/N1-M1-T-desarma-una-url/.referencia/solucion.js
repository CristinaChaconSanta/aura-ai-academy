// Reference solution for taller N1-M1-T. Do not show to the learner.
function partesDeUrl(texto) {
  const url = new URL(texto);
  return {
    esquema: url.protocol.replace(":", ""),
    dominio: url.hostname,
    ruta: url.pathname,
    parametros: url.search.replace("?", ""),
    ancla: url.hash.replace("#", ""),
  };
}

function parametro(texto, nombre) {
  const url = new URL(texto);
  return url.searchParams.get(nombre);
}

if (typeof module !== "undefined") module.exports = { partesDeUrl, parametro };
