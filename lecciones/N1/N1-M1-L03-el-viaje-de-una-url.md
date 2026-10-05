---
id: N1-M1-L03
titulo: El viaje de una URL
nivel: 1
duracion_min: 28
estado: borrador
prerequisitos: [N1-M1-L01]
fuentes:
  - https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works
  - https://developer.mozilla.org/en-US/docs/Glossary/HTTP
  - https://developer.mozilla.org/en-US/docs/Glossary/HTTPS
  - https://developer.mozilla.org/en-US/docs/Glossary/Hypertext
  - https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL
glosario: [cliente y servidor, DNS, dirección IP, HTTP, paquete]
---

## 1. El gancho ⏱ 1 min
Escribes `elespectador.com` y en un segundo tienes la portada en pantalla.
Parece instantáneo, pero en ese segundo tu navegador hizo varias cosas, una detrás de otra.

Cuando una web "no carga", el problema está en uno de esos pasos.
Si sabes cuáles son y cómo se llaman, puedes preguntarle a la IA algo concreto en lugar de "no funciona".

¿Qué crees que pasa entre el momento en que pulsas Enter y el momento en que ves la portada?

## 2. La idea en una frase ⏱ 30 s
**El navegador traduce el nombre del sitio a un número, le pide la página al computador que tiene ese número y arma lo que recibe en pedazos.**

## 3. Las palabras nuevas ⏱ 5 min
Esta lección tiene cinco palabras nuevas. Cada una es un actor o una pieza del viaje.
Usaremos la dirección de N1-M1-L01, donde ya separaste esquema, dominio y ruta:

```text
https://tienda.com/productos
```

### Cliente y servidor
**Qué es:** el *cliente* es quien pide (tu navegador). El *servidor* es el computador que responde y entrega la página.

**Ejemplo:** tu Chrome es el cliente. El computador de `tienda.com` es el servidor.

<details><summary>Por qué se llama así</summary>

Como en un negocio: el cliente pide un servicio y el servidor lo sirve.
MDN, la documentación web de referencia, usa la imagen de una carretera: en una punta está tu casa (el cliente) y en la otra, la tienda (el servidor).

</details>

### DNS
**Qué es:** el sistema que traduce un dominio a una dirección IP.

**Ejemplo:** le preguntas al DNS por `mozilla.org` y te responde con un número como `192.0.2.172`.

<details><summary>Por qué se llama así</summary>

Son las siglas de *Domain Name System*, "sistema de nombres de dominio".
MDN lo compara con la libreta de direcciones de los sitios web.

</details>

### Dirección IP
**Qué es:** el número que identifica a un computador en internet. Los computadores se encuentran entre sí por ese número, no por el nombre.

**Ejemplo:** `192.0.2.172`.

<details><summary>Por qué se llama así</summary>

IP son las siglas de *Internet Protocol*, "protocolo de internet".
Un *protocolo* es un conjunto de reglas de comunicación. La dirección IP es la dirección que usan esas reglas.

</details>

### HTTP
**Qué es:** las reglas de conversación entre el navegador y el servidor: cómo se pide una página y cómo se responde.

**Ejemplo:** el navegador manda "dame la página `/productos`" y el servidor contesta `200 OK`, que significa "sí, aquí va".

<details><summary>Por qué se llama así</summary>

Son las siglas de *HyperText Transfer Protocol*, "protocolo de transferencia de hipertexto".
*Hipertexto* es texto con enlaces a otros textos, en lugar de un hilo lineal como el de una novela. El término lo acuñó Ted Nelson hacia 1965.
HTTPS es la misma conversación, pero cifrada (escrita en un código que nadie más puede leer en el camino). La S viene de *Secure*, "seguro".

</details>

### Paquete
**Qué es:** cada uno de los pedazos pequeños en que viaja la información por internet.

**Ejemplo:** una página llega en muchos paquetes. Pueden llegar desordenados, y el navegador los vuelve a ordenar con los números de las etiquetas.

