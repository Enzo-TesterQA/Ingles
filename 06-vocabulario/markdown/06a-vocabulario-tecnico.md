# Vocabulario técnico QA & AI

Oct 13, 2026 · @Enzo

El vocabulario que más vas a usar en entrevistas y en el día a día, agrupado por tema, con un ejemplo de uso real. Método recomendado: 10 palabras por semana, escribiendo una oración propia con cada una.

## 1. Testing y calidad

| Término | Significado | Ejemplo |
| --- | --- | --- |
| test case | caso de prueba | I wrote 30 test cases for the new checkout flow. |
| test suite | conjunto de pruebas | The regression suite has around 400 tests. |
| test plan / test strategy | plan / estrategia de pruebas | I shared the test plan with the team before the sprint started. |
| coverage | cobertura | We increased API test coverage to 80%. |
| edge case | caso límite | Empty carts are an edge case we often forget. |
| corner case | caso extremo (varias condiciones límite juntas) | That bug only happens in a corner case with two discounts and a refund. |
| happy path | flujo ideal sin errores | The happy path works, but the error messages are wrong. |
| negative testing | pruebas con datos inválidos | Negative testing showed the API accepted negative quantities. |
| exploratory testing | pruebas exploratorias | I found the issue during an exploratory testing session. |
| acceptance criteria | criterios de aceptación | The story isn't ready because it has no acceptance criteria. |
| expected / actual result | resultado esperado / obtenido | Expected result: an error message. Actual result: a blank page. |
| sign-off | aprobación final | QA sign-off is required before every release. |
| go / no-go | decisión de lanzar o no | I gave a no-go because of an open blocker. |
| shift-left | probar más temprano en el ciclo | We're shifting left by reviewing stories before development. |
| test environment / staging | entorno de pruebas | The bug only reproduces on staging. |
| load / stress testing | pruebas de carga / estrés | We ran load tests with k6 before Black Friday. |
| usability | usabilidad | Automation can't evaluate usability. |
| accessibility (a11y) | accesibilidad | We added accessibility checks to the pipeline. |
| reliability | confiabilidad | Flaky tests hurt the reliability of the suite. |

## 2. Automatización, código y CI/CD

| Término | Significado | Ejemplo |
| --- | --- | --- |
| framework | estructura base de automatización | I built the framework with Playwright and TypeScript. |
| locator / selector | localizador de un elemento | Use data-testid locators instead of CSS classes. |
| assertion | verificación en un test | The test failed on the second assertion. |
| fixture | datos o estado preparado para un test | Each test gets a fresh user from a fixture. |
| mock / stub | simulación de un servicio | We mocked the payment provider to test errors. |
| flaky test | test inestable (a veces pasa, a veces falla) | That flaky test failed three times this week. |
| wait (implicit / explicit) | espera | Replace the hard-coded wait with an explicit wait. |
| headless | sin interfaz gráfica | Tests run headless in CI. |
| pipeline | flujo automatizado de build y deploy | The pipeline takes 12 minutes. |
| build | compilación / versión generada | The build is broken since the last merge. |
| deploy / deployment | despliegue | We deploy to production twice a week. |
| rollback / roll back | volver a la versión anterior | We had to roll back the release. |
| hotfix | arreglo urgente en producción | The hotfix went out the same afternoon. |
| merge | integrar cambios | Don't merge until the checks are green. |
| pull request (PR) / merge request | pedido de integración de código | I left two comments on your PR. |
| branch | rama | I created a branch for the new tests. |
| green / red | pasando / fallando | The pipeline is green again. |
| nightly run | ejecución nocturna | The nightly run caught a regression. |
| parallel execution | ejecución en paralelo | Parallel execution cut the time in half. |
| artifact | archivo generado por el pipeline (reportes, binarios) | Download the test report from the job artifacts. |
| environment variable | variable de entorno | The deploy failed because of a missing environment variable. |
| refactor | reestructurar código sin cambiar comportamiento | I refactored the page objects to remove duplication. |
| maintainability | facilidad de mantenimiento | The Page Object Model improves maintainability. |

## 3. APIs, backend y bugs

