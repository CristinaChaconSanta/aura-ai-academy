# Malla canónica — Aura AI Academy

Única fuente de verdad del orden de estudio. Reemplaza las 4 versiones del documento de Perplexity.

**Formato de ID:** `N<nivel>-M<módulo>-L<lección>` (ej. `N1-M2-L03`).
**Estados:** ⬜ pendiente · 📝 borrador · 🔎 verificada · ✅ aprobada (solo la aprendiz marca ✅).
**Regla:** una lección = un concepto = 15–32 minutos.
**Talleres:** cada módulo cierra con un taller `N<k>-M<m>-T` (ver `talleres/README.md`). 🛠️ = práctica con tus manos.

## Mapa de niveles

| Nivel | Capa | Pregunta que responde | Proyecto ancla (evidencia para aprobar) |
| :-- | :-- | :-- | :-- |
| N1 | Cómo funciona la máquina | ¿Qué pasa realmente cuando uso un computador e internet? | Landing page estática publicada + explicación oral de URL → página. |
| N2 | Cómo se construye software | ¿Cómo trabaja un equipo (o un agente) para cambiar código sin romperlo? | Un PR propio con tests, revisado con la checklist de C6. |
| N3 | Productos web | ¿Qué piezas tiene cada tipo de producto? | SaaS con login donde el usuario A no puede ver datos de B. |
| N4 | Pagos, operación y nube | ¿Cómo se cobra, se publica y se mantiene vivo? | Tienda en modo prueba con webhook firmado e idempotente, desplegada y monitoreada. |
| N5 | Cómo funciona la IA | ¿Qué es realmente un modelo y por qué falla? | Ensayo de 800 palabras: "por qué alucina un LLM", verificado por el tutor. |
| N6 | Construir con IA | ¿Cómo se diseña un agente que funcione en producción? | Agente con RAG, herramientas, evals, logs y límites de costo; pasa una prueba de prompt injection. |
| N7 | Chief AI Officer | ¿Cómo se dirige la IA en una organización? | Documento de estrategia de IA para una empresa real. |

Transversales (aparecen en todos los niveles): **revisar a la IA** (sección 9 de cada lección) y **glosario vivo** (`aprendizaje/glosario.md`).

---

## N1 — Cómo funciona la máquina

### N1-M1 · Internet
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N1-M1-L01 | Las partes de una URL | 🔎 |
| N1-M1-L02 | Parámetros y anclas: el final de una URL | 🔎 |
| N1-M1-L03 | El viaje de una URL | 🔎 |
| N1-M1-L04 | Cliente y servidor | ⬜ |
| N1-M1-L05 | HTTP: peticiones, respuestas y códigos (200, 404, 500) | ⬜ |
| N1-M1-L06 | DNS y dominios | ⬜ |
| N1-M1-L07 | HTTPS y certificados | ⬜ |
| N1-M1-L08 | APIs y endpoints | ⬜ |
| N1-M1-L09 | JSON: el idioma de las APIs | ⬜ |
| N1-M1-T | 🛠️ Taller del módulo | 🔎 |

### N1-M2 · El computador por dentro
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N1-M2-L01 | CPU, memoria y disco | ⬜ |
| N1-M2-L02 | Archivos, carpetas y rutas | ⬜ |
| N1-M2-L03 | Procesos y puertos (qué es `localhost:3000`) | ⬜ |
| N1-M2-L04 | La terminal: por qué existe y los 10 comandos básicos | ⬜ |
| N1-M2-L05 | Variables de entorno y secretos | ⬜ |
| N1-M2-T | 🛠️ Taller del módulo | ⬜ |

