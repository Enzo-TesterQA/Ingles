# Modales, condicionales, pasiva y preguntas

Oct 13, 2026 · @Enzo

Después de los tiempos verbales, estas son las estructuras que más aparecen en entrevistas técnicas: proponer soluciones, responder hipotéticos, describir procesos y hacer preguntas con naturalidad.

## 1. Modales

**Cómo se arman:** modal + verbo base, sin "to" y sin -s en tercera persona. Negativa: modal + not. Pregunta: modal + sujeto + verbo.

| Modal | Uso | Ejemplo en el trabajo | Negativa / pregunta |
| --- | --- | --- | --- |
| can | habilidad, posibilidad, permiso | I can write tests in TypeScript and Python. | I can't reproduce it. / Can you share the logs? |
| could | posibilidad, sugerencia suave, pedido cortés, habilidad pasada | We could run the tests in parallel. / Could you review my PR? | It couldn't connect to the database. |
| should | recomendación, lo esperable | We should add a test for that edge case. / The build should be ready in 10 minutes. | We shouldn't release with an open blocker. |
| would | hipotético, cómo actuarías, cortesía | I would start by checking the logs. / Would it be possible to extend the deadline? | I wouldn't automate that test. |
| might / may | posibilidad (no seguro) | It might be a caching issue. / This may affect other modules. | It might not be related. |
| must | obligación fuerte, deducción segura | All PRs must pass the checks. / It must be a config problem. | You mustn't share production data. |
| have to | obligación (externa) | We have to support Safari. | We don't have to test IE anymore. (no es necesario) |
| need to | necesidad | I need to update the test data. | You don't need to run the full suite. |

**Para sonar profesional en entrevistas:** usá **would** para describir cómo actuarías ("I would..."), **could** para proponer opciones ("We could also...") y **might** para hipótesis de causas ("It might be a race condition").

**Errores típicos:** "I can to test" (sin to), "She cans" (sin s), "I must to go". Ojo: **mustn't** = está prohibido; **don't have to** = no es necesario.

### Modales en pasado (modal + have + participio)

| Estructura | Significado | Ejemplo |
| --- | --- | --- |
| should have + participio | debería haber (crítica o arrepentimiento) | We should have tested the migration on staging first. |
| could have + participio | podría haber (posibilidad no aprovechada) | We could have caught it with a contract test. |
| would have + participio | habría (hipotético pasado) | An integration test would have caught the bug. |
| might have + participio | puede que haya (hipótesis sobre el pasado) | The deploy might have failed because of the new variable. |
| must have + participio | seguro que (deducción sobre el pasado) | Someone must have changed the config. |

Estas estructuras son oro para la parte "What did you learn?" de STAR: *Looking back, I should have involved QA earlier.*

## 2. Condicionales

| Tipo | Cuándo | Estructura | Ejemplo |
| --- | --- | --- | --- |
| Zero | Hechos y reglas que siempre se cumplen | If + presente, presente | If a test fails, the pipeline stops. |
| First | Situaciones reales o probables en el futuro | If + presente, will + verbo | If the fix is ready today, we'll release tomorrow. |
| Second | Situaciones hipotéticas o imaginarias (presente / futuro) | If + pasado, would + verbo | If I had more time, I would automate the mobile tests. |
| Third | Situaciones pasadas que no pasaron (arrepentimiento, análisis) | If + had + participio, would have + participio | If we had run the regression, we would have caught the bug. |

**Variantes útiles:**

- **Unless** = if not: *We won't release unless all blockers are fixed.*
- **As soon as / When** con futuro: *I'll let you know as soon as the build finishes.* (no "will finish")
- **If I were you** (consejo): *If I were you, I'd add a contract test.*
- **In case**: *I'll keep the old version in case we need to roll back.*

**Errores típicos:**

- Will o would después de if. Mal: "If the test will fail..." / "If I would have time..." Bien: "If the test **fails**..." / "If I **had** time...".
- Mezclar segundo y tercero. Mal: "If we tested it, we would have found it." Bien: "If we **had tested** it, we would have found it."

### Mixed conditional (bonus)

Pasado que afecta al presente: **If + had + participio, would + verbo**. *If we had automated the regression last year, we wouldn't be testing everything by hand now.*

## 3. Cómo responder preguntas hipotéticas

