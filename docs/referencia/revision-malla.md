# Revisión de la malla "De Vibecoder a Chief AI Officer"

Documento base: 4 respuestas de Perplexity concatenadas (4.060 líneas).
Este archivo tiene dos partes: **A. qué arreglar** y **B. qué agregar**.

---

## A. Qué arreglar del documento actual

### A1. Problemas de estructura

| Problema | Dónde | Por qué importa |
| :-- | :-- | :-- |
| Hay **4 versiones distintas** de la malla (Módulos 1-4, Niveles 1-5, Fases 0-3, Partes I-IV) | Líneas 21, 349, 2253, 2528 | Con TDAH, cuatro mapas que no coinciden = no hay mapa. Hace falta UNA estructura canónica. |
| Hay **3 rúbricas** diferentes | Líneas 84, 461, 2418 | Ninguna dice cómo se demuestra cada nivel. |
| "El Gran Libro Blanco" aparece **dos veces** con contenido distinto | Líneas 527 y 2502 | Duplicación. |
| **El documento está cortado**: la Parte IV (Seguridad) se rompe en "Adversarial Suffix" y la línea 4038 tiene ~54.000 caracteres de `! ! ! !` | Línea 4038 | El modelo de Perplexity entró en un loop. La parte de seguridad de IA quedó incompleta. |
| No hay **proyectos evaluables** por nivel | Todo | Sin entregable, no hay forma de saber si aprendiste. |

### A2. Errores o afirmaciones dudosas

| Afirmación del doc | Corrección |
| :-- | :-- |
| "LAM: InstructDiffusion" (línea 3314) | InstructDiffusion es un modelo de **edición de imágenes** por difusión, no un modelo de acciones. |
| "MoE: GPT-4" (línea 3342) | OpenAI **nunca confirmó** la arquitectura de GPT-4. Es rumor. Mixtral sí es MoE confirmado. |
| "VLM: CLIP" | CLIP no genera texto; es un modelo de **embeddings** imagen-texto. Útil, pero no es lo mismo que un VLM conversacional. |
| "Cross-Prompt Injection" como tipo propio | No es un término estándar. Lo que describe es **indirect prompt injection vía RAG** (data poisoning). |
| Los 5 patrones (ReAct, Plan-and-Execute, Reflexion, Evaluator-Optimizer, Orchestrator-Workers) | Están bien, pero falta la fuente: ReAct (Yao et al., 2022) y Reflexion (Shinn et al., 2023) son papers; Evaluator-Optimizer y Orchestrator-Workers vienen del post de Anthropic **"Building effective agents"** (dic. 2024), que además agrega **Prompt Chaining, Routing y Parallelization**. |
| "PCI-DSS: si no lo cumples, te multan" | Simplificado. Si usas Stripe Checkout / Wompi con redirección, la tarjeta nunca toca tu servidor y tu carga de cumplimiento es mínima (cuestionario SAQ A). El riesgo real está en el **webhook sin verificar firma**. |
| "2 semanas entendiendo Python" | Irreal para alguien sin base. Mejor: medir por **capacidad demostrada**, no por semanas. |
| "Python es ideal para TDAH" | No hay evidencia de eso. Python es buena opción por el ecosistema de IA, no por neurodivergencia. |
| Recomienda Python + React + Next + LangFlow + Flowise + n8n | Demasiados lenguajes y herramientas a la vez. Elegir **un stack** (ver B9). |
| Citas de "Julián Campos" y "Flavio Copes" (sept. 2026) | No pude verificarlas. El contenido es razonable, pero conviene enlazar el post original. |
| Codewars / LeetCode como gamificación | Entrenan algoritmos de entrevista, no lo que necesitas (leer, diseñar, depurar). Mejor gamificar con tu propio tablero de proyectos. |

### A3. Qué conservar (está bien)

- La metáfora **arquitecta vs. albañil**.
- Las tablas con **analogía + herramienta visual** por tema.
- Los **10 fundamentales** (HTTP, Git, SQL, terminal, navegador, async, seguridad, DNS, leer código, testing).
- La **tipología de sitios web** (estático, CMS, e-commerce, SaaS, dashboard).
- El contenido de @silvanrec sobre los niveles de madurez de agentes.

