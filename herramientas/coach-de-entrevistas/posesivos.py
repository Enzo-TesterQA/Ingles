"""Posesivos y pronombres (doc 14) para el coach de tiempos verbales.

Los ítems van en tiempos.json con "tema": "pos" y "nivel": 4 (los arma build_tiempos.py desde P).
grade() no mira tiempos verbales: busca la frase esperada y los errores típicos.

kind: "f" completar, "c" elegir, "x" corregir el error, "tr" transformar.
answers: frases que tiene que tener tu oración (alcanza con una).
bad: frases que repiten el error (MAL).
escribir: its/it's, your/you're y el apóstrofo suenan igual: ese ítem se escribe con el teclado.
"""
import re

BIEN, CASI, MAL = "bien", "casi", "mal"

# (id, kind, consigna, modelo, answers, bad, regla, escribir)
P = [
    # sujeto obligatorio
    ("01", "x", "Represents the time that passes.", "It represents the time that passes.",
     ["it represents"], ["it represent the"], "El sujeto es obligatorio en inglés, aunque sea it.", False),
    ("02", "x", "Fails on Safari but works on Chrome.", "It fails on Safari but works on Chrome.",
     ["it fails"], [], "El sujeto es obligatorio: It fails...", False),
    ("03", "x", "Is very important for me.", "It's very important to me.",
     ["it's very important", "it's important"], [], "Sujeto obligatorio (it). Y important to me suena más natural.", False),
    ("04", "x", "Have two critical bugs in staging.", "There are two critical bugs in staging.",
     ["there are two"], ["have two"], "Para decir que algo existe: there is / there are.", False),
    ("05", "x", "Was a really hard sprint.", "It was a really hard sprint.",
     ["it was"], [], "El sujeto es obligatorio: It was...", False),
    ("06", "tr", "Say it again with a subject: Takes about twenty minutes to run.",
     "It takes about twenty minutes to run.", ["it takes"], [], "Tiempo y duración: el sujeto es it (It takes...).", False),
    # my / mine / of me
    ("07", "x", "The first object of me is my wedding ring.", "My first object is my wedding ring.",
     ["my first object"], ["object of me"], "El posesivo va antes del sustantivo: my, nunca \"of me\".", False),
    ("08", "x", "The laptop of me is very slow.", "My laptop is very slow.",
     ["my laptop"], ["laptop of me"], "El posesivo va antes del sustantivo: my laptop.", False),
    ("09", "f", "This laptop isn't the company's. It's ___. (my / mine)", "This laptop isn't the company's. It's mine.",
     ["it's mine"], ["it's my"], "Sin sustantivo después: mine, yours, his, hers, ours, theirs.", False),
    ("10", "x", "Lucía is a friend of me.", "Lucía is a friend of mine.",
     ["friend of mine"], ["friend of me"], "La única forma con of: a friend of mine / of yours.", False),
    ("11", "x", "I always wear the watch at work.", "I always wear my watch at work.",
     ["wear my watch"], ["wear the watch"], "Ropa y accesorios propios: posesivo, no artículo.", False),
    ("12", "x", "We support us in the difficult moments.", "We support each other in difficult moments.",
     ["support each other"], ["support us"], "Uno al otro: each other.", False),
    ("13", "tr", "Answer with mine: Is this branch yours?", "Yes, this branch is mine.",
     ["is mine", "it's mine"], ["is my"], "Sin sustantivo después: mine.", False),
    # his / her / its / their
    ("14", "c", "Saturn is famous for ___ rings. (his / its)", "Saturn is famous for its rings.",
     ["for its rings", "for it's rings"], ["his rings"], "Cosas, planetas, apps y animales: its.", False),
    ("15", "c", "My wife wears ___ wedding ring every day. (his / her)", "My wife wears her wedding ring every day.",
     ["wears her"], ["wears his"], "El posesivo depende del dueño: ella = her.", False),
    ("16", "c", "Martín forgot to update ___ test data. (his / her / its)", "Martín forgot to update his test data.",
     ["update his"], ["update her"], "El dueño es un hombre: his.", False),
    ("17", "c", "The API changed ___ response format. (his / its / their)", "The API changed its response format.",
     ["changed its", "changed it's"], ["changed his", "changed their"], "Una cosa (la API): its.", False),
    ("18", "c", "The developers pushed ___ changes on Friday. (his / their / theirs)",
     "The developers pushed their changes on Friday.", ["pushed their", "pushed there"], ["pushed his", "pushed theirs"],
     "Varios dueños: their (antes del sustantivo).", False),
    ("19", "c", "Each user can change ___ password. (his / their)", "Each user can change their password.",
     ["change their", "change there"], ["change his"], "Persona sin género conocido: their en singular.", False),
    ("20", "x", "My daughter loves his Riolu plush.", "My daughter loves her Riolu plush.",
     ["loves her"], ["loves his"], "El dueño manda: tu hija = her.", False),
    ("21", "tr", "Describe the app: The app lost the session after the update. (use its)",
     "The app lost its session after the update.", ["lost its", "lost it's"], ["lost his"], "Una cosa: its.", False),
    # its / it's (se escriben)
    ("22", "f", "___ a Pokémon named Riolu. (Its / It's)", "It's a Pokémon named Riolu.",
     ["it's a"], ["its a"], "it's = it is. its = de eso.", True),
    ("23", "f", "The service lost ___ connection to the database. (its / it's)",
     "The service lost its connection to the database.", ["lost its connection"], ["lost it's"],
     "Posesivo de una cosa: its, sin apóstrofo.", True),
    ("24", "f", "___ been flaky since the last deploy. (Its / It's)", "It's been flaky since the last deploy.",
     ["it's been"], ["its been"], "It's = it has (it has been).", True),
    ("25", "f", "I like this framework because of ___ documentation. (its / it's)",
     "I like this framework because of its documentation.", ["of its documentation"], ["of it's"],
     "Posesivo: its. Probá el truco: \"because of it is documentation\" no tiene sentido.", True),
    ("26", "f", "___ right, ___ fix works. (Your / You're)", "You're right, your fix works.",
     ["you're right your fix"], ["your right"], "you're = you are. your = tu.", True),
    ("27", "f", "___ PR broke the build? (Whose / Who's)", "Whose PR broke the build?",
     ["whose pr"], ["who's pr"], "whose = de quién. who's = who is.", True),
    # 's
    ("28", "tr", "Say it with 's: The plush of my daughter is a Pokémon.", "My daughter's plush is a Pokémon.",
     ["daughter's plush", "daughter's stuffed"], ["plush of my daughter"], "Dueño + 's + cosa: my daughter's plush.", False),
    ("29", "tr", "Say it with 's: The watch of my father is very old.", "My father's watch is very old.",
     ["father's watch", "dad's watch"], ["watch of my father"], "Dueño + 's + cosa: my father's watch.", False),
    ("30", "tr", "Say it with 's: The pull request of Enzo is ready.", "Enzo's pull request is ready.",
     ["enzo's pull request", "enzo's pr"], ["request of enzo"], "Nombre propio + 's: Enzo's PR.", False),
    ("31", "x", "This plush is from my daughter. (quiero decir que es de ella)",
     "This plush belongs to my daughter.", ["belongs to my daughter", "is my daughter's"], ["is from my"],
     "De quién es algo: belongs to o 's. from = origen.", False),
    ("32", "tr", "Write it with an apostrophe: the comments of the developers were useful.",
     "The developers' comments were useful.", ["developers' comments"], ["developer's comments", "comments of the developers"],
     "Plural con -s: solo apóstrofo (developers').", True),
    ("33", "tr", "Say it with 's: The toys of the children are everywhere.", "The children's toys are everywhere.",
     ["children's toys"], ["childrens toys", "toys of the children"], "Plural irregular (sin -s): + 's.", False),
    # pronombres sujeto / objeto
    ("34", "x", "Me and my team automated the regression suite.", "My team and I automated the regression suite.",
     ["my team and i"], ["me and my team"], "Como sujeto va I, y al final.", False),
    ("35", "f", "Between you and ___, the deadline isn't realistic. (I / me)",
     "Between you and me, the deadline isn't realistic.", ["you and me"], ["you and i"],
     "Después de preposición: me, him, her, us, them.", False),
    ("36", "f", "The QA lead asked ___ for a report. (we / us)", "The QA lead asked us for a report.",
     ["asked us"], ["asked we"], "Objeto: us.", False),
    ("37", "f", "I taught ___ Playwright. (me / myself)", "I taught myself Playwright.",
     ["taught myself"], ["taught me"], "Sujeto y objeto son la misma persona: myself.", False),
    # concordancia con it / he / she
    ("38", "x", "Its have a little planet in it.", "It has a little planet in it.",
     ["it has"], ["it have", "its have"], "Sujeto it + verbo con -s: it has.", False),
    ("39", "x", "The test that cover the login is failing.", "The test that covers the login is failing.",
     ["that covers"], ["that cover the"], "El verbo concuerda con the test (= it): covers.", False),
    ("40", "x", "We really likes Lego and Pokémon.", "We really like Lego and Pokémon.",
     ["we really like"], ["we really likes", "we likes"], "La -s va solo con he / she / it.", False),
    ("41", "x", "I don't know what is the problem.", "I don't know what the problem is.",
     ["what the problem is"], ["what is the problem"], "Pregunta indirecta: sujeto + verbo, sin invertir.", False),
    ("42", "x", "It shows how important is every moment.", "It shows how important every moment is.",
     ["important every moment is"], ["important is every"], "Dentro de otra frase: sujeto + verbo (every moment is).", False),
    # producción libre
    ("43", "tr", "Tell me about your watch in one sentence. Use It and its.",
     "It's a nice watch, and its face has a small Saturn.", ["its"], [],
     "Usá el sujeto it y el posesivo its (sin apóstrofo).", True),
    ("44", "tr", "Tell me something your team did. Start with My team and I.",
     "My team and I automated the whole regression suite.", ["my team and i"], ["me and my team"],
     "Como sujeto: My team and I...", False),
]

