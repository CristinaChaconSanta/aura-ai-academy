// mini-prueba.js: tiny zero-dependency test helper for the talleres.
// Works in Node (CommonJS) and in the browser (plain <script>, globals).
// API: prueba(nombre, fn), igual(obtenido, esperado, mensaje?), resumen().
(function (global) {
  "use strict";

  var resultados = [];

  // Marks a failed comparison, so we can tell it apart from a crash.
  function FalloDePrueba(mensaje) {
    this.name = "FalloDePrueba";
    this.message = mensaje;
  }
  FalloDePrueba.prototype = Object.create(Error.prototype);

  // Deep equality for primitives, arrays and plain objects.
  function sonIguales(a, b) {
    if (a === b) return true;
    if (typeof a !== "object" || typeof b !== "object" || a === null || b === null) {
      return a !== a && b !== b; // NaN === NaN
    }
    if (Array.isArray(a) !== Array.isArray(b)) return false;
    var llavesA = Object.keys(a);
    var llavesB = Object.keys(b);
    if (llavesA.length !== llavesB.length) return false;
    for (var i = 0; i < llavesA.length; i++) {
      var k = llavesA[i];
      if (!Object.prototype.hasOwnProperty.call(b, k)) return false;
      if (!sonIguales(a[k], b[k])) return false;
    }
    return true;
  }

  // Human-readable value: strings with quotes, undefined spelled out.
  function mostrar(valor) {
    if (valor === undefined) return "undefined (nada)";
    if (typeof valor === "function") return "una función";
    try {
      return JSON.stringify(valor);
    } catch (e) {
      return String(valor);
    }
  }

  function igual(obtenido, esperado, mensaje) {
    if (sonIguales(obtenido, esperado)) return;
    var texto = "esperaba " + mostrar(esperado) + ", obtuve " + mostrar(obtenido) + ".";
    if (mensaje) texto = mensaje + "\n   " + texto;
    throw new FalloDePrueba(texto);
  }

  function prueba(nombre, fn) {
    try {
      fn();
      resultados.push({ nombre: nombre, pasa: true, detalle: "" });
    } catch (error) {
      var detalle;
      if (error instanceof FalloDePrueba) {
        detalle = error.message;
      } else {
        var msg = error && error.message ? error.message : String(error);
        detalle = "tu código lanzó un error: " + msg;
      }
      resultados.push({ nombre: nombre, pasa: false, detalle: detalle });
    }
  }

  function contar() {
    var pasan = 0;
    for (var i = 0; i < resultados.length; i++) if (resultados[i].pasa) pasan++;
    return { pasan: pasan, total: resultados.length };
  }

  function resumenNode() {
    var c = contar();
    console.log("");
    resultados.forEach(function (r) {
      if (r.pasa) {
        console.log("✅ " + r.nombre);
      } else {
        console.log("❌ " + r.nombre);
        console.log("   " + r.detalle);
      }
    });
    console.log("");
    console.log(c.pasan + " de " + c.total + " pruebas pasan");
    if (c.pasan === c.total) console.log("¡Todo en verde! 🎉");
    if (c.pasan !== c.total) process.exitCode = 1;
    return c;
  }

  function resumenNavegador() {
    var c = contar();
    var caja = document.getElementById("resultados");
    if (!caja) {
      caja = document.createElement("div");
      caja.id = "resultados";
      document.body.appendChild(caja);
    }
    caja.innerHTML = "";

    var arriba = document.createElement("p");
    arriba.style.fontSize = "1.6em";
    arriba.style.fontWeight = "bold";
    arriba.style.color = c.pasan === c.total ? "#11702b" : "#a31616";
    arriba.textContent =
      c.pasan + " de " + c.total + " pruebas pasan" + (c.pasan === c.total ? " 🎉" : "");
    caja.appendChild(arriba);

    resultados.forEach(function (r) {
      var fila = document.createElement("div");
      fila.style.fontSize = "1.25em";
      fila.style.lineHeight = "1.5";
      fila.style.margin = "0.6em 0";
      fila.style.padding = "0.5em 0.8em";
      fila.style.borderRadius = "8px";
      fila.style.background = r.pasa ? "#e3f6e8" : "#fde7e7";
      fila.style.color = r.pasa ? "#11702b" : "#a31616";
      fila.textContent = (r.pasa ? "✅ " : "❌ ") + r.nombre;
      if (!r.pasa) {
        var detalle = document.createElement("div");
        detalle.style.fontSize = "0.85em";
        detalle.style.whiteSpace = "pre-wrap";
        detalle.style.color = "#5a1010";
        detalle.textContent = r.detalle;
        fila.appendChild(detalle);
      }
      caja.appendChild(fila);
    });
    return c;
  }

  function resumen() {
    var enNode = typeof process !== "undefined" && process.versions && process.versions.node;
    return enNode && typeof document === "undefined" ? resumenNode() : resumenNavegador();
  }

  var api = { prueba: prueba, igual: igual, resumen: resumen };

  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  } else {
    global.miniPrueba = api;
    global.prueba = prueba;
    global.igual = igual;
    global.resumen = resumen;
  }
})(typeof window !== "undefined" ? window : this);
