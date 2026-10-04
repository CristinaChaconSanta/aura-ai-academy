// Pruebas del taller N1-M1: Desarma una URL.
// No necesitas editar este archivo. Léelo si quieres ver qué se espera.
(function () {
  var lib, sol;

  if (typeof window === "undefined") {
    // Node: load the lib and the solution file.
    var path = require("path");
    lib = require(path.join(__dirname, "../_lib/mini-prueba.js"));
    var archivo = path.resolve(process.env.TALLER_SOLUCION || path.join(__dirname, "solucion.js"));
    try {
      sol = require(archivo);
    } catch (error) {
      console.log("❌ No pude leer solucion.js");
      console.log("   tu código lanzó un error: " + error.message);
      console.log("   Revisa que no falte un paréntesis, una llave o una coma.");
      process.exitCode = 1;
      return;
    }
  } else {
    // Browser: everything is global.
    lib = window.miniPrueba;
    sol = window;
  }

  var prueba = lib.prueba;
  var igual = lib.igual;

  var TIENDA = "https://tienda.com/productos?categoria=libros#resenas";
  var DIARIO = "https://diario.com/deportes?fecha=hoy#futbol";

  // ---------- Nivel 1 ----------
  prueba("El esquema de la tienda es https (sin los dos puntos)", function () {
    igual(sol.partesDeUrl(TIENDA).esquema, "https");
  });

  prueba("El dominio de la tienda es tienda.com", function () {
    igual(sol.partesDeUrl(TIENDA).dominio, "tienda.com");
  });

  prueba("La ruta de la tienda es /productos", function () {
    igual(sol.partesDeUrl(TIENDA).ruta, "/productos");
  });

  prueba("Los parámetros de la tienda son categoria=libros (sin el ?)", function () {
    igual(sol.partesDeUrl(TIENDA).parametros, "categoria=libros");
  });

  prueba("El ancla de la tienda es resenas (sin el #)", function () {
    igual(sol.partesDeUrl(TIENDA).ancla, "resenas");
  });

  prueba("El diario se desarma completo en sus cinco partes", function () {
    igual(sol.partesDeUrl(DIARIO), {
      esquema: "https",
      dominio: "diario.com",
      ruta: "/deportes",
      parametros: "fecha=hoy",
      ancla: "futbol",
    });
  });

  prueba("Una URL sin parámetros ni ancla devuelve textos vacíos", function () {
    var partes = sol.partesDeUrl("https://elespectador.com/opinion");
    igual(partes.parametros, "", "Si no hay ?, parametros debe ser \"\" (texto vacío).");
    igual(partes.ancla, "", "Si no hay #, ancla debe ser \"\" (texto vacío).");
  });

  prueba("Con dos parámetros, se ven los dos unidos por &", function () {
    var partes = sol.partesDeUrl("https://tienda.com/productos?categoria=libros&orden=precio");
    igual(partes.parametros, "categoria=libros&orden=precio");
  });

  // ---------- Nivel 2 ----------
  prueba("Reto: el parámetro orden vale precio", function () {
    igual(
      sol.parametro("https://tienda.com/productos?categoria=libros&orden=precio", "orden"),
      "precio"
    );
  });

  prueba("Reto: fecha vale hoy, y un parámetro que no existe devuelve null", function () {
    igual(sol.parametro(DIARIO, "fecha"), "hoy");
    igual(sol.parametro(DIARIO, "autor"), null, "Si el parámetro no está en la URL, devuelve null.");
  });

  lib.resumen();
})();