### N1-M3 · Pensar como programa
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N1-M3-L01 | Algoritmo: una receta sin ambigüedades | ⬜ |
| N1-M3-L02 | Variables y tipos de datos | ⬜ |
| N1-M3-L03 | Condicionales | ⬜ |
| N1-M3-L04 | Bucles | ⬜ |
| N1-M3-L05 | Funciones: entrada, proceso, salida | ⬜ |
| N1-M3-L06 | Listas y diccionarios | ⬜ |
| N1-M3-L07 | Errores, excepciones y cómo leer un stack trace | ⬜ |
| N1-M3-L08 | Descomponer un problema antes de pedírselo a la IA | ⬜ |
| N1-M3-T | 🛠️ Taller del módulo | ⬜ |

### N1-M4 · Lenguajes y paradigmas
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N1-M4-L01 | Mapa de lenguajes: cuál sirve para qué | ⬜ |
| N1-M4-L02 | Tipado dinámico vs. estático (JavaScript vs. TypeScript) | ⬜ |
| N1-M4-L03 | Interpretado vs. compilado | ⬜ |
| N1-M4-L04 | Paradigma imperativo vs. declarativo | ⬜ |
| N1-M4-L05 | Programación orientada a objetos | ⬜ |
| N1-M4-L06 | Programación funcional | ⬜ |
| N1-M4-L07 | Programación orientada a eventos | ⬜ |
| N1-M4-L08 | Librería, framework, SDK y dependencia | ⬜ |
| N1-M4-T | 🛠️ Taller del módulo | ⬜ |

### N1-M5 · Estructuras de datos por intuición
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N1-M5-L01 | Cola y pila | ⬜ |
| N1-M5-L02 | Árboles | ⬜ |
| N1-M5-L03 | Grafos: la estructura de datos | ⬜ |
| N1-M5-L04 | Big-O por intuición: por qué algo es lento con 10.000 usuarios | ⬜ |
| N1-M5-T | 🛠️ Taller del módulo | ⬜ |

### N1-M6 · La web en el navegador
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N1-M6-L01 | HTML: estructura y semántica | ⬜ |
| N1-M6-L02 | CSS: estilo, Flexbox y Grid | ⬜ |
| N1-M6-L03 | JavaScript en el navegador y el DOM | ⬜ |
| N1-M6-L04 | Cómo el navegador convierte código en píxeles | ⬜ |
| N1-M6-L05 | Asincronía y el event loop | ⬜ |
| N1-M6-T | 🛠️ Taller del módulo | ⬜ |

---

## N2 — Cómo se construye software

### N2-M1 · El viaje de un cambio
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N2-M1-L01 | Git: commits como versiones guardadas | ⬜ |
| N2-M1-L02 | Ramas (branches) | ⬜ |
| N2-M1-L03 | GitHub: repositorio remoto, push y pull | ⬜ |
| N2-M1-L04 | Pull Request y diff | ⬜ |
| N2-M1-L05 | Code review | ⬜ |
| N2-M1-L06 | Merge y conflictos | ⬜ |
| N2-M1-L07 | CI/CD: robots que prueban y publican | ⬜ |
| N2-M1-L08 | Entornos: desarrollo, staging, producción | ⬜ |
| N2-M1-T | 🛠️ Taller del módulo | ⬜ |

### N2-M2 · Calidad
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N2-M2-L01 | Qué prueba un buen test | ⬜ |
| N2-M2-L02 | Tests unitarios, de integración y end-to-end | ⬜ |
| N2-M2-L03 | TDD: el test como contrato para la IA | ⬜ |
| N2-M2-L04 | Debugging: método científico para errores | ⬜ |
| N2-M2-L05 | Leer código que no escribiste | ⬜ |
| N2-M2-L06 | Señales de que la IA la está cagando | ⬜ |
| N2-M2-T | 🛠️ Taller del módulo | ⬜ |

### N2-M3 · Metodologías
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N2-M3-L01 | Agile y Scrum | ⬜ |
| N2-M3-L02 | Kanban | ⬜ |
| N2-M3-L03 | Shape Up | ⬜ |
| N2-M3-L04 | BDD: tests escritos como frases | ⬜ |
| N2-M3-L05 | DDD: el código habla el idioma del negocio | ⬜ |
| N2-M3-L06 | Spec-driven development con agentes | ⬜ |
| N2-M3-L07 | Métricas DORA | ⬜ |
| N2-M3-T | 🛠️ Taller del módulo | ⬜ |

