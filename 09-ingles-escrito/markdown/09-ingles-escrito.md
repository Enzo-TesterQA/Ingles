# Inglés escrito en el trabajo

Oct 13, 2026 · @Enzo

Plantillas listas para usar en stand-ups, bug reports, Slack, pull requests y mails de búsqueda laboral. Copialas, cambiá los datos y mandame tus versiones para corregir.

## 1. Stand-up

El stand-up es el mejor ejercicio diario de tiempos verbales: cada parte tiene el suyo.

| Parte | Tiempo verbal | Frases |
| --- | --- | --- |
| Ayer | Past Simple (con yesterday) o Present Perfect (sin momento, resultado ahora) | Yesterday I finished... / I worked on... / I've fixed... |
| Hoy | Present Continuous, going to, will | Today I'm working on... / I'm going to... / I'll pair with... |
| Bloqueos | Present Simple / Present Perfect Continuous | I'm blocked by... / I'm waiting for... / I've been trying to... but... |
| Nada nuevo | Present Simple | No blockers on my side. / Nothing new, still working on... |

### Ejemplo hablado o escrito

> **Yesterday** I finished the API tests for the orders endpoint and I found two bugs, which I've already logged in Jira.
>
> **Today** I'm going to review the new checkout tests and pair with María on the flaky login test.
>
> **Blockers:** I've been trying to run the mobile suite on the new device farm since yesterday, but the credentials don't work. Could someone from DevOps help me with that?

### Versión corta para Slack (async stand-up)

> **Done:** API tests for /orders (2 bugs logged: QA-231, QA-232)
>
> **Today:** review checkout tests, fix flaky login test
>
> **Blockers:** device farm credentials not working, waiting on DevOps

**Error típico:** "Yesterday I have finished..." (con yesterday va Past Simple) y "Today I work on..." (para lo que estás haciendo hoy, mejor Present Continuous: "Today I'm working on...").

## 2. Bug report

Un buen bug report permite que el dev lo reproduzca sin hacerte ninguna pregunta. Título específico, pasos numerados en imperativo, y resultado esperado vs. obtenido en Present Simple.

### Plantilla

```markdown
**Title:** [Qué falla] when [condición] on [dónde]

**Environment:** [staging / prod], [browser + version / device + OS], build [número]
**Severity:** [Critical / High / Medium / Low]

**Steps to reproduce:**
1. Go to ...
2. Click ...
3. Enter ...

**Expected result:** ...
**Actual result:** ...

**Frequency:** Always / Intermittent (3 out of 10 attempts)
**Evidence:** screenshot, video, logs, failing request
**Notes:** It started after build 1.4.2. It doesn't happen on Chrome.
```

### Ejemplo

