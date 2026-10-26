# Cuaderno de práctica: Tiempos verbales

Oct 13, 2026 · @Enzo

Este cuaderno es el punto 2 del plan en versión práctica. El apunte de tiempos verbales explica la teoría; acá se practica, un tema por día, con oraciones de tu trabajo en QA e IA.

## Cómo usar este cuaderno

1. **Empezá por el diagnóstico.** Son 15 oraciones para ver qué tiempos ya te salen solos y cuáles no. Hacelo sin mirar el apunte, mandame las respuestas y te digo qué lecciones podés saltear y en cuáles conviene frenar.
2. **Hacé una lección por día.** Cada una tiene un repaso de dos líneas y 5 ejercicios cortos; te lleva unos 15 minutos. Si necesitás la teoría completa, cada repaso indica la sección del apunte.
3. **Mandame las respuestas en el chat** con la lección y el número, por ejemplo: *L5.2: Have you ever tested*. Te corrijo con tu frase, la versión correcta y la regla en una línea.
4. **Para avanzar necesitás 4 de 5 bien.** Si sacás menos, repetí la lección al día siguiente y hacé 10 minutos de Tense Runner filtrando ese tiempo.
5. **Anotá cada lección en la hoja de seguimiento** del final, y los errores que se repiten en el registro de errores.
6. **Al terminar, hacé el test final** y comparalo con el diagnóstico.

Los ejercicios 5 de cada lección son de producción: no tienen una única respuesta. Escribí sobre tu trabajo real, porque esas oraciones después las vas a usar en entrevistas.

Si tu profesor está trabajando otro tiempo verbal, seguí su orden y usá este cuaderno para reforzar lo que vean en clase.

### Ruta de 4 semanas

Una lección por día hábil. Los días que quedan libres son para Tense Runner (suite *Mis errores*) y para el registro de errores.

| Semana | Lunes | Martes | Miércoles | Jueves | Viernes |
| --- | --- | --- | --- | --- | --- |
| 1 | Diagnóstico | L1. Present Simple | L2. Present Continuous | L3. Simple vs Continuous | L4. Past Simple |
| 2 | L5. Present Perfect | L6. Present Perfect vs Past Simple (1) | L7. Present Perfect vs Past Simple (2) | L8. Present Perfect Continuous | Repaso con Tense Runner |
| 3 | L9. Perfect vs Perfect Continuous | L10. Past Continuous | L11. Past Perfect | L12. Past Perfect Continuous | Repaso con Tense Runner |
| 4 | L13. Will, going to y planes | L14. Futuros avanzados | L15. Used to y would | L16. Repaso mixto | Test final |

## Diagnóstico inicial

Completá con la forma correcta del verbo entre paréntesis. No mires el apunte: la idea es ver qué te sale solo. Mandame las 15 respuestas juntas, por ejemplo *D1: runs*.

D1. Our nightly job \_\_\_\_\_\_ (run) at 2 am every day.

D2. Can you call me later? I \_\_\_\_\_\_ (review) a pull request right now.

D3. I \_\_\_\_\_\_ (never / work) with Cypress, but I know Playwright well.

D4. We \_\_\_\_\_\_ (deploy) the hotfix two hours ago.

D5. I \_\_\_\_\_\_ (wait) for the staging environment since 9 am, and it's still down.

D6. When the alert came in, I \_\_\_\_\_\_ (write) the test report.

D7. By the time the client reported the issue, we \_\_\_\_\_\_ (already / fix) it.

D8. The pipeline \_\_\_\_\_\_ (run) slowly for weeks before we found the problem.

D9. "The login page is broken." "Don't worry, I \_\_\_\_\_\_ (check) it."

D10. We \_\_\_\_\_\_ (adopt) a new test management tool next quarter; it's already approved.

D11. Don't call me at 3 pm, I \_\_\_\_\_\_ (interview) a candidate then.

D12. By the end of the week, we \_\_\_\_\_\_ (close) all the critical tickets.

D13. Next month, I \_\_\_\_\_\_ (work) on this product for a whole year.

D14. At my old job, we \_\_\_\_\_\_ (have) a manual regression every Friday, but now it's automated.

D15. \_\_\_\_\_\_ you \_\_\_\_\_\_ (ever / use) an LLM to generate test data?