### N2-M4 · Producto antes que código
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N2-M4-L01 | Problema, usuario y resultado medible | ⬜ |
| N2-M4-L02 | Historias de usuario y criterios de aceptación | ⬜ |
| N2-M4-L03 | PRD: el documento de requisitos | ⬜ |
| N2-M4-L04 | Alcance: qué NO va en la versión 1 | ⬜ |
| N2-M4-T | 🛠️ Taller del módulo | ⬜ |

### N2-M5 · Arquitectura de software
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N2-M5-L01 | Qué es arquitectura y por qué importa | ⬜ |
| N2-M5-L02 | Separación de responsabilidades y capas | ⬜ |
| N2-M5-L03 | Monolito vs. microservicios | ⬜ |
| N2-M5-L04 | Diseño de APIs (REST) | ⬜ |
| N2-M5-T | 🛠️ Taller del módulo | ⬜ |

---

## N3 — Productos web

### N3-M1 · Tipos de producto
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N3-M1-L01 | Sitio estático vs. dinámico | ⬜ |
| N3-M1-L02 | CMS: el tablero de anuncios | ⬜ |
| N3-M1-L03 | E-commerce | ⬜ |
| N3-M1-L04 | SaaS y aplicaciones con login | ⬜ |
| N3-M1-L05 | Marketplace: por qué es más difícil que una tienda | ⬜ |
| N3-M1-L06 | Dashboards y portales internos | ⬜ |
| N3-M1-T | 🛠️ Taller del módulo | ⬜ |

### N3-M2 · Frontend
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N3-M2-L01 | Componentes y React | ⬜ |
| N3-M2-L02 | Estado: la memoria de la interfaz | ⬜ |
| N3-M2-L03 | Renderizado: SSG, SSR, CSR e ISR | ⬜ |
| N3-M2-L04 | Next.js: qué resuelve un framework web | ⬜ |
| N3-M2-L05 | Accesibilidad (WCAG) | ⬜ |
| N3-M2-L06 | Rendimiento y Core Web Vitals | ⬜ |
| N3-M2-L07 | SEO técnico | ⬜ |
| N3-M2-T | 🛠️ Taller del módulo | ⬜ |

### N3-M3 · Backend y datos
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N3-M3-L01 | Qué hace un backend | ⬜ |
| N3-M3-L02 | Bases de datos relacionales y SQL | ⬜ |
| N3-M3-L03 | Modelado de datos: tablas y relaciones | ⬜ |
| N3-M3-L04 | Migraciones | ⬜ |
| N3-M3-L05 | ORM vs. SQL directo | ⬜ |
| N3-M3-L06 | Bases de datos no relacionales | ⬜ |
| N3-M3-L07 | Supabase: backend como servicio | ⬜ |
| N3-M3-L08 | Trabajos en segundo plano, colas y cron | ⬜ |
| N3-M3-L09 | Subida y almacenamiento de archivos | ⬜ |
| N3-M3-L10 | Correo transaccional (SPF, DKIM, DMARC) | ⬜ |
| N3-M3-L11 | Concurrencia: dos personas compran el último producto | ⬜ |
| N3-M3-T | 🛠️ Taller del módulo | ⬜ |

### N3-M4 · Usuarios y permisos
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N3-M4-L01 | Autenticación vs. autorización | ⬜ |
| N3-M4-L02 | Contraseñas, hashing y MFA | ⬜ |
| N3-M4-L03 | Sesiones, cookies y JWT | ⬜ |
| N3-M4-L04 | OAuth: entrar con Google | ⬜ |
| N3-M4-L05 | Roles y permisos (RBAC) | ⬜ |
| N3-M4-L06 | Row Level Security | ⬜ |
| N3-M4-L07 | Multi-tenancy | ⬜ |
| N3-M4-T | 🛠️ Taller del módulo | ⬜ |

---