> **Title:** Checkout button stays disabled after applying a discount code on Safari 17
>
> **Environment:** staging, Safari 17.2 on macOS 14, build 2.8.1
>
> **Severity:** High (blocks purchases for Safari users)
>
> **Steps to reproduce:** 1. Add any product to the cart. 2. Go to checkout. 3. Apply the code SAVE10. 4. Fill in the payment details.
>
> **Expected result:** The "Place order" button is enabled.
>
> **Actual result:** The button stays disabled. The console shows "TypeError: total is undefined".
>
> **Frequency:** Always on Safari. It doesn't happen on Chrome or Firefox.
>
> **Notes:** It started after the discount refactor was merged (PR #482).

**Verbos para títulos de bugs:** doesn't load, fails to, crashes when, returns 500, shows the wrong..., is not saved, stays disabled, is displayed twice, times out.

**Errores típicos:** títulos vagos ("Checkout doesn't work"), pasos en pasado ("I clicked..."; mejor imperativo: "Click...") y mezclar el resultado esperado con el obtenido.

## 3. Mensajes de Slack

En Slack se escribe corto, directo y amable. Arrancá con el contexto, después el pedido.

| Situación | Mensaje |
| --- | --- |
| Pedir ayuda | Hi team, quick question: has anyone seen this error on staging before? "Connection refused on port 5432". I've already restarted the container, but it keeps failing. |
| Avisar de un problema | Heads-up: the nightly regression failed because staging was down between 2 and 3 am. I'm re-running it now and I'll post the results here. |
| Avisar de un bug crítico | @here I found a blocker in the checkout flow on the release candidate: orders with discount codes can't be placed. Bug: QA-245. I'd suggest we hold off on the release until it's fixed. |
| Hacer seguimiento | Hi Juan, just following up on QA-231. Any updates on the fix? We'd like to include it in Friday's release. |
| Pedir una revisión | Hey, could you take a look at my PR when you have a moment? It adds API tests for the orders endpoint. No rush, end of day is fine. |
| Confirmar | Got it, thanks! I'll test it this afternoon. |
| Decir que no tengo tiempo | I'd love to help, but I don't have the bandwidth this sprint. Could we look at it next week, or could someone else pick it up? |
| No estar de acuerdo | I see your point, but I'm a bit worried about releasing without regression tests. Could we at least run the smoke suite first? |
| Disculparse por demora | Sorry for the late reply, I was in back-to-back meetings. Here's the report: ... |
| Cerrar un tema | All tests passed on the new build. Closing the ticket. Thanks for the quick fix! |

**Abreviaturas comunes en Slack:** FYI (for your information), ASAP (as soon as possible), EOD (end of day), ETA (estimated time), PTAL (please take a look), LGTM (looks good to me), WIP (work in progress), OOO (out of office), TL;DR (resumen).

**Error típico:** mensajes de una sola palabra como "Hi" y esperar respuesta. En equipos internacionales se considera mejor mandar el saludo y la pregunta en el mismo mensaje.

## 4. Pull requests y test reports

### Descripción de un PR

```markdown
**What:** Adds end-to-end tests for the guest checkout flow.

**Why:** Guest checkout had no automated coverage, and we found two regressions there last month.

**How:**
- Added a GuestCheckoutPage page object
- Added 6 tests: happy path, invalid card, expired card, empty cart, discount code, address validation
- Test data is created through the API and cleaned up after each test

**How to test:** Run `npx playwright test checkout/guest`

**Notes:** One test is skipped until QA-245 is fixed.
```

**Comentarios en PRs (code review):**

- Nit: could we rename this to `placeOrder` for consistency? (nit = detalle menor)
- What do you think about using a fixture here instead of creating the user in each test?
- This wait might make the test flaky. Could we wait for the response instead?
- LGTM, thanks for adding the negative cases!

### Resumen de una corrida de tests (test summary)

> **Regression results, release 2.9.0**
>
> We ran 412 tests on staging: 405 passed, 4 failed and 3 were skipped. Two failures are known issues (QA-231, QA-240). The other two are new: the password reset email isn't sent (QA-251, high) and the order history page loads slowly (QA-252, medium). **Recommendation:** go for release once QA-251 is fixed. Full report: \[link\]

**Tiempos:** los resultados van en Past Simple ("we ran", "405 passed"), el estado actual en Present Simple ("the email isn't sent"), y la recomendación en imperativo o con should / would.

## 5. Mails de búsqueda laboral

### Responder a un recruiter

> Hi Sarah,
>
> Thanks for reaching out. The QA Automation Engineer role sounds really interesting, especially the focus on AI-based testing. I'd be happy to have a call this week. I'm available on Wednesday or Thursday between 10 am and 2 pm (Argentina time, GMT-3).
>
> Best regards, Enzo

### Agradecer después de una entrevista (mandalo dentro de las 24 horas)

> Hi Michael,
>
> Thank you for taking the time to talk with me today. I really enjoyed learning about how your team is using LLMs to generate test data, and I'm even more excited about the role now.
>
> As I mentioned, I've built a Playwright framework from scratch and integrated it into CI, and I'd love to bring that experience to your team.
>
> Looking forward to hearing from you.
>
> Best, Enzo

### Hacer seguimiento si no te responden (después de una semana)

> Hi Sarah,
>
> I hope you're doing well. I wanted to follow up on my interview for the QA Automation Engineer position last Tuesday. I'm still very interested in the role. Is there any update on the next steps?
>
> Thanks again, Enzo

### Reprogramar una entrevista

> Hi Sarah,
>
> Unfortunately, something urgent has come up and I won't be able to make our call tomorrow at 3 pm. I'm really sorry for the inconvenience. Would it be possible to reschedule for Thursday or Friday? I'm flexible in the afternoon.
>
> Best regards, Enzo

### Aceptar o rechazar una oferta

> **Aceptar:** Hi Sarah, thank you so much for the offer. I'm happy to accept it, and I'm looking forward to joining the team on November 3rd. Please let me know what the next steps are.
>
> **Rechazar:** Hi Sarah, thank you for the offer and for your time during the process. After careful consideration, I've decided to accept another position that's a better fit for me right now. I really enjoyed meeting the team, and I hope our paths cross again.

**Saludos y cierres:** Hi \[nombre\] (lo más común), Hello, Dear \[nombre\] (formal). Cierres: Best, Best regards, Thanks, Kind regards. Evitá "Greetings" y "Waiting for your answer".

## 6. Suavizar el tono

Una traducción literal del español puede sonar brusca en inglés. Estas fórmulas mantienen el mensaje claro pero cortés.

| Suena brusco | Suena profesional |
| --- | --- |
| Send me the logs. | Could you send me the logs, please? |
| You're wrong. | I see it a bit differently. / I'm not sure that's the case, because... |
| This is a bad idea. | I'm a bit worried that this could cause... |
| Fix this today. | Would it be possible to fix this today? It's blocking the release. |
| I need an answer. | Any updates on this? / Just checking in on this. |
| Why didn't you test it? | Do you know if this case was covered in the tests? |
| No. | I don't think that will work, but what if we...? |
| Your code broke the build. | It looks like the last merge broke the build. Could you take a look? |
| I don't understand. | Could you clarify what you mean by...? |
| I want to... | I'd like to... |

**Trucos:** usá **could / would** para pedir, **it looks like / it seems** para señalar problemas sin culpar, y **we** en vez de **you** cuando hablás de un error del equipo.

## 7. Ejercicios de escritura

Uno por día, los jueves de la rutina. Mandame cada texto en el chat y te lo devuelvo corregido con las reglas.

1. Escribí tu stand-up de hoy (real) con las tres partes: ayer, hoy, bloqueos.
2. Escribí un bug report completo de un bug real que hayas encontrado (cambiá los datos sensibles).
3. Escribí un mensaje de Slack avisando que el pipeline está rojo y que lo estás investigando.
4. Escribí un mensaje de Slack diciendo que no tenés tiempo para una tarea, de forma amable.
5. Escribí la descripción de un PR que hayas hecho (o inventado) con What / Why / How.
6. Escribí el mail de agradecimiento después de una entrevista para un rol de AI Engineer.
7. Escribí un resumen de una corrida de regresión con 3 bugs encontrados y tu recomendación.
8. Reescribí en tono profesional: "Your change broke the tests. Fix it now."
9. Reescribí en tono profesional: "I need the requirements. Send them today."
10. Escribí tu "About" de LinkedIn en inglés (4 a 6 oraciones) usando Present Simple, Present Perfect y un logro con número.
