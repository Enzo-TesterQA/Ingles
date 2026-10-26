# Tiempos verbales para QA & AI Engineering

Oct 13, 2026 · @Enzo

## Cómo usar este apunte

Cada tiempo tiene la misma estructura: **cuándo se usa**, **cómo se arma** (afirmativa, negativa, pregunta), **ejemplos de tu día a día** en QA / AI, el **error típico** de hispanohablantes y las **palabras clave** que lo delatan. Al final hay comparaciones de los tiempos que más se confunden y ejercicios. Mandame tus respuestas en el chat y te corrijo.

### Mapa rápido

| Tiempo | Estructura | Para qué | Ejemplo corto |
| --- | --- | --- | --- |
| Present Simple | verbo / verbo+s | Rutinas, hechos, cómo funciona algo | The pipeline **runs** every night. |
| Present Continuous | am/is/are + -ing | Ahora mismo, temporal, planes cerrados | **I'm debugging** a flaky test. |
| Present Perfect | have/has + participio | Pasado sin fecha, experiencia, resultado hoy | **I've automated** 200 test cases. |
| Present Perfect Continuous | have/has been + -ing | Algo que empezó antes y sigue (duración) | **I've been working** with Playwright for two years. |
| Past Simple | verbo-ed / 2da columna | Pasado terminado, con fecha o contexto | We **released** v2.0 last Friday. |
| Past Continuous | was/were + -ing | Acción en progreso en el pasado | I **was running** the suite when it crashed. |
| Past Perfect | had + participio | Lo que pasó *antes* de otro pasado | The bug **had reached** prod before we caught it. |
| Past Perfect Continuous | had been + -ing | Duración antes de otro pasado | The test **had been failing** for days before anyone noticed. |
| Will | will + verbo | Decisión en el momento, predicción, promesa | **I'll check** the logs. |
| Going to | am/is/are going to + verbo | Plan ya decidido, predicción con evidencia | **We're going to migrate** to Playwright. |
| Future Continuous | will be + -ing | Acción en progreso en un momento futuro | At 3 pm **I'll be running** the regression. |
| Future Perfect | will have + participio | Algo terminado antes de un momento futuro | By Friday **we'll have fixed** all blockers. |
| Future Perfect Continuous | will have been + -ing | Duración hasta un momento futuro | In March **I'll have been working** here for 3 years. |

## 1. Present Simple

**Cuándo se usa:** rutinas y frecuencia, hechos generales, cómo funciona un sistema o un proceso, y describir tu rol actual. En entrevistas es el tiempo de "What do you do?".

| Forma | Estructura | Ejemplo |
| --- | --- | --- |
| Afirmativa | Sujeto + verbo (+s con he/she/it) | The CI pipeline **runs** on every pull request. |
| Negativa | Sujeto + don't / doesn't + verbo | This test **doesn't cover** the edge cases. |
| Pregunta | Do / Does + sujeto + verbo? | **Does** the suite **run** in parallel? |

| Situación en el trabajo | Oración |
| --- | --- |
| Describir tu rol | I **work** as a QA Automation Engineer and I **design** end-to-end tests. |
| Proceso del equipo | We **review** every bug in the daily stand-up. |
| Cómo funciona algo | The agent **calls** a retrieval tool before it **answers**. |
| Frecuencia | I usually **write** API tests with Postman and RestAssured. |

**Error típico:** olvidar la -s en tercera persona. Mal: *The test fail on Firefox.* Bien: *The test **fails** on Firefox.* También usar Present Simple para algo que está pasando ahora (eso es Continuous).

**Palabras clave:** always, usually, often, every day / sprint / release, normally, never.

## 2. Present Continuous

**Cuándo se usa:** algo que pasa ahora mismo, algo temporal de esta etapa ("this sprint", "these days"), y planes futuros ya agendados.

| Forma | Estructura | Ejemplo |
| --- | --- | --- |
| Afirmativa | Sujeto + am / is / are + verbo-ing | **I'm investigating** a flaky login test. |
| Negativa | Sujeto + am not / isn't / aren't + verbo-ing | The build **isn't passing** right now. |
| Pregunta | Am / Is / Are + sujeto + verbo-ing? | **Are** you **working** on the payment module this sprint? |