## Lección 1. Present Simple

**Repaso:** rutinas, hechos y cómo funciona un sistema o un proceso. Ojo con la **-s** en he / she / it, y con **do / does** en negativas y preguntas. *(Apunte, sección 1)*

1. The pipeline \_\_\_\_\_\_ (send) a Slack message when a test \_\_\_\_\_\_ (fail).
2. Our QA lead \_\_\_\_\_\_ (not / approve) releases without a test report.
3. Armá la pregunta: the agent / call / the search tool / before it answers?
4. Corregí los dos errores: *She don't write unit tests, she focus on E2E tests.*
5. Producí: describí en 2 oraciones qué hacés en un día normal de trabajo.

## Lección 2. Present Continuous

**Repaso:** algo que pasa ahora, algo temporal de esta etapa (*this sprint*, *these days*) y planes ya agendados. Se arma con **am / is / are + -ing**. No se usa con verbos de estado como know, need o want. *(Apunte, sección 2)*

1. Right now we \_\_\_\_\_\_ (migrate) our UI tests from Selenium to Playwright.
2. I can't join the call, I \_\_\_\_\_\_ (pair) with a developer on a production bug.
3. Pasá a negativa: *The new build is passing all the checks.*
4. Corregí: *I'm needing access to the staging database.*
5. Producí: ¿en qué estás trabajando esta semana? Respondé en 2 oraciones.

## Lección 3. Present Simple vs Present Continuous

**Repaso:** Present Simple es lo que pasa siempre o en general; Present Continuous es lo que pasa ahora o en esta etapa. Los verbos de estado (know, think como opinión, understand, need, depend, belong) van en Present Simple aunque hables de ahora. *(Apunte, secciones 1 y 2)*

1. We usually \_\_\_\_\_\_ (deploy) on Thursdays, but this week we \_\_\_\_\_\_ (deploy) on Friday because of the holiday.
2. The suite \_\_\_\_\_\_ (take) 40 minutes on average, but today it \_\_\_\_\_\_ (take) much longer.
3. Elegí: I **think / am thinking** this test is flaky.
4. Elegí: This endpoint **depends / is depending** on the auth service.
5. Corregí: *Every day I am checking the nightly report before the stand-up.*

## Lección 4. Past Simple

**Repaso:** pasado terminado, con fecha o con contexto (*yesterday*, *last sprint*, *in 2023*, *at my previous job*). Negativa y pregunta con **did + verbo base**. Los irregulares más usados están en el apéndice. *(Apunte, sección 5)*

1. Last sprint I \_\_\_\_\_\_ (write) 30 API tests and \_\_\_\_\_\_ (find) four bugs.
2. The deploy \_\_\_\_\_\_ (break) the checkout, so we \_\_\_\_\_\_ (roll) back to the previous version.
3. Armá la pregunta con *Why*: *The test failed because of a timeout.*
4. Corregí: *We didn't caught the bug before the release.*
5. Producí: contá en 2 o 3 oraciones qué hiciste ayer en el trabajo.

## Lección 5. Present Perfect

**Repaso:** pasado sin fecha que importa ahora: experiencia (*ever*, *never*), resultados (*already*, *just*, *yet*) y cambios. Se arma con **have / has + participio**. Nunca va con *yesterday*, *last*, *ago* ni *in 2023*. *(Apunte, sección 3)*

1. I \_\_\_\_\_\_ (just / merge) the fix, can you run the smoke tests?
2. \_\_\_\_\_\_ you \_\_\_\_\_\_ (ever / test) a RAG application?
3. Completá con *already* o *yet*: *We haven't released the new version \_\_\_\_\_\_.* / *I've \_\_\_\_\_\_ logged the bug in Jira.*
4. Corregí: *She has write three new test suites this month.*
5. Producí: ¿con qué herramientas trabajaste en tu carrera? Respondé en 2 oraciones con Present Perfect.

## Lección 6. Present Perfect vs Past Simple (1)

**Repaso:** si decís cuándo, o el período ya terminó, va Past Simple. Si no decís cuándo y lo que importa es la experiencia o el resultado de hoy, va Present Perfect. Es tu error más frecuente, por eso esta comparación tiene dos lecciones. *(Apunte, comparación Present Perfect vs Past Simple)*