---

## B. Qué agregar (temas que NO están en el documento)

### B1. Fundamentos reales de IA (el hueco más grande)

El doc salta de "13 tipos de modelos" a "Transformer" sin lo que de verdad necesitas para **dirigir** un modelo.

| Tema | Qué es | Analogía |
| :-- | :-- | :-- |
| **Tokens** | La unidad en que el modelo lee y cobra. ~1 token ≈ ¾ de palabra en inglés; en español gasta más. | Como cobrar un telegrama por sílabas, no por palabras. |
| **Ventana de contexto** | Todo lo que el modelo "ve" en un turno. Lo que no está ahí, no existe para él. | La mesa de trabajo de una editora: solo edita lo que tiene encima. |
| **Context rot** | Con mucho contexto, el modelo presta peor atención a lo del medio. | Un reportero con 40 pestañas abiertas. |
| **Predicción del siguiente token** | Un LLM no "sabe", calcula la continuación más probable. | El autocompletar del celular, entrenado con internet. |
| **Por qué alucina** | Siempre produce algo plausible, aunque no tenga el dato. | Un entrevistado que nunca dice "no sé". |
| **Temperatura y muestreo** | Cuánto azar hay al elegir el siguiente token. | Redacción de manual (baja) vs. lluvia de ideas (alta). |
| **Cómo se entrena** | Preentrenamiento → ajuste con instrucciones (SFT) → ajuste con preferencias humanas o de IA (RLHF / RLAIF / Constitutional AI). | Leer toda la biblioteca → hacer la práctica → recibir correcciones del editor. |
| **Modelos de razonamiento** | "Piensan" más tokens antes de responder (test-time compute). Más lentos y caros, mejores en lógica. | Responder al aire vs. pedir 10 minutos para investigar. |
| **Prompting vs. RAG vs. fine-tuning** | Cuándo usar cada uno. | Dar instrucciones / dar el archivo / reentrenar a la persona. |
| **Costo y latencia** | Elegir modelo grande vs. pequeño según la tarea. | No mandas al editor general a corregir comas. |
| **Por qué los benchmarks engañan** | Contaminación de datos, métricas que no reflejan tu caso. | Un ranking de universidades no te dice si esa carrera te sirve. |
| **Modelos abiertos vs. cerrados** | Pesos descargables (Llama, Qwen, Mistral) vs. API (Claude, GPT, Gemini). | Comprar el carro vs. tomar taxi. |

**Recorte sugerido:** de los "13 tipos de modelos", quedarse con LLM, SLM, modelo de razonamiento, multimodal y embeddings. SSM, LNN, SAM, CNN son cultura general, no fundamentos para tu objetivo.

### B2. Context engineering (más allá del prompt)

El doc habla de "ingeniería de prompts". Hoy el concepto es más amplio:

- **System prompt** vs. mensaje del usuario.
- **Archivos de instrucciones del proyecto**: `CLAUDE.md`, `AGENTS.md`, `.cursor/rules`.
- **Skills**, **subagentes**, **hooks**, **MCP servers**: qué es cada uno y cuándo usarlo.
- **Compactación** y cómo un agente pierde el hilo en sesiones largas.
- **Ejemplos (few-shot)** y **salida estructurada** (JSON schema).
- **Tool design**: una herramienta mal descrita es un agente confundido.

### B3. Metodologías de desarrollo (lo pediste y casi no está)

| Metodología | Idea central | Cuándo sirve |
| :-- | :-- | :-- |
| **Agile / Scrum** | Iteraciones cortas (sprints) con revisión. | Equipos con cliente que cambia de idea. |
| **Kanban** | Flujo continuo, límite de tareas en curso. | Ideal para TDAH: ves todo en un tablero. |
| **Shape Up** (Basecamp) | Ciclos de 6 semanas con problema bien acotado. | Producto con equipo pequeño. |
| **TDD** (Test-Driven Development) | Primero el test que falla, luego el código. | Muy potente con IA: el test es el contrato que el agente debe cumplir. |
| **BDD** | Tests escritos como frases ("Dado… cuando… entonces…"). | Para alguien que escribe bien: es redacción. |
| **DDD** (Domain-Driven Design) | El código usa el lenguaje del negocio. | Productos con reglas complejas. |
| **Spec-Driven Development** | Escribir la especificación antes de que el agente codee. | El método más natural para vibecoding serio. |
| **Trunk-based + CI/CD** | Cambios pequeños, integrados y desplegados seguido. | Base de todo despliegue moderno. |
| **Métricas DORA** | Frecuencia de despliegue, tiempo de cambio, tasa de fallo, tiempo de recuperación. | Para medir si un equipo entrega bien (útil en el rol CAIO). |