| Situación en el trabajo | Oración |
| --- | --- |
| Ahora mismo | I can't merge yet, the pipeline **is running**. |
| Etapa temporal | This sprint **we're migrating** our tests from Selenium to Playwright. |
| Plan agendado | **I'm meeting** the product owner tomorrow at 10. |
| Tendencia | More teams **are adopting** AI agents for test generation. |

**Error típico:** usarlo con verbos de estado (know, need, want, understand, believe). Mal: "I'm knowing Cypress." Bien: "I **know** Cypress." También olvidar el verbo to be. Mal: "I working on it." Bien: "**I'm working** on it."

**Palabras clave:** now, right now, at the moment, currently, this week / sprint, these days.

## 3. Present Perfect

**Cuándo se usa:** algo pasado **sin decir cuándo**, tu experiencia acumulada hasta hoy, y acciones recientes cuyo resultado importa ahora. Es el tiempo estrella para hablar de logros en entrevistas.

| Forma | Estructura | Ejemplo |
| --- | --- | --- |
| Afirmativa | Sujeto + have / has + participio | **I've built** a test framework from scratch. |
| Negativa | Sujeto + haven't / hasn't + participio | We **haven't found** the root cause yet. |
| Pregunta | Have / Has + sujeto + participio? | **Have** you ever **worked** with RAG pipelines? |

| Situación en el trabajo | Oración |
| --- | --- |
| Experiencia | **I've worked** with Cypress, Playwright and Appium. |
| Logro (sin fecha) | **I've reduced** the regression time from 4 hours to 40 minutes. |
| Resultado ahora | Someone **has broken** the staging build, nothing deploys. |
| Novedad en stand-up | **I've just fixed** the flaky checkout test. |
| Todavía no | The fix **hasn't been deployed** yet. |

**Error típico:** usarlo con un momento terminado. Mal: "I have fixed the bug yesterday." Bien: "I **fixed** the bug yesterday." (si hay fecha, va Past Simple). Y al revés: en español decimos "trabajo acá hace 2 años", pero en inglés es "**I've worked** here for 2 years", nunca "I work here since 2 years".

**Palabras clave:** ever, never, already, yet, just, so far, recently, since, for.

## 4. Present Perfect Continuous

**Cuándo se usa:** algo que empezó en el pasado y **sigue hasta ahora**, poniendo el foco en la duración o en el proceso. También para una actividad reciente que explica cómo están las cosas ahora.

| Forma | Estructura | Ejemplo |
| --- | --- | --- |
| Afirmativa | Sujeto + have / has been + verbo-ing | **I've been testing** this feature since Monday. |
| Negativa | Sujeto + haven't / hasn't been + verbo-ing | **The test hasn't been running** on the nightly job. |
| Pregunta | Have / Has + sujeto + been + verbo-ing? | How long **have you been working** in QA? |

| Situación en el trabajo | Oración |
| --- | --- |
| Duración hasta hoy | **I've been working** in test automation for four years. |
| Problema que sigue | **This test has been failing** intermittently for a week. |
| Proceso en curso | **We've been building** an LLM evaluation pipeline since Q2. |
| Explica el estado actual | Sorry for the delay, **I've been debugging** the CI runners all morning. |

**Error típico:** traducir "hace X que..." con presente. Mal: "I work with Playwright since 2022." Bien: "**I've been working** with Playwright since 2022." Y no usarlo con verbos de estado: "**I've known** him for years", no "I've been knowing".

**Palabras clave:** for, since, how long, all day / morning, lately, recently.

## 5. Past Simple

**Cuándo se usa:** acciones terminadas en un momento pasado concreto (dicho o claro por contexto). Es el tiempo principal de las respuestas STAR: "Tell me about a time when...".

| Forma | Estructura | Ejemplo |
| --- | --- | --- |
| Afirmativa | Sujeto + verbo-ed (o irregular, 2da columna) | **We found** a critical bug in the release candidate. |
| Negativa | Sujeto + didn't + verbo base | **The fix didn't solve** the timeout issue. |
| Pregunta | Did + sujeto + verbo base? | **Did you run** the smoke tests after the deploy? |

| Situación en el trabajo | Oración |
| --- | --- |
| Historia STAR | In my last project, **I noticed** that our tests took too long, so **I introduced** parallel execution. |
| Ayer en el stand-up | Yesterday **I wrote** API tests for the login endpoint. |
| Incidente | **The deploy failed** last night because of a missing env variable. |
| Trabajo anterior | At my previous company **I led** the migration to GitHub Actions. |