Muchas preguntas técnicas son hipotéticas: "What would you do if...?", "How would you test...?". Se responden con **would** (o I'd) durante toda la respuesta, no con presente ni con will.

| Paso | Frase |
| --- | --- |
| Aclarar el contexto | First, I'd want to understand... / It depends on..., but assuming... |
| Primer paso | I'd start by + -ing... |
| Pasos siguientes | Then I'd... / After that, I would... / I'd also make sure that... |
| Alternativa | If that didn't work, I'd... / Another option would be to... |
| Cerrar | That way, we'd... / The goal would be to... |

### Ejemplo: "What would you do if you found a critical bug one hour before a release?"

> First, I'd confirm that I can reproduce it and check how many users it would affect. Then I'd report it immediately to the developers and the release manager, with clear steps and evidence, instead of waiting for the stand-up. If the impact were high, I'd recommend delaying the release or turning off the feature with a feature flag. If it were a minor issue, I'd suggest releasing and fixing it in a hotfix, but the final decision would be made together with the product owner. Either way, I'd add a test for that case afterwards.

**Fijate:** "If the impact **were** high" (segundo condicional; were para todas las personas en estilo formal), "**I'd** recommend", "would be made" (pasiva con would).

### Preguntas hipotéticas para practicar

1. What would you do if a developer said your bug wasn't a bug?
2. How would you test a login page?
3. What would you do if your automated suite took three hours to run?
4. How would you test a chatbot that answers questions about company policies?
5. What would you do if you joined a team with no automation at all?
6. How would you prioritize if you had two days to test a big release?

## 4. Voz pasiva

**Cuándo se usa:** cuando importa la acción o el resultado más que quién lo hizo. Es muy común en bug reports, documentación y descripciones de procesos ("Tests are run on every PR").

**Cómo se arma:** to be (en el tiempo que corresponda) + participio. Si querés decir quién lo hizo, agregás **by**.

| Tiempo | Activa | Pasiva |
| --- | --- | --- |
| Present Simple | The pipeline runs the tests on every PR. | The tests **are run** on every PR. |
| Present Continuous | We are migrating the suite. | The suite **is being migrated**. |
| Present Perfect | Someone has fixed the bug. | The bug **has been fixed**. |
| Past Simple | QA found the issue during regression. | The issue **was found** during regression. |
| Past Continuous | They were deploying the service. | The service **was being deployed**. |
| Past Perfect | Someone had changed the config. | The config **had been changed**. |
| Future (will) | We will release the fix tomorrow. | The fix **will be released** tomorrow. |
| Modal | We should test this edge case. | This edge case **should be tested**. |

### En un bug report

> **Title:** Payment confirmation email is not sent when the card is declined twice
>
> The email **is not sent** after the second declined attempt. The issue **was reproduced** on staging and production. It **has been reported** by three customers. A test for this case **will be added** to the regression suite.

**Error típico:** olvidar el to be. Mal: "The bug fixed yesterday." Bien: "The bug **was fixed** yesterday." Y no abuses: en una entrevista, para hablar de tus logros, usá voz activa con **I** ("I fixed", no "it was fixed").

## 5. Formar preguntas

### El orden básico

**(Palabra interrogativa) + auxiliar + sujeto + verbo principal + resto.** El auxiliar depende del tiempo verbal.

| Tiempo | Auxiliar | Pregunta |
| --- | --- | --- |
| Present Simple | do / does | How often **do** you **deploy**? |
| Past Simple | did | Why **did** the test **fail**? |
| Present Perfect | have / has | **Have** you **worked** with Kafka? |
| Continuous | am / is / are / was / were | What **are** you **working** on? |
| Futuro / modal | will / would / can / should | **Would** you **use** Cypress or Playwright? |
| Verbo to be | am / is / are / was / were (sin auxiliar extra) | **Is** the build green? / Where **was** the error? |

**Excepción:** cuando preguntamos por el sujeto (who / what hace la acción) no hay auxiliar: *Who broke the build?* (no "Who did break") / *What caused the outage?*

### Preguntas indirectas (más corteses)

Después de una frase de introducción, el orden vuelve a ser afirmativo y no se usa do / does / did.

| Directa | Indirecta (más cortés) |
| --- | --- |
| What is the deadline? | Could you tell me **what the deadline is**? |
| How does the team handle releases? | I was wondering **how the team handles releases**. |
| Did the fix work? | Do you know **if the fix worked**? |
| Where are the logs? | Can you tell me **where the logs are**? |
| What tools do you use? | I'd like to know **what tools you use** for automation. |

### Question tags

Para confirmar algo: afirmativa + tag negativa, o negativa + tag afirmativa, con el mismo auxiliar.

- The tests run on every PR, **don't they**?
- You've already merged it, **haven't you**?
- It wasn't on staging, **was it**?
- We should add a test for this, **shouldn't we**?

**Errores típicos:** "What means this error?" (Bien: What **does** this error **mean**?), "Why the test failed?" (Bien: Why **did** the test **fail**?), "Can you tell me where is it?" (Bien: where **it is**).

## Ejercicios

Mandame las respuestas en el chat con el número y te corrijo.

### A. Modales: elegí el correcto

1. All pull requests **must / might** pass the checks before merging.
2. The error **might / should** be related to the new cache, but I'm not sure.
3. You **don't have to / mustn't** run the full suite, the smoke tests are enough.
4. **Could / Must** you share the logs with me?
5. Looking back, we **should have tested / should test** the migration on staging first.

### B. Condicionales: completá con la forma correcta

6. If a test \_\_\_\_\_\_ (fail), the pipeline stops. (zero)
7. If the fix \_\_\_\_\_\_ (be) ready today, we \_\_\_\_\_\_ (release) tomorrow. (first)
8. If I \_\_\_\_\_\_ (have) more time, I \_\_\_\_\_\_ (automate) the mobile tests. (second)
9. If we \_\_\_\_\_\_ (run) the regression, we \_\_\_\_\_\_ (catch) the bug. (third)
10. We won't release \_\_\_\_\_\_ all blockers are fixed. (unless / if)

### C. Pasiva: transformá

11. QA found the issue during regression. → The issue \_\_\_\_\_\_
12. Someone has changed the config. → The config \_\_\_\_\_\_
13. We will release the fix tomorrow. → The fix \_\_\_\_\_\_
14. We run the tests on every PR. → The tests \_\_\_\_\_\_

### D. Preguntas: corregí o transformá

15. Corregí: What means this error?
16. Corregí: Why the deploy failed?
17. Hacé indirecta: Where are the test reports? → Could you tell me...
18. Agregá el question tag: You've already merged the fix, \_\_\_\_\_\_?

### E. Hipotéticos (respuesta hablada o escrita, 3-5 oraciones)

19. What would you do if your automated suite took three hours to run?
20. How would you test a chatbot that answers questions about company policies?