### B4. Producto antes que código (tu ventaja como periodista)

- **Problema → usuario → resultado medible** antes de cualquier prompt.
- **Historias de usuario** y **criterios de aceptación**.
- **PRD** (documento de requisitos de producto).
- **Entrevistas a usuarios**: es periodismo aplicado.
- **Alcance**: qué NO va en la versión 1.

### B5. Web: temas profundos que faltan

**Cómo se arma una página**
- Renderizado: **SSG, SSR, CSR, ISR**. Qué es cada uno y por qué afecta velocidad y SEO.
- **Caché y CDN**.
- **Core Web Vitals** (velocidad medible).
- **SEO técnico** y **accesibilidad** (WCAG).
- **Internacionalización** (idiomas, monedas, zonas horarias).

**Cómo funciona por detrás**
- **Trabajos en segundo plano y colas** (enviar 1.000 correos sin colgar la web).
- **Cron jobs** y tareas programadas.
- **Subida de archivos** y almacenamiento (S3, Supabase Storage).
- **Correo transaccional** y por qué cae en spam (**SPF, DKIM, DMARC**).
- **Rate limiting** (evitar abuso).
- **Migraciones de base de datos** (cambiar la estructura sin perder datos).

**Apps con login (SaaS)**
- **Autenticación vs. autorización** (quién eres vs. qué puedes hacer).
- **Roles y permisos** (RBAC) y **Row Level Security** en Supabase.
- **Multi-tenancy**: que el cliente A nunca vea datos del cliente B.
- Sesiones, cookies `httpOnly`, recuperación de contraseña, **MFA**.

**Pagos (lo que más plata cuesta si sale mal)**
- **Verificar la firma del webhook** (si no, cualquiera puede "avisar" que pagó).
- **Idempotencia**: el mismo webhook llega dos veces y no debes cobrar ni entregar dos veces.
- Estados del pago: pendiente, aprobado, rechazado, reembolsado, **contracargo**.
- **Modo prueba vs. producción**.
- Suscripciones: renovación, fallo de cobro, cancelación, prorrateo.

**Marketplace (más difícil que e-commerce)**
- **Pagos divididos** (split payments; ej. Stripe Connect): comisión de la plataforma + pago al vendedor.
- **KYC** (verificar identidad de vendedores).
- Disputas, reembolsos, retención de fondos.
- Reputación y reseñas (y fraude en reseñas).
- Impuestos y retenciones.

**Contexto Colombia** (verificar vigencia antes de usar)
- Pasarelas locales: **Wompi, ePayco, PayU, Mercado Pago**; medios **PSE, Nequi, Daviplata**.
- **Facturación electrónica DIAN**.
- **Ley 1581 de 2012** (protección de datos personales / habeas data).

### B6. Operación: lo que pasa después del deploy

- **Entornos**: desarrollo, staging, producción.
- **Variables de entorno y secretos** (nunca en el repo).
- **Logs, métricas, alertas**; qué es un **baseline**.
- **Feature flags** y despliegue gradual (canary).
- **Rollback** (volver atrás rápido).
- **Backups y prueba de restauración** (un backup que nunca restauraste no es backup).
- **Respuesta a incidentes** y **postmortem sin culpables**.
- **Costos de nube y de tokens** (FinOps).

### B7. Seguridad: lo que quedó cortado + lo nuevo

**Web clásica**
- **OWASP Top 10** (versión vigente): control de acceso roto, inyección, fallos criptográficos, configuración insegura, etc.
- **IDOR**: cambiar `/factura/123` por `/factura/124` y ver la de otro. El fallo más común en apps hechas con IA.
- CORS, CSRF, headers de seguridad.
- **Cadena de suministro**: dependencias vulnerables, `npm audit`.