**Error típico:** conjugar dos veces en negativa o pregunta. Mal: "I didn't found the bug." / "Did you fixed it?" Bien: "I didn't **find** the bug." / "Did you **fix** it?" El auxiliar did ya lleva el pasado, el verbo queda en base.

**Irregulares que vas a usar mucho:** find-found, write-wrote, run-ran, break-broke, catch-caught, lead-led, build-built, take-took, choose-chose, set-set.

**Palabras clave:** yesterday, last week / sprint / year, ago, in 2023, when..., at my previous job.

## 6. Past Continuous

**Cuándo se usa:** una acción que estaba en progreso en un momento del pasado, casi siempre como "escenario" de otra acción corta (Past Simple) que la interrumpe. Sirve para poner contexto en una historia.

| Forma | Estructura | Ejemplo |
| --- | --- | --- |
| Afirmativa | Sujeto + was / were + verbo-ing | **I was reviewing** the logs when I spotted the error. |
| Negativa | Sujeto + wasn't / weren't + verbo-ing | **The monitoring wasn't working** during the outage. |
| Pregunta | Was / Were + sujeto + verbo-ing? | What **were you testing** when the app crashed? |

| Situación en el trabajo | Oración |
| --- | --- |
| Acción interrumpida | **We were running** the regression suite when the staging server went down. |
| Contexto de historia STAR | **I was working** on a fintech app, and the team **was struggling** with flaky tests. |
| Dos acciones a la vez | While **I was writing** the test cases, **the devs were fixing** the API. |
| Momento exacto | At 9 pm **we were still deploying** the hotfix. |

**Error típico:** usar Past Continuous para todo lo que en español es imperfecto ("trabajaba", "hacía"). Si es un hábito pasado, va Past Simple o used to. Mal: "At my old job I was writing tests every day." Bien: "At my old job **I wrote** / **I used to write** tests every day."

**Palabras clave:** while, when, at that moment, at 5 pm yesterday, all day yesterday.

## 7. Past Perfect

**Cuándo se usa:** para marcar que algo pasó **antes** de otro momento o acción del pasado. Es el "pasado del pasado". Muy útil en STAR para explicar qué había pasado antes de que vos intervinieras.

| Forma | Estructura | Ejemplo |
| --- | --- | --- |
| Afirmativa | Sujeto + had + participio | **The bug had reached** production before we caught it. |
| Negativa | Sujeto + hadn't + participio | **The team hadn't automated** any tests when I joined. |
| Pregunta | Had + sujeto + participio? | **Had they tested** the migration before the release? |

| Situación en el trabajo | Oración |
| --- | --- |
| Situación inicial (STAR) | When I joined, **the company had never used** CI/CD. |
| Causa de un incidente | The release failed because **someone had changed** the config manually. |
| Secuencia clara | By the time the PM asked, **I had already reported** the issue. |
| Experiencia previa | Before that role, **I had worked** only on manual testing. |

**Error típico:** usarlo para cualquier pasado "lejano". Solo hace falta cuando hay otro pasado de referencia. Mal: "In 2019 I had started in QA." Bien: "In 2019 **I started** in QA." Pero: "When I started in QA, **I had already studied** programming."

**Palabras clave:** already, before, by the time, when, never... before, after.

## 8. Past Perfect Continuous

**Cuándo se usa:** una acción que venía pasando durante un tiempo **hasta** otro momento del pasado. Foco en la duración o en el proceso previo. Se usa menos, pero suena muy natural en historias de incidentes.

| Forma | Estructura | Ejemplo |
| --- | --- | --- |
| Afirmativa | Sujeto + had been + verbo-ing | **The test had been failing** for days before anyone noticed. |
| Negativa | Sujeto + hadn't been + verbo-ing | **We hadn't been monitoring** the queue, so we missed the spike. |
| Pregunta | Had + sujeto + been + verbo-ing? | How long **had the service been crashing** before the alert fired? |

| Situación en el trabajo | Oración |
| --- | --- |
| Problema previo (STAR) | **The team had been releasing** without regression tests for months. |
| Duración antes de un cambio | **I had been working** as a manual tester for two years when I moved to automation. |
| Causa visible | The pipeline was slow because **the tests had been running** sequentially. |

**Error típico:** confundirlo con el Past Perfect simple. Past Perfect = algo terminado antes ("I had fixed it"). Past Perfect Continuous = algo que venía durando ("I had been fixing it for hours").