## N4 — Pagos, operación y nube

### N4-M1 · Pagos
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N4-M1-L01 | Cómo viaja un pago (y por qué nunca tocas la tarjeta) | ⬜ |
| N4-M1-L02 | PCI-DSS sin miedo | ⬜ |
| N4-M1-L03 | Webhooks y verificación de firma | ⬜ |
| N4-M1-L04 | Idempotencia | ⬜ |
| N4-M1-L05 | Estados del pago, reembolsos y contracargos | ⬜ |
| N4-M1-L06 | Suscripciones | ⬜ |
| N4-M1-L07 | Pagos divididos en marketplaces | ⬜ |
| N4-M1-L08 | Contexto Colombia: pasarelas, PSE, DIAN y Ley 1581 | ⬜ |
| N4-M1-T | 🛠️ Taller del módulo | ⬜ |

### N4-M2 · Seguridad web
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N4-M2-L01 | Mentalidad de atacante | ⬜ |
| N4-M2-L02 | OWASP Top 10 | ⬜ |
| N4-M2-L03 | Inyección SQL | ⬜ |
| N4-M2-L04 | XSS | ⬜ |
| N4-M2-L05 | IDOR: el fallo favorito del código generado por IA | ⬜ |
| N4-M2-L06 | CORS y CSRF | ⬜ |
| N4-M2-L07 | Rate limiting | ⬜ |
| N4-M2-L08 | Cadena de suministro y dependencias | ⬜ |
| N4-M2-T | 🛠️ Taller del módulo | ⬜ |

### N4-M3 · Nube
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N4-M3-L01 | Qué es un servidor y qué es la nube | ⬜ |
| N4-M3-L02 | IaaS, PaaS y SaaS | ⬜ |
| N4-M3-L03 | Serverless | ⬜ |
| N4-M3-L04 | Contenedores y Docker | ⬜ |
| N4-M3-L05 | Escalar: vertical, horizontal y balanceadores | ⬜ |
| N4-M3-L06 | De Vercel a AWS: niveles de nube | ⬜ |
| N4-M3-L07 | AWS: los 8 servicios que debes reconocer | ⬜ |
| N4-M3-L08 | IAM y mínimo privilegio | ⬜ |
| N4-M3-L09 | Infraestructura como código | ⬜ |
| N4-M3-L10 | Costos de nube y alertas de facturación | ⬜ |
| N4-M3-T | 🛠️ Taller del módulo | ⬜ |

### N4-M4 · Operación
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N4-M4-L01 | Logs, métricas y trazas | ⬜ |
| N4-M4-L02 | Alertas y baseline | ⬜ |
| N4-M4-L03 | Feature flags y despliegue gradual | ⬜ |
| N4-M4-L04 | Rollback | ⬜ |
| N4-M4-L05 | Backups y restauración | ⬜ |
| N4-M4-L06 | Incidentes y postmortems | ⬜ |
| N4-M4-L07 | Caché y CDN | ⬜ |
| N4-M4-T | 🛠️ Taller del módulo | ⬜ |

---

## N5 — Cómo funciona la IA

### N5-M1 · El modelo por dentro
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N5-M1-L01 | IA, machine learning, deep learning y LLM | ⬜ |
| N5-M1-L02 | Redes neuronales por intuición | ⬜ |
| N5-M1-L03 | Tokens | ⬜ |
| N5-M1-L04 | Predicción del siguiente token | ⬜ |
| N5-M1-L05 | Embeddings: significado como coordenadas | ⬜ |
| N5-M1-L06 | Transformer y atención | ⬜ |
| N5-M1-L07 | Ventana de contexto y context rot | ⬜ |
| N5-M1-L08 | Temperatura y muestreo | ⬜ |
| N5-M1-T | 🛠️ Taller del módulo | ⬜ |

