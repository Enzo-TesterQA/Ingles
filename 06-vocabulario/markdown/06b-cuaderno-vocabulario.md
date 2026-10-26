# Cuaderno de práctica: Vocabulario técnico

Oct 13, 2026 · @Enzo

Este cuaderno es el punto 6 del plan en versión práctica. El documento de vocabulario técnico tiene las palabras con su significado y un ejemplo; acá las usás, primero reconociéndolas y después en oraciones tuyas, que es como se te quedan.

## Cómo usar este cuaderno

1. **Un bloque por semana, el martes**, como dice el plan de estudio. Cada sección del documento de vocabulario tiene dos bloques: el A es para reconocer las palabras y el B para usarlas vos.
2. **Antes de cada bloque, leé la sección** del documento de vocabulario que le corresponde. Tapate la columna del significado y probá si te acordás. Entre bloques, repasá con [Vocab Deck](https://claude.ai/artifact/Cw1eJAWxrL7kqRX1u6AnPU): son tarjetas con todo el documento y te muestran más seguido las que te cuestan.
3. **Mandame las respuestas con el código**, por ejemplo *1A.3: coverage*. Te corrijo con tu frase, la versión correcta y la regla en una línea. Las soluciones no están en el cuaderno.
4. **Para avanzar necesitás 4 de 5 bien.** Si sacás menos, repasá la sección y repetí el bloque la semana siguiente.
5. **Anotá en tu banco de palabras** las que te costaron, con una oración tuya. Una palabra se queda cuando la usás hablando, no cuando la leés.

En los bloques B también se corrigen los tiempos verbales: muchas preguntas piden Past Simple o Present Perfect a propósito.

### Ruta semanal

| Semana | Sección del documento de vocabulario | Bloque |
| --- | --- | --- |
| 1 | 1. Testing y calidad | 1A |
| 2 | 1. Testing y calidad | 1B |
| 3 | 2. Automatización, código y CI/CD | 2A |
| 4 | 2. Automatización, código y CI/CD | 2B |
| 5 | 3. APIs, backend y bugs | 3A |
| 6 | 3. APIs, backend y bugs | 3B |
| 7 | 4. IA y LLMs | 4A |
| 8 | 4. IA y LLMs | 4B |
| 9 | 5. Agile, reuniones y colaboración | 5A |
| 10 | 5. Agile, reuniones y colaboración | 5B |
| 11 | 6. Falsos amigos | 6A |
| 12 | 6. Falsos amigos | 6B |
| 13 | 7. Errores típicos de hispanohablantes | 7A |
| 14 | 7. Errores típicos de hispanohablantes | 7B |
| 15 | Repaso de todo | Test final |

Si un tema te urge antes (por ejemplo, tenés una entrevista de IA la semana que viene), salteá al bloque que necesites: los bloques no dependen unos de otros.

## Bloque 1. Testing y calidad

### 1A. Completá con la palabra

Usá las palabras del recuadro. Sobran dos.

> **Palabras:** acceptance criteria / coverage / edge case / exploratory testing / happy path / sign-off / staging

1A.1. The story can't go into the sprint yet: nobody has written the \_\_\_\_\_\_.

1A.2. A user who tries to pay with an empty cart is an \_\_\_\_\_\_ we should test.

1A.3. Our unit test \_\_\_\_\_\_ is 85%, but the UI has almost no tests.

1A.4. The new version is on \_\_\_\_\_\_ now. Can you run the smoke tests there before we deploy to production?

1A.5. We tested the \_\_\_\_\_\_ first: valid user, valid card, payment accepted.

### 1B. Usalas vos

Respondé cada pregunta en inglés, en una o dos oraciones, usando la palabra entre paréntesis. Ojo con el tiempo verbal que pide la pregunta.

1B.1. What did you do when you saw that the sign-up form accepted an empty email? *(negative testing)*

1B.2. Why didn't the release go out last Friday? *(no-go)*

1B.3. How do you get involved earlier in the development process? *(shift-left)*

1B.4. Besides the steps, what do you always include in a bug report? *(expected result / actual result)*

1B.5. Why did you remove the hard-coded waits from the suite? *(reliability)*

## Bloque 2. Automatización, código y CI/CD

### 2A. Elegí la palabra correcta

2A.1. The test failed on the third \_\_\_\_\_\_: the total was 99.90 instead of 100. *(assertion / locator)*

2A.2. We \_\_\_\_\_\_ the payment provider, so we can test errors without using real money. *(mocked / merged)*

2A.3. The release broke the login, so we had to \_\_\_\_\_\_ to the previous version. *(roll back / refactor)*

2A.4. The tests run \_\_\_\_\_\_ in CI, so no browser window opens. *(headless / in parallel)*

2A.5. Please don't \_\_\_\_\_\_ your pull request until someone has reviewed it. *(merge / deploy)*

### 2B. Explicalo como en una entrevista

Respondé en inglés, en una o dos oraciones, como si te lo preguntara un entrevistador. No copies el ejemplo del documento: usá tu experiencia.

2B.1. What is a flaky test, and what usually causes it?

2B.2. Why would you use a mock instead of the real service in a test?

2B.3. What is a fixture?

2B.4. What can a nightly run catch that a pull request check can't?

2B.5. Why does the Page Object Model improve maintainability?

## Bloque 3. APIs, backend y bugs

### 3A. Completá con la palabra

Usá las palabras del recuadro. Sobran dos.

> **Palabras:** blocker / intermittent / regression / root cause / timeout / triage / workaround

3A.1. Search worked fine last week, and now it's broken. It's a \_\_\_\_\_\_.

3A.2. Until the fix is deployed, users have a \_\_\_\_\_\_: they can export the report as CSV instead of PDF.

3A.3. We can't release with that bug open. It's a \_\_\_\_\_\_.

3A.4. The bug only happens in 1 out of 20 runs, so it's \_\_\_\_\_\_.

3A.5. After two days of debugging, we found the \_\_\_\_\_\_: the cache wasn't cleared after the deploy.

### 3B. Severity, priority y títulos de bugs

Para 3B.1 a 3B.4, decí en inglés qué severity y qué priority le darías (high, medium o low) y por qué, en una oración. En 3B.5, escribí el título del bug.

3B.1. There's a typo on the *About us* page.

3B.2. Checkout fails for every user on Safari.

3B.3. The admin panel crashes when you upload a 2 GB file. Only two people in the company use that panel.

3B.4. The company logo on the home page is the old one, and there's a big marketing launch tomorrow.

3B.5. The /orders endpoint returns a 500 error when the quantity is 0. Escribí un título claro, de una línea.

## Bloque 4. IA y LLMs

### 4A. Uní cada término con su definición

Sobra una definición. Mandame las respuestas así: *4A.1: letra*.

| Término | Definición |
| --- | --- |
| 4A.1. hallucination | a) the correct reference answer you compare the model's output with |
| 4A.2. grounding | b) an answer the model invents and presents as a fact |
| 4A.3. context window | c) controls that block unsafe or unwanted outputs |
| 4A.4. guardrails | d) the amount of text the model can read at once |
| 4A.5. ground truth | e) basing the model's answers on trusted sources |
|  | f) how random the model's output is |