**Palabras clave:** for, since, how long, before, when, by the time.

## 9. Future Simple: will

**Cuándo se usa:** decisiones que tomás en el momento, ofrecimientos y promesas, y predicciones u opiniones sobre el futuro (sin evidencia concreta). En reuniones es el tiempo de "Yo me encargo".

| Forma | Estructura | Ejemplo |
| --- | --- | --- |
| Afirmativa | Sujeto + will (’ll) + verbo base | **I'll check** the logs and get back to you. |
| Negativa | Sujeto + won't + verbo base | Don't worry, **this change won't affect** the existing tests. |
| Pregunta | Will + sujeto + verbo base? | **Will the new endpoint support** pagination? |

| Situación en el trabajo | Oración |
| --- | --- |
| Decisión en el momento | The build is red? **I'll take** a look right now. |
| Ofrecimiento | **I'll pair** with you on the flaky test if you want. |
| Promesa | **I'll send** you the test report by the end of the day. |
| Predicción / opinión | I think AI agents **will change** how we write tests. |
| En entrevista | If you hire me, **I'll bring** strong experience in API automation. |

**Error típico:** usar will después de if / when en condicionales de futuro. Mal: "When the build will finish, I'll deploy." Bien: "When the build **finishes**, I'll deploy." También usar will para planes ya decididos (eso es going to).

**Palabras clave:** I think, probably, I'm sure, maybe, tomorrow, soon, OK / fine, I'll...

## 10. Future: going to (y Present Continuous para planes)

**Cuándo se usa:** planes e intenciones que ya decidiste antes de hablar, y predicciones basadas en algo que ves ahora (evidencia). Si el plan ya tiene día y hora en la agenda, también podés usar Present Continuous.

| Forma | Estructura | Ejemplo |
| --- | --- | --- |
| Afirmativa | Sujeto + am / is / are going to + verbo base | **We're going to add** contract tests next sprint. |
| Negativa | Sujeto + am not / isn't / aren't going to + verbo base | **We aren't going to support** IE anymore. |
| Pregunta | Am / Is / Are + sujeto + going to + verbo base? | **Are you going to automate** the mobile flows too? |

| Situación en el trabajo | Oración |
| --- | --- |
| Plan decidido | **I'm going to refactor** the page objects this week. |
| Predicción con evidencia | Look at those error rates, **the deploy is going to fail**. |
| Roadmap | **The team is going to migrate** from Jenkins to GitHub Actions in Q1. |
| Agenda cerrada (Present Cont.) | **I'm presenting** the test strategy to the client on Thursday. |
| En entrevista (objetivos) | **I'm going to get** my ISTQB Advanced certification next year. |

**Will vs going to en una línea:** will = lo decido ahora ("I'll fix it"). going to = ya lo tenía decidido ("I'm going to fix it this afternoon").

**Error típico:** olvidar el verbo to be. Mal: "I going to test it." Bien: "**I'm going to test** it." Y en el habla rápida se dice "gonna", pero no lo escribas en un mail o un ticket.

**Palabras clave:** next sprint / week / quarter, tomorrow, this afternoon, plan, look!

## 11. Future Continuous

**Cuándo se usa:** una acción que va a estar en progreso en un momento concreto del futuro. También suena más amable y profesional para preguntar por planes ajenos.

| Forma | Estructura | Ejemplo |
| --- | --- | --- |
| Afirmativa | Sujeto + will be + verbo-ing | This time tomorrow **I'll be running** the full regression. |
| Negativa | Sujeto + won't be + verbo-ing | **I won't be working** on Friday, I'm off. |
| Pregunta | Will + sujeto + be + verbo-ing? | **Will you be joining** the sprint review? |

| Situación en el trabajo | Oración |
| --- | --- |
| Momento futuro | At 10 am **we'll be deploying** to production, so avoid merging. |
| Pregunta amable | **Will you be using** the staging environment this afternoon? |
| Rol futuro (entrevista) | In this role, **I'll be working** closely with developers and product. |

**Error típico:** olvidar el be. Mal: "I will working on it." Bien: "**I'll be working** on it."

**Palabras clave:** this time tomorrow / next week, at 3 pm, all day tomorrow, in this role.

## 12. Future Perfect

**Cuándo se usa:** algo que va a estar **terminado antes** de un momento futuro. Ideal para hablar de deadlines y objetivos de sprint.