<details><summary>Por qué se llama así</summary>

En inglés, *packet*, "paquetito".
Cada uno lleva una etiqueta (llamada *header*, "encabezado") con datos como de dónde viene, a dónde va y qué número de pedazo es.
Dentro va el contenido, que se llama *payload*, "carga".

</details>

## 4. La analogía ⏱ 2 min
Piensa en pedirle una foto a una agencia de noticias.

Sabes el nombre de la agencia, pero no su número de teléfono.
Buscas el número en el directorio, llamas y haces el pedido formal.
La agencia te manda la foto por partes numeradas.
Tú las juntas en orden y ya tienes la imagen completa.

| En la agencia | En internet |
| :-- | :-- |
| Nombre de la agencia | Dominio (`elespectador.com`) |
| Directorio telefónico | DNS |
| Número de teléfono | Dirección IP |
| Pedido formal | Petición HTTP |
| "Sí, aquí va" | Respuesta `200 OK` |
| Partes numeradas | Paquetes |

**Dónde se rompe la analogía:** en la agencia una persona decide si te atiende. En internet, el servidor es un programa que responde solo, sin que nadie revise tu pedido a mano.

## 5. Diagrama ⏱ 2 min
Mira primero el nodo DNS: el navegador no puede hablar con el servidor hasta que el DNS le da el número.

```mermaid
flowchart LR
  T["Tú escribes la URL"] --> N["Navegador (cliente)"]
  N -->|"1. ¿qué IP tiene tienda.com?"| D["DNS"]
  D -->|"2. 192.0.2.172"| N
  N -->|"3. petición HTTP"| S["Servidor"]
  S -->|"4. 200 OK, en paquetes"| N
  N --> P["Página armada en tu pantalla"]
  style D fill:#ffe08a,stroke:#333
```

## 6. Contraste ⏱ 2 min
Tres palabras que se usan como si fueran lo mismo:

| | URL | Dominio | Dirección IP |
| :-- | :-- | :-- | :-- |
| Qué es | La dirección completa de un recurso | El nombre del servidor | El número real del servidor |
| Ejemplo | `https://tienda.com/productos` | `tienda.com` | `192.0.2.172` |
| Quién la usa | Tú, al escribir o compartir un enlace | Tú y el DNS | Los computadores entre sí |
| En la agencia | La dirección con piso y oficina | El nombre de la agencia | El número de teléfono |

## 7. ¿Cuál falla? ⏱ 3 min
Una IA te resume el viaje de una URL de dos maneras.

**A**
```text
1. El navegador le pide la página al servidor de tienda.com
2. El DNS traduce tienda.com a una dirección IP
3. El servidor responde 200 OK y la página llega en paquetes
```

**B**
```text
1. El DNS traduce tienda.com a una dirección IP
2. El navegador le pide la página al servidor (petición HTTP)
3. El servidor responde 200 OK y la página llega en paquetes
```

¿Cuál falla y por qué?

<details><summary>Respuesta</summary>

Falla **A**. Así se resuelve, paso a paso:

1. Pregúntate qué necesita el navegador para hablar con el servidor: su número, la dirección IP.
2. Busca en qué paso consigue ese número: cuando el DNS traduce el dominio.
3. En A, el paso 1 pide la página antes de tener el número. Ese paso todavía no se puede hacer.
4. En B, primero el DNS entrega el número y después sale la petición. Así lo cuenta MDN.
5. Conclusión: A tiene los pasos en desorden. El DNS va primero.

</details>

## 8. Ponte a prueba ⏱ 3 min
Explícalo con tus palabras (2 frases) antes de abrir la respuesta.

1. ¿Qué hace el DNS y por qué hace falta?
<details><summary>Respuesta</summary>Traduce el dominio (un nombre fácil de recordar) a la dirección IP (el número que usan los computadores). Hace falta porque los computadores se encuentran por número, no por nombre.</details>