### 4B. Completá con la palabra

Usá las palabras del recuadro. Sobran dos.

> **Palabras:** chunks / embeddings / evals / fine-tuning / prompt injection / temperature / tool calling

4B.1. We set the \_\_\_\_\_\_ to 0 to make the outputs more consistent in our tests.

4B.2. A user hid the text *"ignore your previous instructions"* in a PDF, and the assistant obeyed it. That was a \_\_\_\_\_\_.

4B.3. We split the documentation into small \_\_\_\_\_\_ before we indexed it.

4B.4. Thanks to \_\_\_\_\_\_, the agent can check the status of an order in our database.

4B.5. Every time someone changes the prompt, the \_\_\_\_\_\_ run automatically to check that the quality didn't drop.

## Bloque 5. Agile, reuniones y colaboración

### 5A. Completá la conversación de Slack

Usá las palabras del recuadro. Sobran dos.

> **Palabras:** bandwidth / ETA / follow up / heads-up / on the same page / out of scope / push back

> **Dev:** Just a **(5A.1)** \_\_\_\_\_\_: the payment API will be down tomorrow from 9 to 10.
>
> **Vos:** Thanks! What's the **(5A.2)** \_\_\_\_\_\_ for the fix on the refund bug?
>
> **Dev:** Probably Thursday. Can you test the mobile flow too?
>
> **Vos:** Mobile is **(5A.3)** \_\_\_\_\_\_ for this sprint, and I don't have the **(5A.4)** \_\_\_\_\_\_ to test both this week. Let's talk to the PO so we're all **(5A.5)** \_\_\_\_\_\_.

### 5B. Reescribí con la expresión

Decí lo mismo usando la expresión entre paréntesis. Mantené el tiempo verbal de la oración original.

5B.1. I'll write to the dev team tomorrow to check if they fixed it. *(follow up)*

5B.2. I told the PM that releasing without regression tests was a bad idea, and I gave my reasons. *(push back)*

5B.3. If the bug isn't fixed today, I'll take it to my manager. *(escalate)*

5B.4. I'm the person responsible for the end-to-end suite. *(own)*

5B.5. We had to choose between speed and coverage. *(trade-off)*

## Bloque 6. Falsos amigos

### 6A. Elegí la palabra correcta

6A.1. \_\_\_\_\_\_, I work at a fintech company. *(Actually / Currently)*

6A.2. I \_\_\_\_\_\_ the meeting with the client yesterday. *(assisted / attended)*