CONTR = [(r"\bit is\b", "it's"), (r"\byou are\b", "you're"), (r"\bthey are\b", "they're"),
         (r"\bwho is\b", "who's"), (r"\bi am\b", "i'm"), (r"\bis not\b", "isn't"), (r"\bdo not\b", "don't"),
         (r"\bdoes not\b", "doesn't"), (r"\bstuffed animal\b", "stuffed"), (r"\bpull request\b", "pr")]

GENERAL = [
    (r"\b(?:the|a|an) (?:my|your|his|her|its|our|their)\b", "El posesivo no lleva artículo: my watch, no the my watch."),
    (r"\b(?:object|friend|laptop|team|watch|ring|plush|car|house|wife|daughter|job|code|pr|branch)s? of (?:me|us)\b",
     "El posesivo va antes del sustantivo: my laptop / our team, no laptop of me."),
    (r"\b(?:it|he|she) have\b", "Con it / he / she va has: it has."),
    (r"\b(?:i|we|you|they) (?:really |also |usually )?(?:likes|has|wants|needs|works|uses)\b",
     "La -s va solo con he / she / it: we like, they use."),
    (r"^me and\b", "Como sujeto: My team and I..., no Me and my team."),
    (r"\bits'", "its' no existe: its (de eso) o it's (it is)."),
]