2. Una web no carga y una IA te dice "el sitio está caído". ¿Qué le preguntarías?
<details><summary>Respuesta</summary>En qué paso falló: el DNS (no encontró el número), la conexión o la respuesta del servidor. Cada uno se arregla distinto.</details>

3. Una IA escribe un programa que se conecta a `192.0.2.172` en vez de a `tienda.com`. ¿Qué está mal?
<details><summary>Respuesta</summary>Puso una dirección IP fija en lugar del dominio. Lo habitual es usar el dominio y dejar que el DNS haga la traducción. Pregúntale por qué lo hizo así.</details>

## 9. Mini ejercicio ⏱ 5 min
1. Escribe `developer.mozilla.org` en la barra de direcciones y pulsa Enter.
2. Abre las herramientas de desarrollador con `Cmd + Option + I` y ve a la pestaña **Network** (red).
3. Recarga la página y mira la columna **Status** (estado) de la primera fila.

**Sabrás que lo lograste cuando:** veas el número `200` en la columna Status y puedas decir qué significa: "sí, aquí va".

## 10. Cómo te ayuda a revisar a la IA ⏱ 2 min
Cuando algo no carga, este es el tipo de diagnóstico que no te sirve:

> Salida de IA: "Tu sitio está caído. Vuelve a intentarlo más tarde."

- Pregúntale en qué paso falló: DNS, conexión o respuesta del servidor. Cada uno se arregla distinto.
- Si una IA pone una dirección IP fija en el código en vez del dominio, pregunta por qué. Lo habitual es usar el dominio y dejar que el DNS haga la traducción.

## 11. Cómo se conecta ⏱ 2 min
**Viene de:** N1-M1-L01. El dominio que aprendiste a separar es el nombre que el DNS traduce a número.

**Lleva a:** cada paso del viaje tiene su lección propia. N1-M1-L04 (cliente y servidor), N1-M1-L05 (HTTP y sus códigos, como el 200), N1-M1-L06 (DNS y dominios) y N1-M1-L07 (HTTPS y certificados).

**Si lo combinas con…:** N1-M1-L02, sabes qué parte de la URL viaja en la petición y cuál se queda en tu navegador. Los parámetros llegan al servidor; el ancla nunca se envía.

```mermaid
flowchart LR
  L01["N1-M1-L01 Partes de una URL"] --> L03["N1-M1-L03 El viaje de una URL"]
  L02["N1-M1-L02 Parámetros y anclas"] -.-> L03
  L03 --> L04["N1-M1-L04 Cliente y servidor"]
  L03 --> L05["N1-M1-L05 HTTP"]
  L03 --> L06["N1-M1-L06 DNS y dominios"]
  L03 --> L07["N1-M1-L07 HTTPS"]
  style L03 fill:#ffe08a,stroke:#333
```

## 12. Ya puedes ⏱ 10 s
Ya puedes contar en cuatro pasos qué pasa entre pulsar Enter y ver una página, y preguntarle a la IA en cuál falló.

## 13. Fuentes
<details><summary>Fuentes</summary>

- [How the web works (MDN)](https://developer.mozilla.org/en-US/docs/Learn_web_development/Getting_started/Web_standards/How_the_web_works): pasos DNS, HTTP, 200 OK, paquetes con encabezado y carga; analogía de la carretera; libreta de direcciones; ejemplo de IP.
- [HTTP (MDN Glossary)](https://developer.mozilla.org/en-US/docs/Glossary/HTTP): significado de *HyperText Transfer Protocol*.
- [HTTPS (MDN Glossary)](https://developer.mozilla.org/en-US/docs/Glossary/HTTPS): *HyperText Transfer Protocol Secure*, versión cifrada de HTTP.
- [Hypertext (MDN Glossary)](https://developer.mozilla.org/en-US/docs/Glossary/Hypertext): definición de hipertexto y su origen (Ted Nelson, hacia 1965).
- [What is a URL? (MDN)](https://developer.mozilla.org/en-US/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL): los parámetros los recibe el servidor; lo que va después de `#` nunca se envía con el pedido.

</details>