**Específico de IA**
- **OWASP Top 10 para LLMs (2025)**: prompt injection, filtración de datos sensibles, cadena de suministro, envenenamiento de datos, manejo inseguro de la salida, **agencia excesiva**, filtración del system prompt, debilidades en vectores/embeddings, desinformación, **consumo sin límites**.
- **La "trifecta letal"** (Simon Willison): un agente con (1) acceso a datos privados + (2) contenido no confiable + (3) capacidad de enviar datos hacia afuera = puede ser usado para robar información.
- **Slopsquatting**: la IA inventa un paquete que no existe; un atacante lo publica con ese nombre.
- Riesgos de **MCP servers** de terceros.
- **Mínimo privilegio** y **humano en el loop** para acciones irreversibles.
- **Sandboxing** del agente.

### B8. Evals (cómo saber si tu agente funciona)

- **Análisis de errores**: leer 50-100 conversaciones reales y clasificar los fallos a mano antes de automatizar nada.
- **Dataset dorado**: casos de prueba con respuesta esperada.
- **LLM-as-judge** y sus trampas (sesgo de posición, preferencia por respuestas largas).
- **Evals de regresión** antes de cambiar un prompt o un modelo.
- Nociones de **estadística**: con 10 casos no puedes concluir nada.

### B9. Decisión de stack (una sola ruta)

Recomendación para tu caso: **TypeScript de punta a punta**.

| Opción | A favor | En contra |
| :-- | :-- | :-- |
| **TypeScript (Next.js + Supabase)** | Un solo lenguaje para front, back y agentes; los tipos atrapan errores de la IA. | Menos tutoriales de ML puro. |
| Python (FastAPI) + React | Ecosistema de IA/datos más grande. | Dos lenguajes = el doble de cosas que leer. |

Python se aprende después, solo cuando un proyecto lo pida (datos, ML).

### B10. Mínimo de ciencias de la computación

- Cómo funciona un computador: CPU, memoria, disco, procesos.
- **Estructuras de datos** básicas: lista, diccionario, árbol, grafo.
- **Big-O por intuición**: por qué un código va bien con 10 usuarios y muere con 10.000.
- **Concurrencia**: dos personas compran el último producto al mismo tiempo.

### B11. Experiencia de usuario en productos con IA

- **Streaming** (que la respuesta aparezca mientras se genera).
- Mostrar **fuentes y citas**.
- Cómo comunicar **incertidumbre** y errores.
- **Escalar a humano** con buen diseño.
- Diseño de **flujos de aprobación** antes de acciones irreversibles.

### B12. Chief AI Officer: lo que falta

| Tema | Qué incluye |
| :-- | :-- |
| **Marcos regulatorios** | **EU AI Act** (niveles de riesgo), **NIST AI RMF**, **ISO/IEC 42001** (sistema de gestión de IA). Política nacional de IA de Colombia (verificar documento CONPES vigente). |
| **Gestión de proveedores** | Contratos con proveedores de modelos: retención de datos, entrenamiento con tus datos, ubicación de los servidores. |
| **Propiedad intelectual** | Copyright de contenido generado, licencias de modelos abiertos. |
| **Inventario y registro de IA** | Qué sistemas de IA usa la empresa, quién es responsable, nivel de riesgo. |
| **Gestión de incidentes de IA** | Qué pasa cuando el agente se equivoca con un cliente. |
| **Alfabetización en IA** | Programas de formación interna (el EU AI Act la exige). |
| **Medir adopción y valor** | Más allá del ROI: uso real, calidad, satisfacción. |
| **Datos como base** | Calidad de datos, gobierno de datos, contratos de datos. |
| **Portafolio de casos de uso** | Matriz impacto vs. factibilidad; qué se hace primero. |

### B13. Cómo aprender (con evidencia, no solo "tips TDAH")

Técnicas con respaldo (Dunlosky et al., 2013, y literatura posterior):