| Forma | Estructura | Ejemplo |
| --- | --- | --- |
| Afirmativa | Sujeto + will have + participio | By Friday **we'll have fixed** all the blockers. |
| Negativa | Sujeto + won't have + participio | **We won't have finished** the migration by the release date. |
| Pregunta | Will + sujeto + have + participio? | **Will you have reviewed** the PR before the demo? |

| Situación en el trabajo | Oración |
| --- | --- |
| Deadline | By the end of the sprint **I'll have automated** the whole checkout flow. |
| Objetivo (entrevista) | In my first 90 days, **I'll have set up** a stable smoke suite in CI. |
| Riesgo | If we don't start today, **we won't have tested** the integration in time. |

**Error típico:** usar Future Simple con "by". Mal: "By Monday I will finish the report." (no es incorrecto del todo, pero no marca el plazo). Mejor: "By Monday **I'll have finished** the report."

**Palabras clave:** by + momento (by Friday, by then, by the end of the sprint), before, in X days.

## 13. Future Perfect Continuous

**Cuándo se usa:** la duración de algo que sigue hasta un momento futuro. Es el menos usado; aparece sobre todo para hablar de años de experiencia o de cuánto viene durando un problema.

| Forma | Estructura | Ejemplo |
| --- | --- | --- |
| Afirmativa | Sujeto + will have been + verbo-ing | In March **I'll have been working** in QA for five years. |
| Negativa | Sujeto + won't have been + verbo-ing | **We won't have been using** the new framework long enough to judge it. |
| Pregunta | Will + sujeto + have been + verbo-ing? | How long **will the suite have been running** by the time we leave? |

| Situación en el trabajo | Oración |
| --- | --- |
| Años de experiencia | Next year **I'll have been automating** tests for six years. |
| Duración de un problema | By Friday **this bug will have been blocking** us for two weeks. |

**Error típico:** forzarlo cuando un Present Perfect Continuous alcanza. Si no hay un momento futuro claro (by..., in March...), no lo uses.

**Palabras clave:** by + momento futuro + for + duración.

## 14. used to vs would (hábitos del pasado)

**Cuándo se usa:** para algo que hacías habitualmente antes y **ya no hacés**. Es el equivalente natural del imperfecto "antes hacíamos...". **used to** sirve para acciones y estados; **would** solo para acciones repetidas, y suele ir después de que ya pusiste el contexto con used to.

| Forma | used to | would |
| --- | --- | --- |
| Afirmativa | **We used to test** everything manually. | Every release, **we would spend** two days on regression. |
| Negativa | **We didn't use to have** a staging environment. | (casi no se usa en negativa) |
| Pregunta | **Did you use to work** with Selenium? | (casi no se usa en pregunta) |
| Con estados (be, have, know) | **I used to be** a manual tester. | Mal: "I would be a manual tester." |

| Situación en el trabajo | Oración |
| --- | --- |
| Antes vs ahora (entrevista) | **I used to do** only manual testing, but now I focus on automation. |
| Historia de mejora | **We used to deploy** once a month. **We would freeze** the code for a week and test everything by hand. |
| Estado pasado | **Our pipeline used to take** over an hour. |

**Error típico:** usar used to en presente para "suelo". Mal: "I use to write tests in the morning." Bien: "I **usually** write tests in the morning." Y en negativa / pregunta va sin d: "didn't **use** to", "did you **use** to".

**Ojo:** "be used to + -ing" es otra cosa: estar acostumbrado. "**I'm used to working** with tight deadlines."

## Comparaciones: los tiempos que más se confunden

### Present Perfect vs Past Simple

La pregunta clave: **¿digo o está claro cuándo pasó?** Sí = Past Simple. No, o el período sigue abierto (today, this week, ever) = Present Perfect.

| Present Perfect (sin fecha / resultado hoy) | Past Simple (momento terminado) |
| --- | --- |
| **I've worked** with Appium. | **I worked** with Appium at my previous job. |
| **We've found** three critical bugs this sprint. | **We found** three critical bugs last sprint. |
| **Have you ever led** a QA team? | **Did you lead** the QA team in 2023? |
| **The build has failed**, nobody can deploy. | **The build failed** yesterday at 6 pm. |

Truco de entrevista: abrí con Present Perfect ("**I've worked** on several e-commerce projects") y pasá a Past Simple apenas contás la historia ("In one of them, **I built**...").

### Past Simple vs Past Continuous