### N5-M2 · Cómo se entrena
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N5-M2-L01 | Preentrenamiento | ⬜ |
| N5-M2-L02 | Ajuste con instrucciones (SFT) | ⬜ |
| N5-M2-L03 | RLHF, RLAIF y Constitutional AI | ⬜ |
| N5-M2-L04 | Entrenamiento vs. inferencia | ⬜ |
| N5-M2-L05 | Modelos de razonamiento | ⬜ |
| N5-M2-T | 🛠️ Taller del módulo | ⬜ |

### N5-M3 · El ecosistema de modelos
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N5-M3-L01 | Modelos grandes vs. pequeños | ⬜ |
| N5-M3-L02 | Multimodales | ⬜ |
| N5-M3-L03 | Modelos abiertos vs. cerrados | ⬜ |
| N5-M3-L04 | Por qué los benchmarks engañan | ⬜ |
| N5-M3-L05 | Costo y latencia: elegir modelo | ⬜ |
| N5-M3-T | 🛠️ Taller del módulo | ⬜ |

### N5-M4 · Límites y riesgos
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N5-M4-L01 | Por qué alucina un LLM | ⬜ |
| N5-M4-L02 | Sesgos | ⬜ |
| N5-M4-L03 | Privacidad y datos de entrenamiento | ⬜ |
| N5-M4-L04 | El cambio de paradigma: del SDLC al ciclo de vida de agentes | ⬜ |
| N5-M4-T | 🛠️ Taller del módulo | ⬜ |

---

## N6 — Construir con IA

### N6-M1 · Dirigir a la IA
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N6-M1-L01 | Prompt engineering vs. context engineering | ⬜ |
| N6-M1-L02 | System prompt y mensajes | ⬜ |
| N6-M1-L03 | Archivos de proyecto: CLAUDE.md, AGENTS.md y reglas | ⬜ |
| N6-M1-L04 | Skills, subagentes y hooks | ⬜ |
| N6-M1-L05 | Few-shot y salida estructurada | ⬜ |
| N6-M1-L06 | Prompting vs. RAG vs. fine-tuning | ⬜ |
| N6-M1-T | 🛠️ Taller del módulo | ⬜ |

### N6-M2 · Anatomía de un agente
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N6-M2-L01 | Chatbot vs. agente | ⬜ |
| N6-M2-L02 | Tool calling | ⬜ |
| N6-M2-L03 | El loop agéntico | ⬜ |
| N6-M2-L04 | MCP: el USB-C de la IA | ⬜ |
| N6-M2-L05 | Diseñar buenas herramientas | ⬜ |
| N6-M2-L06 | Memoria: corto, largo plazo, episódica y semántica | ⬜ |
| N6-M2-L07 | Límites de pasos y de costo | ⬜ |
| N6-M2-T | 🛠️ Taller del módulo | ⬜ |

### N6-M3 · Patrones
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N6-M3-L01 | Prompt chaining y routing | ⬜ |
| N6-M3-L02 | Paralelización | ⬜ |
| N6-M3-L03 | ReAct | ⬜ |
| N6-M3-L04 | Plan-and-Execute | ⬜ |
| N6-M3-L05 | Reflexion | ⬜ |
| N6-M3-L06 | Evaluator-Optimizer | ⬜ |
| N6-M3-L07 | Orchestrator-Workers | ⬜ |
| N6-M3-L08 | Combinar patrones y cuándo NO usar un agente | ⬜ |
| N6-M3-T | 🛠️ Taller del módulo | ⬜ |

### N6-M4 · Conocimiento
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N6-M4-L01 | RAG: el pipeline completo | ⬜ |
| N6-M4-L02 | Chunking | ⬜ |
| N6-M4-L03 | Bases de datos vectoriales | ⬜ |
| N6-M4-L04 | Re-ranking y búsqueda híbrida | ⬜ |
| N6-M4-L05 | Knowledge graphs | ⬜ |
| N6-M4-L06 | GraphRAG | ⬜ |
| N6-M4-L07 | Las tres caras de "grafo" | ⬜ |
| N6-M4-T | 🛠️ Taller del módulo | ⬜ |