| Técnica | Qué es | Cómo la usaría el tutor |
| :-- | :-- | :-- |
| **Práctica de recuperación** | Recordar sin mirar, en lugar de releer. | El tutor pregunta antes de explicar. |
| **Repetición espaciada** | Repasar en intervalos crecientes. | Repasos al día 1, 3, 7, 21. |
| **Intercalado** | Mezclar temas en la práctica. | Un ejercicio de SQL y uno de seguridad juntos. |
| **Ejemplos resueltos** | Ver la solución paso a paso antes de intentar. | Contraste: código malo vs. bueno. |
| **Técnica Feynman** | Explicarlo con palabras simples. | "Escríbelo como nota de prensa de 150 palabras". |
| **Efecto protegido** | Aprender enseñando. | Publicar lo aprendido (ya eres comunicadora). |

Para TDAH: sesiones cortas con un entregable visible, tablero Kanban de aprendizaje, body doubling (estudiar acompañada, aunque sea por video).

### B14. Rúbrica basada en evidencia + proyectos ancla

Cada nivel se aprueba **con un entregable**, no con una sensación.

| Nivel | Proyecto ancla | Evidencia de aprobación |
| :-- | :-- | :-- |
| 1 | Landing page estática desplegada | Explicas qué pasa desde que escribes la URL hasta que ves la página (DNS → HTTP → HTML). |
| 2 | Blog con CMS y base de datos | Diseñas el modelo de datos en papel antes de pedirlo a la IA. |
| 3 | SaaS con login y datos por usuario | Demuestras que el usuario A no puede ver datos del usuario B (test de IDOR). |
| 4 | Tienda con pagos en modo prueba | Webhook con firma verificada e idempotente; manejas pago rechazado y reembolso. |
| 5 | Agente con RAG y herramientas | Tiene evals, logs, límite de pasos y de costo; pasa una prueba de prompt injection. |
| 6 | Marketplace o multiagente | Pagos divididos o arquitectura orquestador-workers con manejo de fallos. |
| 7 | Documento de estrategia de IA para una empresa real | Inventario de casos de uso, matriz de riesgo, business case y plan de gobernanza. |

### B15. Recursos de calidad (gratuitos o casi)