Past Continuous = el escenario largo. Past Simple = la acción corta que pasa en el medio.

| Past Continuous (en progreso) | Past Simple (acción puntual) |
| --- | --- |
| **I was running** the tests... | ...when **the server crashed**. |
| **We were preparing** the release... | ...when **QA found** a blocker. |
| While **the devs were refactoring**,... | ...**I updated** the test data. |

### Present Perfect vs Present Perfect Continuous

Present Perfect = resultado o cantidad (cuánto hiciste). Continuous = duración o proceso (cuánto tiempo viene pasando).

| Present Perfect (resultado) | Present Perfect Continuous (duración) |
| --- | --- |
| **I've written** 50 test cases today. | **I've been writing** test cases all day. |
| **I've fixed** the flaky test. (ya está) | **I've been fixing** the flaky test. (todavía o recién) |
| **We've migrated** 80% of the suite. | **We've been migrating** the suite since July. |

### Will vs going to vs Present Continuous

| will (decido ahora) | going to (ya decidido) | Present Continuous (agendado) |
| --- | --- | --- |
| OK, **I'll write** the test plan. | **I'm going to write** the test plan this week. | **I'm presenting** the test plan on Monday at 11. |
| I think **it'll work**. | Look at the logs, **it's going to fail**. | — |

### used to vs would vs Past Simple

| used to (hábito o estado que ya no es) | would (acción repetida, en una historia) | Past Simple (una vez, o hábito con período cerrado) |
| --- | --- | --- |
| **We used to release** monthly. | **We would test** everything by hand. | In 2021 **we released** monthly. |
| **I used to be** a manual tester. | Mal: "I would be a manual tester." | **I was** a manual tester for two years. |

## Ejercicios

Respondé en el chat con el número de cada ítem (por ejemplo "1. has failed"). Las soluciones te las doy cuando me mandes tus respuestas, con la corrección de cada una.

### A. Completá con el tiempo correcto

1. Our pipeline usually \_\_\_\_\_\_ (take) about 20 minutes.
2. Hold on, I \_\_\_\_\_\_ (run) the smoke tests right now.
3. I \_\_\_\_\_\_ (work) with Playwright since 2022.
4. Last sprint we \_\_\_\_\_\_ (find) a memory leak in the payment service.
5. I \_\_\_\_\_\_ (review) the logs when the alert \_\_\_\_\_\_ (go) off.
6. When I joined the company, they \_\_\_\_\_\_ (never / use) any automation framework.
7. "The build is red." "OK, I \_\_\_\_\_\_ (look) at it now."
8. By the end of the month, we \_\_\_\_\_\_ (migrate) all the tests to GitHub Actions.

### B. Corregí el error (hay uno en cada oración)

9. I have fixed the bug yesterday.
10. The test fail on Safari but not on Chrome.
11. Did you found the root cause?
12. I work in QA since five years.
13. When the deploy will finish, I'll run the regression.
14. I'm knowing Python and TypeScript.
15. I use to write my test cases in Jira.

### C. Elegí la opción correcta

16. **I've reduced / I reduced** the execution time by 60% in my last project.
17. **Have you ever worked / Did you ever work** with LLM evaluations?
18. Sorry I'm late, **I've been fixing / I've fixed** the CI runners all morning.
19. **We're going to adopt / We'll adopt** contract testing next quarter, it's already in the roadmap.
20. **We used to / We would** have a dedicated QA environment, but they shut it down.
21. While I **tested / was testing** the API, the devs **deployed / were deploying** a new version.

### D. Transformá la oración

22. We test the login flow every day. → negativa
23. The agent called the retrieval tool. → pregunta
24. She has automated the onboarding flow. → pregunta con "yet"
25. They were running the load tests. → negativa
26. I will finish the test report today. → Future Perfect, empezando con "By 6 pm..."
27. I started working on this bug three hours ago and I'm still on it. → una sola oración con Present Perfect Continuous

### E. Producí (respuestas de entrevista, 2-4 oraciones)

28. "What do you do in your current role?" (Present Simple + Present Continuous)
29. "What testing tools have you worked with?" (Present Perfect + un ejemplo en Past Simple)
30. "Tell me about a time when you found a critical bug." (Past Simple + Past Continuous + Past Perfect)
31. "How was QA different at your previous company?" (used to / would)
32. "Where do you see yourself in two years?" (going to / will / Future Perfect)