| Término | Significado | Ejemplo |
| --- | --- | --- |
| endpoint | URL de un recurso de la API | The /orders endpoint returns a 500 error. |
| request / response | pedido / respuesta | The response body is missing the total field. |
| payload | contenido que se envía | The payload is too large for the endpoint. |
| status code | código de estado HTTP | It should return 404, not 200. |
| header | encabezado | The auth token goes in the Authorization header. |
| authentication / authorization | quién sos / qué podés hacer | A normal user passed the authorization check for admin routes. |
| schema / contract | estructura acordada de datos | The new version broke the contract with the mobile app. |
| latency / response time | demora / tiempo de respuesta | Latency went up to 2 seconds after the deploy. |
| timeout | tiempo de espera agotado | The test failed with a timeout. |
| bug / defect / issue | error | I logged the issue in Jira. |
| blocker | error que bloquea el release o el trabajo | That bug is a blocker for the release. |
| severity / priority | gravedad / prioridad | High severity, but low priority because few users are affected. |
| root cause | causa raíz | The root cause was a race condition. |
| race condition | error por concurrencia | Two requests at the same time caused a race condition. |
| regression | algo que funcionaba y se rompió | This is a regression from last week's release. |
| workaround | solución provisoria | There's a workaround: refresh the page. |
| to reproduce (repro) | reproducir | I can't reproduce it on Chrome. |
| intermittent | intermitente | It's an intermittent issue, it fails 1 in 10 times. |
| log / logs | registros | I attached the logs to the ticket. |
| stack trace | traza del error | The stack trace points to the payment service. |
| triage | clasificar y priorizar bugs | We triage new bugs every Monday. |
| outage / incident | caída / incidente | There was a 20-minute outage last night. |
| post-mortem | análisis después de un incidente | We wrote a post-mortem with action items. |

## 4. IA y LLMs

| Término | Significado | Ejemplo |
| --- | --- | --- |
| LLM (large language model) | modelo de lenguaje grande | We use an LLM to summarize bug reports. |
| prompt | instrucción que se le da al modelo | A small change in the prompt changed the output a lot. |
| system prompt | instrucciones fijas del sistema | The system prompt tells the agent which tools it can use. |
| token | unidad de texto que procesa el modelo | Long documents use a lot of tokens. |
| context window | cantidad de texto que el modelo puede leer a la vez | The whole log didn't fit in the context window. |
| temperature | grado de aleatoriedad de la respuesta | We set the temperature to 0 for tests. |
| hallucination | respuesta inventada | The model hallucinated an API endpoint that doesn't exist. |
| grounding | basar la respuesta en fuentes | Grounding the answers in our docs reduced hallucinations. |
| RAG (retrieval-augmented generation) | generación con documentos recuperados | Our support bot uses RAG over the help center. |
| embedding | representación numérica del significado | We generate embeddings for every document. |
| vector database / vector store | base de datos de embeddings | The vector store returns the five closest chunks. |
| chunk / chunking | fragmento / dividir documentos | Smaller chunks improved retrieval. |
| agent | sistema que decide pasos y usa herramientas | The agent opens a ticket when a test fails. |
| tool calling / function calling | que el modelo llame funciones | Tool calling lets the agent query the database. |
| orchestration / orchestrator | coordinación de varios agentes o pasos | The orchestrator splits the task between three agents. |
| MCP (Model Context Protocol) | protocolo para conectar modelos con herramientas | We exposed our test runner as an MCP server. |
| eval / evaluation | evaluación de calidad del modelo | Every prompt change has to pass the evals. |
| LLM-as-a-judge | usar un modelo para calificar respuestas | We use an LLM as a judge to score relevance. |
| ground truth | respuesta de referencia correcta | We built a ground truth dataset of 200 questions. |
| guardrails | límites y controles de seguridad | Guardrails block answers with personal data. |
| prompt injection | instrucciones maliciosas en la entrada | The agent followed a prompt injection hidden in a web page. |
| fine-tuning | reentrenar un modelo con datos propios | We didn't need fine-tuning, RAG was enough. |
| latency / throughput | demora / cantidad de pedidos por segundo | Streaming improved perceived latency. |
| non-deterministic | no determinístico (no siempre da lo mismo) | LLM outputs are non-deterministic, so we test properties. |

## 5. Agile, reuniones y colaboración

| Término | Significado | Ejemplo |
| --- | --- | --- |
| sprint | iteración de trabajo | We work in two-week sprints. |
| backlog | lista de trabajo pendiente | The bug went back to the backlog. |
| user story | historia de usuario | Each user story has acceptance criteria. |
| stand-up / daily | reunión diaria | I mentioned the blocker in the stand-up. |
| refinement / grooming | refinamiento de historias | During refinement, I ask about edge cases. |
| retro (retrospective) | retrospectiva | In the retro, we agreed to write tests earlier. |
| estimate / story points | estimación / puntos | I estimated the testing effort at three points. |
| stakeholder | persona interesada o afectada | We presented the results to the stakeholders. |
| deadline | fecha límite | The deadline is next Friday. |
| scope | alcance | Mobile is out of scope for this release. |
| handover / hand off | traspaso de trabajo | I'll hand off the tests to the new QA next week. |
| ownership / to own | responsabilidad / hacerse cargo | I own the end-to-end suite. |
| to follow up | hacer seguimiento | I'll follow up with the dev team tomorrow. |
| to escalate | escalar un problema | If it's not fixed today, I'll escalate it to the lead. |
| to sync / a quick sync | coordinar / reunión corta | Can we have a quick sync after lunch? |
| to be on the same page | estar alineados | Let's make sure we're on the same page about the scope. |
| action items | tareas que salen de una reunión | I'll send the action items after the meeting. |
| bandwidth | capacidad / tiempo disponible | I don't have the bandwidth to test both features this sprint. |
| trade-off | compromiso entre dos opciones | It's a trade-off between speed and coverage. |
| to push back | oponerse con argumentos | I pushed back on releasing without regression tests. |
| heads-up | aviso previo | Just a heads-up: staging will be down at 3 pm. |
| ETA | tiempo estimado de llegada / entrega | What's the ETA for the fix? |