- **CS50x** (Harvard): fundamentos de computación.
- **MDN Web Docs**: referencia web.
- **The Odin Project**: ruta full-stack con proyectos.
- **Andrej Karpathy**: "Intro to Large Language Models" y "Deep Dive into LLMs" (YouTube).
- **3Blue1Brown**: serie visual de redes neuronales (ideal para aprendizaje visual).
- **Anthropic**: "Building effective agents" y la documentación de Claude Code.
- **Chip Huyen**: libro *AI Engineering* (O'Reilly, 2025).
- **Hamel Husain**: artículos sobre evals.
- **OWASP**: Top 10 web y Top 10 para LLMs.
- **DeepLearning.AI**: cursos cortos.

---

## C. Bloques que faltaban (segunda revisión)

### C1. Fundamentos de programación (antes que cualquier framework)

**Conceptos base** (iguales en todos los lenguajes)
- Variables y **tipos de datos** (texto, número, verdadero/falso, lista, diccionario).
- Condicionales, bucles, **funciones**.
- **Entrada → proceso → salida**.
- Errores y excepciones: qué significa un "stack trace".
- Leer documentación de una librería.

**Cómo se clasifican los lenguajes**

| Contraste | Lado A | Lado B | Analogía |
| :-- | :-- | :-- | :-- |
| Tipado | **Dinámico** (Python, JavaScript): el tipo se descubre al ejecutar. | **Estático** (TypeScript, Java, Go): el tipo se declara y se revisa antes. | Formulario sin validar vs. formulario que no te deja enviar si el teléfono tiene letras. |
| Ejecución | **Interpretado** (Python, JS): se lee línea por línea. | **Compilado** (Go, Rust, C): se traduce entero antes. | Intérprete simultáneo vs. traducción del libro completo. |
| Dónde corre | **Frontend** (navegador). | **Backend** (servidor). | El salón del restaurante vs. la cocina. |
| Nivel | **Alto nivel** (Python): cerca del idioma humano. | **Bajo nivel** (C): cerca del hardware. | Pedir "un café" vs. dar instrucciones a cada músculo del barista. |

**Paradigmas (formas de pensar un programa)**

| Paradigma | Idea | Analogía | Dónde lo verás |
| :-- | :-- | :-- | :-- |
| **Imperativo** | Pasos en orden: haz esto, luego esto. | Una receta. | Scripts. |
| **Orientado a objetos (POO)** | Todo es un "objeto" con datos y acciones. | Una ficha de personaje: atributos + lo que puede hacer. | Python, Java, muchos backends. |
| **Funcional** | Funciones que transforman datos sin modificar nada externo. | Una línea de montaje: entra materia prima, sale producto. | React, procesamiento de datos. |
| **Declarativo** | Dices **qué** quieres, no **cómo**. | Pedir en un restaurante vs. cocinar. | SQL, HTML, CSS. |
| **Orientado a eventos** | El código reacciona cuando algo pasa. | Un timbre: nada ocurre hasta que alguien toca. | Clics en la web, webhooks, agentes. |

**Los lenguajes que vas a encontrar**

| Lenguaje | Para qué se usa sobre todo |
| :-- | :-- |
| **HTML / CSS** | Estructura y estilo de páginas (no son lenguajes de programación en sentido estricto). |
| **JavaScript** | El único lenguaje que corre nativo en el navegador. También en servidor (Node.js). |
| **TypeScript** | JavaScript + tipos. Lo que genera Cursor/Claude Code en la mayoría de proyectos web hoy. |
| **Python** | IA, datos, automatización, backends. |
| **SQL** | Consultar bases de datos. |
| **Bash** | Comandos en la terminal. |
| Go, Rust, Java, C# | Sistemas grandes y de alto rendimiento. Saber que existen; no aprenderlos ahora. |

**Ciencias de la computación mínimas**
- Estructuras de datos: lista, diccionario, cola, **árbol**, **grafo**.
- Algoritmos por intuición: buscar, ordenar, recorrer un grafo.
- Big-O por intuición.
- Memoria, procesos, archivos.

### C2. La palabra "grafo" significa tres cosas distintas

| "Grafo" en… | Qué es | Ejemplo |
| :-- | :-- | :-- |
| **Estructura de datos** | Nodos unidos por conexiones. Concepto matemático base. | Mapa de metro: estaciones (nodos) y líneas (conexiones). |
| **Knowledge graph** (grafo de conocimiento) | Una base de datos donde guardas entidades y relaciones. | "Gabo — escribió → Cien años de soledad". Neo4j. GraphRAG. |
| **LangGraph** | Un framework que dibuja el **flujo de trabajo** de un agente como grafo: cada nodo es un paso, cada flecha es "qué sigue". | Nodo "buscar vuelos" → si es caro → nodo "probar otras fechas". |

Los tres usan la misma idea (nodos + conexiones) para cosas completamente distintas.

### C3. El ecosistema del AI Engineer

**Qué hace un AI Engineer** (contraste con otros roles)

| Rol | Qué hace | Analogía |
| :-- | :-- | :-- |
| **ML Engineer / Researcher** | Entrena y crea modelos. | Fabrica el motor. |
| **AI Engineer** | Construye productos usando modelos ya hechos (APIs). | Diseña el carro alrededor del motor. |
| **Software Engineer** | Construye sistemas en general. | Construye el carro completo, con o sin ese motor. |
| **Data Engineer** | Mueve y limpia datos. | Construye las carreteras y el combustible. |

**Las capas de herramientas**

| Capa | Qué resuelve | Herramientas |
| :-- | :-- | :-- |
| **Modelo** | El "cerebro". | Claude, GPT, Gemini, Llama. |
| **SDK del proveedor** | Hablar con el modelo desde código. | Anthropic SDK, OpenAI SDK, Vercel AI SDK. |
| **Framework de orquestación** | Encadenar pasos, herramientas y memoria. | **LangChain**, **LangGraph**, LlamaIndex, CrewAI, Claude Agent SDK, Mastra. |
| **Herramientas / conexiones** | Que el agente actúe en el mundo. | Function calling, **MCP**. |
| **Datos y memoria** | Que el agente sepa cosas. | Bases vectoriales (pgvector, Pinecone), grafos (Neo4j). |
| **Observabilidad y evals** | Saber si funciona. | LangSmith, Langfuse, Braintrust. |
| **No-code** | Automatizar sin programar. | n8n, Make, Zapier, Flowise. |

**LangChain vs. LangGraph**
- **LangChain**: caja de piezas para conectar modelos, prompts, herramientas y datos. Como un set de LEGO.
- **LangGraph** (de la misma empresa): para flujos de agente con estados, ciclos y decisiones. Es el plano que dice en qué orden se arman las piezas y qué pasa si algo falla.
- Nota: muchos equipos usan directamente el SDK del proveedor sin frameworks. Hay que entender ambos caminos.

**Otros conceptos del AI Engineer**
- Embeddings y búsqueda semántica.
- Chunking y re-ranking en RAG.
- GraphRAG (RAG con grafos de conocimiento).
- Fine-tuning y destilación (nivel conceptual).
- Modelos locales (Ollama).
- Guardrails (filtros de entrada y salida).
- Caché de prompts y control de costos.

### C4. Nube (cloud) y despliegue

**Conceptos base**

| Concepto | Qué es | Analogía |
| :-- | :-- | :-- |
| **Servidor** | Un computador encendido 24/7 que responde peticiones. | Una tienda que nunca cierra. |
| **Nube** | Alquilar servidores de otro (Amazon, Google, Microsoft) en lugar de comprarlos. | Alquilar oficina vs. construir edificio. |
| **IaaS / PaaS / SaaS** | Alquilas el terreno / el local amoblado / el servicio listo. | Lote vacío / oficina amoblada / coworking con café incluido. |
| **Serverless** | Tu código corre solo cuando alguien lo llama; pagas por uso. | Taxi vs. carro propio. |
| **Contenedor (Docker)** | Empaqueta tu app con todo lo que necesita para correr igual en cualquier lado. | Contenedor de barco: mismo tamaño en cualquier puerto. |
| **Región / zona** | Dónde están físicamente los servidores. | Afecta velocidad y leyes de datos. |
| **Escalar** | Aguantar más usuarios: servidor más grande (vertical) o más servidores (horizontal). | Cocina más grande vs. más cocinas. |
| **Balanceador de carga** | Reparte usuarios entre varios servidores. | La persona que asigna mesas. |

**Los niveles de "nube" de más fácil a más difícil**
1. **Plataformas simples**: Vercel, Netlify, Railway, Supabase. Subes y funciona.
2. **Servicios administrados**: bases de datos, colas, almacenamiento.
3. **Nubes grandes**: AWS, Google Cloud, Azure. Todo configurable y todo es responsabilidad tuya.

**AWS: los 8 servicios que debes reconocer**

| Servicio | Qué es |
| :-- | :-- |
| **EC2** | Servidores virtuales. |
| **S3** | Almacenamiento de archivos. |
| **RDS** | Bases de datos administradas. |
| **Lambda** | Funciones serverless. |
| **IAM** | Quién puede hacer qué (permisos). El más importante para seguridad. |
| **CloudWatch** | Logs y monitoreo. |
| **VPC** | Tu red privada dentro de AWS. |
| **Bedrock** | Acceso a modelos de IA (incluido Claude) dentro de AWS. |

**Otros temas de nube**
- **Infraestructura como código** (Terraform): describir servidores en un archivo, no a mano.
- **CI/CD** (GitHub Actions): tests y despliegue automáticos.
- **Facturación y alertas de costo**: el error de principiante más caro.
- Redes: DNS, dominios, HTTPS/certificados, puertos.

### C5. El viaje de un cambio: de la idea a producción

Este es el flujo que atraviesa TODO desarrollo profesional. Cada palabra rara que escuchas vive en uno de estos pasos.

| # | Paso | Qué pasa | Analogía periodística |
| :-- | :-- | :-- | :-- |
| 1 | **Issue / ticket** | Se escribe el problema o la tarea. | La orden de trabajo del editor. |
| 2 | **Repositorio (repo)** | La carpeta del proyecto con todo su historial (en GitHub). | El archivo del periódico. |
| 3 | **Branch (rama)** | Una copia paralela donde haces cambios sin tocar la versión oficial. | Un borrador aparte de la edición publicada. |
| 4 | **Commit** | Un "guardado" con descripción de qué cambiaste. | Cada versión guardada del borrador con nota. |
| 5 | **Push** | Subir tus commits a GitHub. | Enviar el borrador al sistema del periódico. |
| 6 | **PR (Pull Request)** | Pedir que tus cambios se unan a la versión oficial. Muestra el **diff**. | Entregar la nota al editor para revisión. |
| 7 | **Diff** | Qué líneas se agregaron (verde) y cuáles se quitaron (rojo). | El control de cambios de Word. |
| 8 | **Code review** | Otra persona (o IA) revisa el PR y comenta. | La corrección del editor. |
| 9 | **CI** (integración continua) | Robots corren tests automáticos sobre el PR. | El corrector de estilo y el verificador de datos. |
| 10 | **Merge** | Se acepta el PR y se une a la rama principal (`main`). | La nota pasa a la edición oficial. |
| 11 | **Deploy** | La versión nueva sale a internet. | Imprenta / publicación. |
| 12 | **Monitoreo** | Vigilar errores después de publicar. | Revisar reacciones y fe de erratas. |
| 13 | **Rollback / revert** | Volver a la versión anterior si algo se rompió. | Despublicar la nota. |

**Cuando Claude Code o Cursor trabajan, recorren estos mismos pasos.** Si sabes en qué paso está, sabes qué revisar.

### C6. Señales de que la IA la está cagando

Checklist para revisar lo que hace un agente de código.

**Al leer lo que dice**
- Dice "listo" o "done" **sin mostrar que corrió los tests**.
- Dice "arreglé el bug" pero no explica **la causa**.
- Usa "debería funcionar" (no lo probó).
- Cambia de estrategia cada vez que algo falla (está adivinando).

**Al mirar el diff**
- Cambió **muchos más archivos** de los que pediste.
- **Borró o desactivó tests** para que "pasen".
- Agregó `try/catch` que **silencia errores** en vez de arreglarlos.
- Puso **claves o contraseñas** directamente en el código.
- Instaló **librerías nuevas** sin que lo pidieras (riesgo de paquetes inventados).
- Duplicó código que ya existía en otro archivo.
- Dejó `TODO`, `console.log` o datos falsos ("mock") en código de producción.

**En la base de datos y la seguridad**
- Consultas que no filtran por usuario (un usuario podría ver datos de otro).
- Desactivó permisos (RLS) "para que funcione".
- Migraciones que **borran columnas o tablas**.

**En el comportamiento**
- Funciona en tu computador pero no en producción (variables de entorno, rutas).
- Funciona con un usuario pero no con dos al mismo tiempo.
- Solo probaste el camino feliz: ¿qué pasa si el pago falla, si no hay internet, si el campo viene vacío?

### C7. Glosario vivo

El tutor debe mantener un glosario que crece contigo: cada palabra nueva entra con **definición en una frase + analogía + dónde aparece en el viaje de un cambio (C5)**. Ejemplos iniciales: API, endpoint, JSON, framework, librería, dependencia, variable de entorno, token, prompt, embedding, deploy, PR, merge, CI/CD, staging, webhook, schema, migración, ORM, SDK, runtime.

---

## D. Mapa general (cómo encaja todo)

La malla tiene 6 capas que atraviesan desarrollo, IA y producto:

1. **Cómo funciona la máquina**: programación, computación, internet, nube.
2. **Cómo se construye software**: el viaje de un cambio (C5), metodologías, testing, seguridad.
3. **Qué tipos de productos existen**: web, SaaS, e-commerce, marketplace, pagos.
4. **Cómo funciona la IA**: modelos, tokens, contexto, entrenamiento, riesgos.
5. **Cómo se construye con IA**: agentes, patrones, RAG, grafos, frameworks, evals.
6. **Cómo se dirige la IA en una organización**: Chief AI Officer, gobernanza, negocio.

Transversal a todo: **saber revisar a la IA** (C6) y el **glosario vivo** (C7).