1. I \_\_\_\_\_\_ (work) with Postman for years, but I \_\_\_\_\_\_ (start) using Playwright in 2024.
2. We \_\_\_\_\_\_ (find) a critical bug yesterday, and the devs \_\_\_\_\_\_ (not / fix) it yet.
3. Elegí: **I've led / I led** the migration to Playwright at my previous company.
4. Elegí: The PM **has asked / asked** for the report twice today, and it's only 11 am.
5. Corregí: *I have joined this team two years ago.*

## Lección 7. Present Perfect vs Past Simple (2): en entrevistas

**Repaso:** en una entrevista, tu experiencia general va en Present Perfect (*I've worked with...*) y el ejemplo concreto va en Past Simple (*At my last job, I built...*). Arrancá por lo general y bajá al ejemplo. Ojo: *for* + un período que ya terminó va con Past Simple. *(Apunte, comparación Present Perfect vs Past Simple)*

1. "\_\_\_\_\_\_ you ever \_\_\_\_\_\_ (work) in a team without QA?" "Yes, at my first job we \_\_\_\_\_\_ (not / have) any testers."
2. I \_\_\_\_\_\_ (use) Cypress for three years at my previous company, but I \_\_\_\_\_\_ (switch) to Playwright when I joined my current team.
3. Elegí: In my career, I **have mentored / mentored** five junior testers.
4. Elegí: When **have you started / did you start** working in QA?
5. Producí: respondé *What experience do you have with test automation?* en 3 oraciones: una general con Present Perfect y un ejemplo con Past Simple.

## Lección 8. Present Perfect Continuous

**Repaso:** algo que empezó antes y sigue ahora (o que acaba de terminar y se nota), con foco en la duración: *for* + período, *since* + punto de inicio, *all morning*, *lately*. Se arma con **have / has been + -ing**. *(Apunte, sección 4)*

1. I \_\_\_\_\_\_ (work) in QA for five years.
2. We \_\_\_\_\_\_ (investigate) this memory leak since Monday.
3. Armá la pregunta con *How long*: you / use / Playwright?
4. Corregí: *I'm working on this ticket since this morning.*
5. Producí: ¿qué estuviste aprendiendo últimamente? Respondé en 2 oraciones con *lately* o *recently*.

## Lección 9. Present Perfect vs Present Perfect Continuous

**Repaso:** Present Perfect habla del resultado o de la cantidad (*how many*, ya está hecho). Present Perfect Continuous habla de la duración o de la actividad (*how long*, todavía sigue). Los verbos de estado (know, have como posesión, be) no van en Continuous. *(Apunte, comparación Present Perfect vs Present Perfect Continuous)*

1. I \_\_\_\_\_\_ (write) 15 tests today. / I \_\_\_\_\_\_ (write) tests all morning.
2. You look tired. \_\_\_\_\_\_ you \_\_\_\_\_\_ (debug) that flaky test again?
3. Elegí: I **have known / have been knowing** the tech lead since 2021.
4. Elegí: The team **has fixed / has been fixing** 12 bugs this sprint.
5. Producí: dos oraciones sobre tu semana: una con lo que ya hiciste (cantidad, Present Perfect) y otra con algo que venís haciendo hace un tiempo (duración, Present Perfect Continuous).

## Lección 10. Past Continuous y Past Simple

**Repaso:** Past Continuous es la acción que estaba en progreso en el pasado, el fondo de la historia (**was / were + -ing**). Past Simple es la acción corta que la interrumpe. Regla práctica: *when* + Past Simple, *while* + Past Continuous. *(Apunte, sección 6 y comparación Past Simple vs Past Continuous)*

1. I \_\_\_\_\_\_ (run) the regression when the staging server \_\_\_\_\_\_ (go) down.
2. While the devs \_\_\_\_\_\_ (deploy) the new version, I \_\_\_\_\_\_ (notice) an error in the logs.
3. At 10 pm last night, the nightly job still \_\_\_\_\_\_ (run).
4. Corregí: *When I was finding the bug, I reported it immediately.*
5. Producí: contá en 2 o 3 oraciones algo que pasó en el trabajo mientras estabas haciendo otra cosa.

## Lección 11. Past Perfect

**Repaso:** lo que pasó antes de otro momento del pasado. Se arma con **had + participio**. Es muy útil en la parte *Situation* de una historia STAR: *The team had never automated anything.* *(Apunte, sección 7)*

1. When I joined the team, they \_\_\_\_\_\_ (never / write) a single automated test.
2. When I checked the dashboard, someone \_\_\_\_\_\_ (already / restart) the server.
3. Uní las dos oraciones con Past Perfect, empezando por *We found the bug after...*: *The release went out. Then we found the bug.*
4. Corregí: *I realized that I forgot to update the test data before the run.*
5. Producí: escribí la *Situation* de una historia STAR tuya, con al menos un Past Perfect.

## Lección 12. Past Perfect Continuous

**Repaso:** la duración de algo que venía pasando hasta un momento del pasado. Se arma con **had been + -ing**. Sirve mucho para explicar causas: *The tests had been failing for weeks.* *(Apunte, sección 8)*

1. The tests \_\_\_\_\_\_ (fail) for two weeks before anyone noticed.
2. I \_\_\_\_\_\_ (work) on the framework for six months when the company decided to switch tools.
3. Elegí: When I arrived, the team **had been waiting / was waiting** for the build for an hour.
4. Corregí: *She was tired because she has been testing all day.*
5. Producí: explicá en 1 o 2 oraciones la causa de un problema que tuvieron en tu equipo, usando Past Perfect Continuous.

## Lección 13. Will, going to y Present Continuous para el futuro

**Repaso:** **will** es una decisión que tomás en el momento, una promesa o una predicción sin evidencia. **Going to** es un plan ya decidido o una predicción con evidencia. **Present Continuous** es un plan agendado, con día u hora. Después de *when*, *as soon as*, *before* o *if* no va will: va presente. *(Apunte, secciones 9 y 10 y comparación will vs going to)*

1. "The build is red again." "OK, I \_\_\_\_\_\_ (take) a look."
2. We \_\_\_\_\_\_ (hire) two more QA engineers in January; the budget is already approved.
3. Look at the error rate in the dashboard. The deploy \_\_\_\_\_\_ (fail).
4. I \_\_\_\_\_\_ (meet) the product owner tomorrow at 10 to review the acceptance criteria.
5. Corregí: *I will call you as soon as the tests will finish.*

## Lección 14. Future Continuous, Future Perfect y Future Perfect Continuous

**Repaso:** **will be + -ing** es algo que va a estar en progreso en un momento del futuro. **Will have + participio** es algo que va a estar terminado antes de un momento del futuro (*by Friday*, *by the end of...*). **Will have been + -ing** es la duración hasta un momento del futuro. *(Apunte, secciones 11, 12 y 13)*

1. This time tomorrow, I \_\_\_\_\_\_ (present) the test strategy to the client.
2. By the end of the sprint, we \_\_\_\_\_\_ (automate) the whole checkout flow.
3. In June, I \_\_\_\_\_\_ (work) on this project for two years.
4. Corregí: *By next month we will migrate all the tests.*
5. Producí: respondé *Where do you see yourself in two years?* en 2 oraciones, con Future Perfect o going to.

## Lección 15. Used to y would

**Repaso:** **used to + verbo** son hábitos o estados del pasado que ya no pasan. **Would + verbo** solo sirve para hábitos repetidos, no para estados. Negativa y pregunta: *didn't use to* y *Did you use to...?* (sin d). Para un hábito de hoy, usá *usually*. *(Apunte, sección 14 y comparación used to vs would)*

1. At my previous job, we \_\_\_\_\_\_ (write) our tests in Java, but now we use TypeScript.
2. Before we had CI, we \_\_\_\_\_\_ (run) the whole regression by hand every Friday. Usá *would*.
3. Armá la pregunta: you / use to / write test cases in Excel?
4. Corregí (es un hábito de hoy): *I use to review the logs every morning.*
5. Producí: respondé *How was QA different at your first job?* en 2 o 3 oraciones con used to y would.

## Lección 16. Repaso mixto: una respuesta de entrevista real

**Repaso:** en una misma respuesta se mezclan varios tiempos: presente para tu rol actual, Present Perfect para tu experiencia, Past Simple para los ejemplos con fecha y futuro para tus objetivos. Esta lección junta todo lo anterior.

1. Corregí los 7 errores de tiempo verbal de esta respuesta a *Tell me about yourself*:

> I am a QA Automation Engineer since 2021. Currently, I work at a fintech company, where I am owning the end-to-end test suite. Last year I have reduced our regression time from four hours to forty minutes. Before that, I was working as a manual tester for two years, and I learn a lot about how users think. Lately I'm getting into AI testing, and in the future I will to work as an AI Engineer.

2. Reescribí esa respuesta con tus datos reales, ya corregida, y decila en voz alta tres veces.
3. Completá esta mini historia STAR: *Last month we \_\_\_\_\_\_ (prepare) a big release when I \_\_\_\_\_\_ (notice) that the payment tests \_\_\_\_\_\_ (fail) for days. Nobody \_\_\_\_\_\_ (see) it because the alerts \_\_\_\_\_\_ (be) muted. I \_\_\_\_\_\_ (fix) the alerts, and since then we \_\_\_\_\_\_ (not / miss) a single failing test.*
4. Producí: respondé *What are you working on these days, and what's next for you?* en 3 oraciones (Present Continuous y going to o will).
5. Grabate diciendo tu versión del ejercicio 2 y fijate si pronunciás bien las terminaciones -ed: *reduced, worked, learned, automated*. Si dudás, repasá la sección de -ed de la guía de pronunciación.

## Test final

Hacelo cuando termines las 16 lecciones, sin mirar el apunte ni el cuaderno. Mandame las 20 respuestas juntas, por ejemplo *T1: releases*, y lo comparamos con tu diagnóstico.

### Completá con la forma correcta

T1. Our team \_\_\_\_\_\_ (release) a new version every two weeks.

T2. Please don't touch staging, I \_\_\_\_\_\_ (run) the performance tests.

T3. \_\_\_\_\_\_ you \_\_\_\_\_\_ (ever / evaluate) an AI agent?

T4. I \_\_\_\_\_\_ (join) the company in March 2022.

T5. We \_\_\_\_\_\_ (use) GitHub Actions for three years now.

T6. The server \_\_\_\_\_\_ (crash) while we \_\_\_\_\_\_ (run) the load test.

T7. I realized that someone \_\_\_\_\_\_ (delete) the test data the night before.

T8. Users \_\_\_\_\_\_ (complain) about slow logins for weeks before we found the cause.

T9. "We need someone to review this PR." "I \_\_\_\_\_\_ (do) it."

T10. Look at all those red checks. The build \_\_\_\_\_\_ (fail).

T11. At 9 am tomorrow I \_\_\_\_\_\_ (deploy) to production, so I'll miss the stand-up.

T12. By December, we \_\_\_\_\_\_ (finish) the migration.

T13. We \_\_\_\_\_\_ (not / use to) have code reviews for test code before I joined.

### Elegí la opción correcta

T14. **I've fixed / I fixed** the bug last night, so it should be in today's build.

T15. **I've worked / I worked** at that company from 2019 to 2021.

T16. Sorry for the delay, **I've been dealing / I dealt** with an outage all morning.

T17. While I **checked / was checking** the logs, I **found / was finding** the root cause.

### Corregí el error

T18. *I am working here since 2020.*

T19. *If the test will fail again, I'll open a ticket.*

T20. *Did you finished the test plan?*

## Apéndice: verbos irregulares de trabajo

La segunda columna se usa en Past Simple (*I wrote*). La tercera, en todos los tiempos perfectos y en la pasiva (*I've written*, *it was written*). Los ejemplos alternan las dos para que veas cada forma en uso.

| Verbo | Pasado | Participio | Ejemplo |
| --- | --- | --- | --- |
| be | was / were | been | The build **has been** red all day. |
| become | became | become | Flaky tests **became** our biggest problem. |
| begin | began | begun | The outage **began** at 2 am. |
| break | broke | broken | The last merge **has broken** the build. |
| bring | brought | brought | I **brought** data to the discussion. |
| build | built | built | I **built** the framework from scratch. |
| catch | caught | caught | The tests **caught** the bug before production. |
| choose | chose | chosen | We **chose** Playwright over Cypress. |
| do | did | done | **Have** you **done** the code review? |
| fall | fell | fallen | Coverage **fell** to 60% after the refactor. |
| find | found | found | I **found** a race condition in the checkout. |
| forget | forgot | forgotten | I **forgot** to update the test data. |
| get | got | got (UK) / gotten (US) | We **got** the green light to release. |
| give | gave | given | I **gave** a demo of the new framework. |
| go | went | gone | The service **went** down during the demo. |
| grow | grew | grown | The suite **has grown** to 400 tests. |
| hold | held | held | We **held** off on the deploy until the fix was ready. |
| keep | kept | kept | I **kept** the old version in case we needed to roll back. |
| know | knew | known | **I've known** the tech lead since 2021. |
| lead | led | led | I **led** the migration to Playwright. |
| leave | left | left | I **left** two comments on your PR. |
| lose | lost | lost | We **lost** the logs after the restart. |
| make | made | made | We **made** the decision to delay the release. |
| mean | meant | meant | The bug **meant** that users couldn't pay. |
| meet | met | met | We **met** the deadline. |
| put | put | put | I **put** the flaky test in quarantine. |
| read | read | read | **I've read** the requirements twice. |
| run | ran | run | I **ran** the regression last night. |
| say | said | said | The dev **said** it wasn't a bug. |
| see | saw | seen | **Have** you **seen** this error before? |
| send | sent | sent | The pipeline **sent** an alert to Slack. |
| set | set | set | I **set** up a nightly job in GitHub Actions. |
| shut | shut | shut | They **shut** down the old QA environment. |
| spend | spent | spent | I **spent** two days on that bug. |
| split | split | split | We **split** the suite into four shards. |
| take | took | taken | It **took** us three days to find the cause. |
| teach | taught | taught | That incident **taught** me to test early. |
| tell | told | told | He **told** me it was fixed. |
| think | thought | thought | I **thought** it was a data problem. |
| throw | threw | thrown | The method **threw** an exception. |
| understand | understood | understood | I **understood** the root cause after reading the logs. |
| write | wrote | written | **I've written** more than 300 tests. |

**Ojo con los regulares:** en los verbos regulares el pasado y el participio son iguales (*fixed*, *automated*, *deployed*), así que lo que te dice el tiempo es el auxiliar: *I fixed* (Past Simple) vs *I've fixed* (Present Perfect).

## Hoja de seguimiento

Completala a medida que avanzás. En *Estado* poné Pendiente, Repetir (menos de 4 de 5) o Aprobada. El error que más se repita en cada lección va también al registro de errores.

| Lección | Fecha | Resultado | Error que más se repitió | Estado |
| --- | --- | --- | --- | --- |
| Diagnóstico |  | \_\_ / 15 |  | Pendiente |
| L1. Present Simple |  | \_\_ / 5 |  | Pendiente |
| L2. Present Continuous |  | \_\_ / 5 |  | Pendiente |
| L3. Simple vs Continuous |  | \_\_ / 5 |  | Pendiente |
| L4. Past Simple |  | \_\_ / 5 |  | Pendiente |
| L5. Present Perfect |  | \_\_ / 5 |  | Pendiente |
| L6. Present Perfect vs Past Simple (1) |  | \_\_ / 5 |  | Pendiente |
| L7. Present Perfect vs Past Simple (2) |  | \_\_ / 5 |  | Pendiente |
| L8. Present Perfect Continuous |  | \_\_ / 5 |  | Pendiente |
| L9. Perfect vs Perfect Continuous |  | \_\_ / 5 |  | Pendiente |
| L10. Past Continuous |  | \_\_ / 5 |  | Pendiente |
| L11. Past Perfect |  | \_\_ / 5 |  | Pendiente |
| L12. Past Perfect Continuous |  | \_\_ / 5 |  | Pendiente |
| L13. Will, going to y planes |  | \_\_ / 5 |  | Pendiente |
| L14. Futuros avanzados |  | \_\_ / 5 |  | Pendiente |
| L15. Used to y would |  | \_\_ / 5 |  | Pendiente |
| L16. Repaso mixto |  | \_\_ / 5 |  | Pendiente |
| Test final |  | \_\_ / 20 |  | Pendiente |

**Diagnóstico vs test final:** si en el test final sacás 17 o más, el punto 2 está superado y pasamos al punto 4 del plan (frases para entrevistas y método STAR). Tense Runner sigue todos los días, 10 minutos.