### N6-M5 · Herramientas del AI Engineer
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N6-M5-L01 | Roles: AI Engineer, ML Engineer, Data Engineer | ⬜ |
| N6-M5-L02 | SDKs de proveedores | ⬜ |
| N6-M5-L03 | LangChain | ⬜ |
| N6-M5-L04 | LangGraph | ⬜ |
| N6-M5-L05 | Otros frameworks: LlamaIndex, CrewAI, Agent SDKs | ⬜ |
| N6-M5-L06 | No-code: n8n y Make como capa determinística | ⬜ |
| N6-M5-L07 | Modelos locales | ⬜ |
| N6-M5-T | 🛠️ Taller del módulo | ⬜ |

### N6-M6 · Calidad y producción
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N6-M6-L01 | Análisis de errores | ⬜ |
| N6-M6-L02 | Evals y dataset dorado | ⬜ |
| N6-M6-L03 | LLM-as-judge y sus trampas | ⬜ |
| N6-M6-L04 | Observabilidad de agentes | ⬜ |
| N6-M6-L05 | Versionar prompts | ⬜ |
| N6-M6-L06 | UX de productos con IA | ⬜ |
| N6-M6-L07 | Costos de tokens y caché de prompts | ⬜ |
| N6-M6-T | 🛠️ Taller del módulo | ⬜ |

### N6-M7 · Seguridad de IA
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N6-M7-L01 | OWASP Top 10 para LLMs | ⬜ |
| N6-M7-L02 | Prompt injection directa e indirecta | ⬜ |
| N6-M7-L03 | La trifecta letal | ⬜ |
| N6-M7-L04 | Agencia excesiva y humano en el loop | ⬜ |
| N6-M7-L05 | Slopsquatting y paquetes inventados | ⬜ |
| N6-M7-L06 | Riesgos de MCP servers | ⬜ |
| N6-M7-L07 | Sandboxing y guardrails | ⬜ |
| N6-M7-T | 🛠️ Taller del módulo | ⬜ |

---

## N7 — Chief AI Officer

### N7-M1 · Estrategia
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N7-M1-L01 | Qué hace un Chief AI Officer | ⬜ |
| N7-M1-L02 | Diagnóstico de madurez de IA | ⬜ |
| N7-M1-L03 | Portafolio de casos de uso: impacto vs. factibilidad | ⬜ |
| N7-M1-L04 | Business case y ROI | ⬜ |
| N7-M1-L05 | Build vs. buy | ⬜ |
| N7-M1-L06 | Datos como base: calidad y gobierno de datos | ⬜ |
| N7-M1-T | 🛠️ Taller del módulo | ⬜ |

### N7-M2 · Gobernanza y regulación
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N7-M2-L01 | EU AI Act y niveles de riesgo | ⬜ |
| N7-M2-L02 | NIST AI RMF | ⬜ |
| N7-M2-L03 | ISO/IEC 42001 | ⬜ |
| N7-M2-L04 | Marco de IA en Colombia | ⬜ |
| N7-M2-L05 | Inventario y registro de sistemas de IA | ⬜ |
| N7-M2-L06 | Propiedad intelectual y copyright | ⬜ |
| N7-M2-L07 | Gestión de proveedores de modelos | ⬜ |
| N7-M2-L08 | Incidentes de IA | ⬜ |
| N7-M2-T | 🛠️ Taller del módulo | ⬜ |

### N7-M3 · Personas y cambio
| ID | Lección | Estado |
| :-- | :-- | :-- |
| N7-M3-L01 | Shadow AI | ⬜ |
| N7-M3-L02 | Alfabetización en IA para equipos | ⬜ |
| N7-M3-L03 | Gestionar el miedo al reemplazo | ⬜ |
| N7-M3-L04 | Equipos híbridos: humanos + agentes | ⬜ |
| N7-M3-L05 | Medir adopción y valor | ⬜ |
| N7-M3-L06 | Presentar a la junta directiva | ⬜ |
| N7-M3-T | 🛠️ Taller del módulo | ⬜ |