def norm(text):
    t = text.replace("’", "'").replace("‘", "'").replace("é", "e").lower()
    t = re.sub(r"[^a-z0-9' ]+", " ", t)
    t = re.sub(r"(?<![a-z])'|'(?![a-z])(?<!s')", " ", t)  # comillas sueltas fuera, deja developers'
    for a, b in CONTR:
        t = re.sub(a, b, t)
    return re.sub(r"\s+", " ", t).strip()


def toks(text):
    return norm(text).split()


def has(phrase, tk):
    p = toks(phrase)
    k = len(p)
    return k > 0 and any(tk[i:i + k] == p for i in range(len(tk) - k + 1))


def grade(item, said):
    tk = toks(said)
    joined = " ".join(tk)
    rule = item["rule"]
    res = {"tiempos": [], "objetivo": "pos", "regla": rule, "avisos": [], "errores": []}

    def out(v, why):
        res["veredicto"], res["motivo"] = v, why
        return res

    if not tk:
        return out(MAL, "No escuché ninguna oración.")
    if len(tk) < 3:
        return out(CASI, "Decí la oración completa, no solo la palabra que falta.")
    gen = [msg for rx, msg in GENERAL if re.search(rx, joined)]
    bad = list(item.get("bad", []))
    ok = any(has(a, tk) for a in item.get("answers", []))
    hit = next((b for b in bad if has(b, tk)), None)
    if hit:
        return out(MAL, f"Quedó el error: \"{hit}\". {rule}")
    if ok:
        if gen:
            return out(CASI, "La parte del ejercicio está bien, pero hay otro error: " + gen[0])
        return out(BIEN, "Correcto.")
    if gen:
        return out(MAL, gen[0])
    return out(MAL, f"No encontré la forma esperada ({item['answers'][0]}). Fijate en el modelo.")


def items():
    out = []
    for pid, kind, prompt, model, answers, bad, rule, escribir in P:
        d = {"id": f"pos-{pid}", "nivel": 4, "tema": "pos", "tags": ["pos"], "kind": kind, "rule": rule,
             "prompt": prompt, "model": model, "answers": answers, "bad": bad}
        if kind == "x":
            d["wrong"] = re.sub(r"\s*\([^)]*\)\s*$", "", prompt)
        if escribir:
            d["escribir"] = True
        out.append(d)
    return out