## 6. Falsos amigos

Palabras que se parecen al español pero significan otra cosa. Las de esta tabla aparecen seguido en conversaciones de trabajo.

| Palabra en inglés | Significa | No significa | Para decir eso, usá |
| --- | --- | --- | --- |
| actually | en realidad | actualmente | currently, right now |
| eventually | finalmente, con el tiempo | eventualmente (quizás) | possibly, at some point |
| realize | darse cuenta | realizar | do, carry out, run (tests) |
| assist | ayudar | asistir (ir) | attend (a meeting) |
| attend | asistir, ir a | atender | serve, deal with, take care of |
| career | carrera profesional | carrera universitaria | degree, studies |
| support | apoyar, dar soporte | soportar (aguantar) | stand, put up with |
| sensible | sensato | sensible | sensitive (sensitive data) |
| library | biblioteca (también de código) | librería (negocio) | bookstore |
| exit | salida | éxito | success |
| succeed | tener éxito | suceder | happen |
| compromise | acuerdo / concesión; también comprometer la seguridad | compromiso (obligación) | commitment |
| discussion | conversación, debate | discusión (pelea) | argument |
| argument | discusión fuerte o argumento | solo argumento | point, reason (para argumento) |
| demand | exigir | demandar (judicialmente) | sue |
| lecture | clase magistral, charla | lectura | reading |
| advice | consejo | aviso | warning, notice, heads-up |
| resume / résumé | retomar / CV | resumir | summarize, sum up |
| particular | específico | privado / particular de una persona | private, personal |
| topic | tema | tópico (lugar común) | cliché |
| embarrassed | avergonzado | embarazada | pregnant |
| constipated | estreñido | resfriado | have a cold |
| quite | bastante | quitar | remove |
| deception | engaño | decepción | disappointment |
| pretend | fingir | pretender (aspirar) | intend, aim, expect |
| application | aplicación / postulación a un trabajo | solo app | (contexto) I sent my application. |

## 7. Errores típicos de hispanohablantes

Más allá de los tiempos verbales, estos son los errores que más se notan en una entrevista.

| Error | Correcto | Regla |
| --- | --- | --- |
| Is very important to test early. | **It** is very important to test early. | En inglés el sujeto nunca se omite. |
| The people is happy with the release. | The people **are** happy. | People es plural. |
| I received many feedbacks / informations / advices. | I received a lot of **feedback / information / advice**. | Incontables: sin plural y sin "a". |
| I have experience in testing of APIs. | I have experience **in API testing**. | El sustantivo que describe va adelante. |
| The automation is important for the companies. | Automation is important for companies. | Hablando en general, sin "the". |
| I'm working in Globant. | I work **at** Globant. | At + empresa. In + ciudad / equipo / área. |
| The meeting is in Monday at the 10. | The meeting is **on** Monday **at** 10. | On + día, at + hora, in + mes / año. |
| Make a test / make a deploy. | **Run** a test / **do** a deploy / **deploy**. | Collocations: run tests, do a review, make a decision. |
| He said me that it was fixed. | He **told me** / He **said** that it was fixed. | Tell + persona; say sin persona. |
| Where is the log? I can't find. | I can't find **it**. | Los verbos transitivos necesitan objeto. |
| More easy / more fast. | **Easier / faster**. | Adjetivos cortos: -er. |
| What means "flaky"? | What **does** "flaky" **mean**? | Preguntas con do / does. |
| Can you tell me where is the report? | Can you tell me where **the report is**? | En preguntas indirectas no se invierte. |
| I didn't see nothing. | I didn't see **anything**. | No hay doble negación. |
| I like very much testing. | I **really like** testing. / I like testing a lot. | Very much no va entre el verbo y el objeto. |
| If I would have time, I would automate it. | If I **had** time, I would automate it. | Después de if, nunca would. |
| I'm boring in long meetings. | I'm **bored** in long meetings. | -ed = cómo te sentís; -ing = cómo es algo. |
| Two years ago I work at X. | Two years ago I **worked** at X. | Ago siempre con Past Simple. |
| I know him since 2020. | I've **known** him since 2020. | Since con algo que sigue: Present Perfect. |
| One of the best tester. | One of the best **testers**. | One of the + plural. |

**Qué hacer con esta tabla:** marcá los 5 errores que reconocés en vos y anotalos en el registro de errores. Esos son tu foco del mes.