6A.3. We \_\_\_\_\_\_ the regression tests on staging every night. *(realize / run)*

6A.4. That's a very \_\_\_\_\_\_ decision: it saves time and reduces risk. *(sensible / sensitive)*

6A.5. Before applying, I updated my \_\_\_\_\_\_ with my last project. *(career / résumé)*

### 6B. Corregí el falso amigo

Cada oración tiene una palabra que suena bien en español pero en inglés significa otra cosa. Encontrala y cambiala.

6B.1. Eventually we will migrate to Playwright, but it isn't decided yet.

6B.2. I can't support long meetings without an agenda.

6B.3. The lecture of the logs took me an hour.

6B.4. The release was a big exit: no bugs in production.

6B.5. Next year, I pretend to apply for a senior position.

## Bloque 7. Errores típicos de hispanohablantes

### 7A. Corregí la oración (parte 1)

Algunas oraciones tienen más de un error.

7A.1. Is necessary to update the test data every sprint.

7A.2. I received a lot of feedbacks after the demo.

7A.3. The meeting with the client is in Thursday at the 3 pm.

7A.4. Can you tell me where is the staging URL?

7A.5. If I would know the root cause, I would fix it.

### 7B. Corregí la oración (parte 2)

Acá también aparecen errores de tiempos verbales.

7B.1. What means "flaky test"?

7B.2. I work in Mercado Libre since 2022.

7B.3. He said me that the build was green.

7B.4. Playwright is more fast than Selenium for our suite.

7B.5. I checked the logs, but I didn't find nothing.

## Test final

Hacelo en la semana 15, sin mirar el documento de vocabulario. Son 15 preguntas de todas las secciones. Mandame las 15 juntas.

### Parte 1. Completá la palabra

Tenés la primera letra de cada palabra como ayuda.

T1. The bug only reproduces on s\_\_\_\_\_\_, not on my machine.

T2. The login broke after the deploy, so we had to r\_\_\_ b\_\_\_ the release.

T3. The chatbot told a customer about a refund policy that doesn't exist. That's a h\_\_\_\_\_\_\_\_\_\_\_.

T4. I'll send the a\_\_\_\_\_ i\_\_\_\_ to everyone after the retro.

T5. The s\_\_\_\_ t\_\_\_\_ points to a null value in the payment service.

### Parte 2. Corregí la oración

T6. Actually I'm learning about RAG and agents.

T7. I assisted to a conference about AI testing last month.

T8. We need more informations about the error before we can fix it.

T9. The people in my team is very collaborative.

T10. The demo is on Monday in 10 am.

### Parte 3. Explicalo en inglés

Una o dos oraciones cada una, como en una entrevista.

T11. What's the difference between severity and priority?

T12. What is a regression?

T13. What's the difference between authentication and authorization?

T14. What is RAG?

T15. What is a trade-off? Give an example from your work.

## Mi banco de palabras

Anotá acá las palabras que te cuestan, con una oración tuya sobre tu trabajo. Marcá la última columna la primera vez que la uses hablando (en un simulacro, en una daily o en una entrevista).

| Palabra | Mi oración | La usé hablando |
| --- | --- | --- |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

## Hoja de seguimiento

En *Estado* poné Pendiente, Repetir (menos de 4 de 5) o Aprobado. Las palabras que fallaste van a tu banco de palabras.

| Bloque | Fecha | Resultado | Palabras que fallé | Estado |
| --- | --- | --- | --- | --- |
| 1A. Testing: completá |  | \_\_ / 5 |  | Pendiente |
| 1B. Testing: usalas vos |  | \_\_ / 5 |  | Pendiente |
| 2A. Automatización: elegí |  | \_\_ / 5 |  | Pendiente |
| 2B. Automatización: explicalo |  | \_\_ / 5 |  | Pendiente |
| 3A. Bugs: completá |  | \_\_ / 5 |  | Pendiente |
| 3B. Severity y priority |  | \_\_ / 5 |  | Pendiente |
| 4A. IA: uní |  | \_\_ / 5 |  | Pendiente |
| 4B. IA: completá |  | \_\_ / 5 |  | Pendiente |
| 5A. Slack |  | \_\_ / 5 |  | Pendiente |
| 5B. Expresiones |  | \_\_ / 5 |  | Pendiente |
| 6A. Falsos amigos: elegí |  | \_\_ / 5 |  | Pendiente |
| 6B. Falsos amigos: corregí |  | \_\_ / 5 |  | Pendiente |
| 7A. Errores típicos 1 |  | \_\_ / 5 |  | Pendiente |
| 7B. Errores típicos 2 |  | \_\_ / 5 |  | Pendiente |
| Test final |  | \_\_ / 15 |  | Pendiente |

**Test final:** con 12 o más, el vocabulario de entrevistas está firme. Con menos, repetí los bloques de las preguntas que fallaste y volvé a hacer el test dos semanas después.
