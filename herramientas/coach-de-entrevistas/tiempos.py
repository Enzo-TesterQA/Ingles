#!/usr/bin/env python3
"""Coach de tiempos verbales: respuestas de una oración, calificadas en el momento.

Es un modo del coach de entrevistas (usa el mismo micrófono, el mismo Whisper y la
misma instalación). El programa te pide una oración en un tiempo verbal, la decís en
voz alta y te dice si el tiempo está bien (BIEN / CASI / MAL), con la regla en una
línea y una oración modelo. Al final de la serie guarda todo en un .txt de preguntas
y respuestas, listo para pegarle a Claude.

Uso:
  iniciar.bat --tiempos              (o practicar-tiempos.bat)
  python coach.py --tiempos --texto  escribís en vez de hablar
  python tiempos.py --probar "I have fixed the bug yesterday."   prueba el detector
"""
import csv
import datetime as dt
import difflib
import json
import os
import random
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
import coach as C  # noqa: E402  (coach.py se registra como "coach" antes de importarnos)

DATA = HERE / "tiempos.json"
OUT = C.SESSIONS / "tiempos"
HISTORY = OUT / "historial-tiempos.csv"
SERIES = 10

NAMES = {
    "ps": "Present Simple", "pc": "Present Continuous", "pp": "Present Perfect",
    "ppc": "Present Perfect Continuous", "past": "Past Simple", "pastc": "Past Continuous",
    "pastp": "Past Perfect", "pastpc": "Past Perfect Continuous", "will": "Futuro con will",
    "goingto": "Futuro con going to", "futc": "Future Continuous", "futp": "Future Perfect",
    "futpc": "Future Perfect Continuous", "usedto": "Used to", "would": "Would",
}
ORDER = list(NAMES)
FORM = {
    "ps": "Present Simple: verbo base (I test) y con he/she/it + s (it runs). Rutinas, hechos y cómo funciona algo.",
    "pc": "Present Continuous: am/is/are + -ing (I'm testing). Algo en curso ahora o en este período.",
    "pp": "Present Perfect: have/has + participio (I've automated). Experiencia o resultado hasta hoy, sin fecha terminada.",
    "ppc": "Present Perfect Continuous: have/has been + -ing (I've been working). Duración de algo que sigue.",
    "past": "Past Simple: verbo en pasado (I fixed, I wrote). Algo terminado, en un momento del pasado.",
    "pastc": "Past Continuous: was/were + -ing (I was testing). La acción de fondo cuando pasó otra cosa.",
    "pastp": "Past Perfect: had + participio (I had reported). Lo que pasó antes de otro pasado.",
    "pastpc": "Past Perfect Continuous: had been + -ing (I had been working). Duración hasta un momento del pasado.",
    "will": "Will + verbo base (I'll check). Decisiones en el momento, promesas y predicciones.",
    "goingto": "Am/is/are going to + verbo base (I'm going to test). Planes ya decididos.",
    "futc": "Will be + -ing (I'll be deploying). Algo en curso en un momento del futuro.",
    "futp": "Will have + participio (I'll have finished). Terminado antes de un momento del futuro.",
    "futpc": "Will have been + -ing (I'll have been working). Duración hasta un momento del futuro.",
    "usedto": "Used to + verbo base (I used to test manually). Hábitos o estados del pasado que ya no siguen.",
    "would": "Would + verbo base. Hábitos repetidos en una historia del pasado, o condicional.",
}
APUNTE = {"ps": "L1", "pc": "L2", "past": "L4", "pp": "L5-L7", "ppc": "L8-L9", "pastc": "L10", "pastp": "L11",
          "pastpc": "L12", "will": "L13", "goingto": "L13", "futc": "L14", "futp": "L14", "futpc": "L14",
          "usedto": "L15", "would": "L15"}

# ---------------------------------------------------------------- verbos

IRREGULAR = """be was been|become became become|begin began begun|break broke broken|bring brought brought|
build built built|buy bought bought|catch caught caught|choose chose chosen|come came come|cost cost cost|
cut cut cut|deal dealt dealt|do did done|draw drew drawn|drive drove driven|eat ate eaten|fall fell fallen|
feel felt felt|fight fought fought|find found found|fly flew flown|forget forgot forgotten|get got gotten|
give gave given|go went gone|grow grew grown|have had had|hear heard heard|hide hid hidden|hit hit hit|
hold held held|keep kept kept|know knew known|lead led led|learn learnt learnt|leave left left|lend lent lent|
let let let|lose lost lost|make made made|mean meant meant|meet met met|pay paid paid|put put put|quit quit quit|
read read read|ride rode ridden|ring rang rung|rise rose risen|run ran run|say said said|see saw seen|
seek sought sought|sell sold sold|send sent sent|set set set|shake shook shaken|show showed shown|shut shut shut|
sing sang sung|sit sat sat|sleep slept slept|speak spoke spoken|spend spent spent|split split split|
spread spread spread|stand stood stood|steal stole stolen|stick stuck stuck|swim swam swum|take took taken|
teach taught taught|tell told told|think thought thought|throw threw thrown|understand understood understood|
wake woke woken|wear wore worn|win won won|write wrote written|rebuild rebuilt rebuilt|rerun reran rerun|
rewrite rewrote rewritten|undo undid undone|overcome overcame overcome|mislead misled misled|
withdraw withdrew withdrawn|forgive forgave forgiven|freeze froze frozen|bite bit bitten|hang hung hung|
light lit lit|feed fed fed|bleed bled bled|breed bred bred|bet bet bet|burst burst burst|shoot shot shot|
dig dug dug|sweep swept swept|weep wept wept|lay laid laid|tear tore torn|bear bore born|forecast forecast forecast"""
IRR = {}
for chunk in IRREGULAR.replace("\n", "").split("|"):
    b, p, pp = chunk.split()
    IRR[b] = (p, pp)
IRR_PAST = {p: b for b, (p, _) in IRR.items()}
IRR_PART = {pp: b for b, (_, pp) in IRR.items()}
IRR_PART.update({"gotten": "get", "got": "get", "learned": "learn"})

REGULAR = """accept add adopt affect agree allow analyze apply approve arrive ask assign attach attend automate
avoid block book call cancel change check clean click close code collect commit compare complete configure
connect contain continue copy cover crash create debug decide define delay delete deliver depend deploy
describe design detect develop discover discuss document download drop email enjoy ensure estimate evaluate
explain export extract fail fix focus follow handle happen hate help identify implement import improve include
increase inform install integrate introduce investigate join jump kill launch like list listen live load
log look love maintain manage mark measure merge migrate miss mock monitor move need notice notify open
order organize own pass pick plan play prefer prepare present prevent print prioritize process produce
promote provide publish push raise reach receive record reduce refactor refer release remember remove repeat
replace reply report request require reset resolve rest restart retry return reuse review roll save
schedule script search seem select share ship sign skip solve sort start stay stop store study submit
suggest support switch talk test track train transform travel trigger try turn update upgrade upload use
validate verify visit wait walk want watch work worry""".split()
BASE = set(REGULAR) | set(IRR)

PRONOUNS = {"i", "you", "we", "they", "he", "she", "it"}
SUBJ = PRONOUNS | {"there", "this", "that", "someone", "somebody", "everyone", "everybody", "nobody", "who",
                   "people", "everything", "nothing", "something"}
SUBJ3 = {"he", "she", "it", "this", "that", "someone", "somebody", "everyone", "everybody", "nobody", "who",
         "everything", "nothing", "something"}
DET = {"a", "an", "the", "my", "our", "your", "their", "his", "her", "its", "this", "that", "these", "those",
       "some", "any", "every", "each", "all", "no", "more", "most", "many", "few", "several", "other", "two",
       "three", "of", "and", "or", "very", "well", "fully", "already", "partially", "manually", "automatically"}
ADV = {"not", "never", "already", "just", "also", "always", "recently", "ever", "still", "really", "usually",
       "often", "sometimes", "normally", "finally", "actually", "probably", "definitely", "only", "even", "mostly",
       "generally", "rarely", "again", "currently", "both", "all", "basically", "mainly", "typically", "first",
       "then", "now", "almost", "totally", "fully", "once", "certainly", "surely", "personally", "hardly"}
MODALS = {"can", "could", "should", "must", "might", "may", "shall", "ought"}
FUNCTION = ADV | MODALS | DET | {"to", "in", "on", "at", "for", "with", "by", "from", "as", "so", "but", "if",
                                 "because", "when", "while", "yes", "no", "am", "is", "are", "was", "were", "be",
                                 "been", "being", "have", "has", "had", "do", "does", "did", "will", "would",
                                 "i", "you", "we", "they", "he", "she", "it", "me", "us", "them", "him",
                                 "about", "here", "there", "what", "which", "who",
                                 "how", "where", "why", "too", "okay", "ok", "um", "uh", "eh", "hmm", "well",
                                 "sure", "sorry", "please", "thanks", "again", "yeah"}
NOT_ED = C.NOT_PAST_ED | {"embed", "need", "speed", "feed", "red", "bed", "shed", "hundred", "seed", "proceed",
                          "succeed", "exceed", "led", "wed", "ted", "fed"}


def is_ing(w):
    return len(w) > 4 and w.endswith("ing") and w not in C.ING_NOT_VERB and w not in {"during", "anything"}


def ed_form(w):
    return w.endswith("ed") and len(w) >= 4 and w not in NOT_ED


def is_past_form(w):
    return w in IRR_PAST or ed_form(w) or w in ("led", "fed")


def is_part(w):
    return w in IRR_PART or ed_form(w) or w in ("led", "fed")


def third(b):
    if b.endswith(("s", "sh", "ch", "x", "z", "o")):
        return b + "es"
    if b.endswith("y") and b[-2:-1] not in "aeiou":
        return b[:-1] + "ies"
    return b + "s"


# verbos que también son sustantivos comunes en QA (it is a test / the main change is process)
NOUNISH = {"test", "release", "plan", "change", "process", "fix", "work", "start", "report", "review", "update",
           "deploy", "build", "merge", "script", "log", "record", "order", "mark", "list", "load", "need", "help"}
SUBJ_NOUNS = {"team", "pipeline", "app", "system", "suite", "framework", "tool", "company", "client", "manager",
              "developer", "server", "api", "agent", "page", "job", "product", "owner", "environment", "service",
              "bot", "dashboard", "tester", "engineer", "database", "backend", "frontend", "platform"}
BASE3 = {third(b): b for b in BASE}
BASE3.update({"has": "have", "does": "do", "goes": "go", "is": "be"})


def bad_irregular(w):
    """writed, catched, buyed... -> (base, pasado, participio)"""
    if not w.endswith("ed"):
        return None
    for cand in (w[:-2], w[:-1], w[:-3] if len(w) > 5 and w[-3] == w[-4] else None):
        if cand and cand in IRR and cand not in ("learn", "show"):
            return cand, IRR[cand][0], IRR[cand][1]
    return None


# ---------------------------------------------------------------- texto

S_HAS = {"been", "got", "gotten"} | (set(IRR_PART) - set(IRR_PAST)) | {"already", "just", "never", "always", "ever"}


def expand(text):
    t = C.normalize(text).lower()
    t = re.sub(r"(?:^|,)\s*(?:you know|i mean)\s*,", ",", t)  # muletillas, no verbos
    t = re.sub(r"\bgonna\b", "going to", t)
    t = re.sub(r"\bwanna\b", "want to", t)
    t = re.sub(r"\bwon't\b", "will not", t)
    t = re.sub(r"\bcan't\b", "can not", t)
    t = re.sub(r"\bshan't\b", "shall not", t)
    t = re.sub(r"\bain't\b", "is not", t)
    t = re.sub(r"(\w)n't\b", r"\1 not", t)
    t = re.sub(r"\bi'm\b", "i am", t)
    t = re.sub(r"'re\b", " are", t)
    t = re.sub(r"'ve\b", " have", t)
    t = re.sub(r"'ll\b", " will", t)
    t = re.sub(r"\blet's\b", "let us", t)

    def d(m):
        nxt = m.group(2)
        if nxt == "better":
            return m.group(1) + " had " + nxt
        if nxt in ("been", "already", "just", "never") or (is_part(nxt) and nxt not in BASE):
            return m.group(1) + " had " + nxt
        return m.group(1) + " would " + nxt
    t = re.sub(r"\b(\w+)'d\s+(\w+)", d, t)

    def s(m):
        nxt = m.group(2)
        if nxt in S_HAS:
            return m.group(1) + " has " + nxt
        return m.group(1) + " is " + nxt
    t = re.sub(r"\b(it|he|she|that|there|what|who|here|where|everything|nothing|something|this)'s\s+(\w+)", s, t)
    t = re.sub(r"'s\b", "", t)  # posesivos: the team's -> the team
    return t


def tokens(text):
    return re.findall(r"[a-z]+|\d+", expand(text))


def words_display(toks, a, b):
    return " ".join(toks[max(0, a):b])


# ---------------------------------------------------------------- detector

def detect(text):
    """Devuelve (tiempos encontrados en orden, avisos). Cada aviso: (código, fragmento, explicación)."""
    toks = tokens(text)
    n = len(toks)
    used = [False] * n
    found, flags = [], []

    def tok(j):
        return toks[j] if 0 <= j < n else ""

    def skip(j):
        while tok(j) in ADV:
            j += 1
        return j

    def add(label, a, b):
        for k in range(a, min(b, n)):
            used[k] = True
        if label and label not in found:
            found.append(label)

    def flag(code, a, b, msg):
        flags.append((code, words_display(toks, a, b), msg))

    i = 0
    while i < n:
        w = toks[i]
        if used[i]:
            i += 1
            continue
        if w in ("will", "shall"):
            j = skip(i + 1)
            if tok(j) in SUBJ and tok(i - 1) not in SUBJ:
                j = skip(j + 1)
            if tok(j) == "have" and tok(j + 1) == "been" and is_ing(tok(j + 2)):
                add("futpc", i, j + 3)
            elif tok(j) == "have" and is_part(tok(j + 1)):
                add("futp", i, j + 2)
            elif tok(j) == "be" and is_ing(tok(j + 1)):
                add("futc", i, j + 2)
            elif is_ing(tok(j)):
                flag("modal_ing", i, j + 1, "Después de will va el verbo base (I'll work) o be + -ing (I'll be working).")
                add("will", i, j + 1)
            elif tok(j):
                add("will", i, j + 1)
        elif w == "would":
            j = skip(i + 1)
            if tok(j) in SUBJ and tok(i - 1) not in SUBJ:
                j = skip(j + 1)
            add("would", i, j + 1)
        elif w in MODALS:
            j = skip(i + 1)
            if tok(j) in SUBJ and tok(i - 1) not in SUBJ:
                j = skip(j + 1)
            if is_ing(tok(j)):
                flag("modal_ing", i, j + 1, f"Después de {w} va el verbo base: {w} {tok(j)[:-3]}...")
            add(None, i, j + 1)
        elif w == "used" and tok(i + 1) == "to":
            if tok(i - 1) in ("am", "is", "are", "was", "were", "be", "get", "got", "getting", "been"):
                add(None, i, i + 3)  # be used to + -ing: no es used to de hábito
                if not is_ing(tok(i + 2)) and tok(i + 2) in BASE:
                    flag("used_to_ing", i - 1, i + 3, "Be used to (estar acostumbrado) va con -ing: I'm used to working.")
            elif is_ing(tok(i + 2)):
                flag("used_to_ing2", i, i + 3, "Used to (antes hacía) va con verbo base: I used to work.")
                add("usedto", i, i + 3)
            else:
                if is_past_form(tok(i + 2)) and tok(i + 2) not in BASE:
                    flag("used_to_past", i, i + 3, f"Después de used to va el verbo base: used to {base_of(tok(i + 2))}.")
                add("usedto", i, i + 3)
        elif w == "use" and tok(i + 1) == "to" and (tok(i - 1) in ("did", "not") or tok(i - 2) == "did"):
            add("usedto", i, i + 3)
        elif w == "use" and tok(i + 1) == "to" and tok(i - 1) in PRONOUNS and tok(i + 2) in BASE:
            flag("use_to", i - 1, i + 3, "Para un hábito del pasado va used to (con d): I used to work...")
            add(None, i, i + 3)
        elif w == "had":
            j = skip(i + 1)
            if tok(j) in SUBJ and tok(i - 1) not in SUBJ:
                j = skip(j + 1)
            if tok(j) == "been" and is_ing(tok(j + 1)):
                add("pastpc", i, j + 2)
            elif tok(j) == "been" or (is_part(tok(j)) and tok(j) != "to"):
                add("pastp", i, j + 1)
            else:
                add("past", i, i + 1)  # had como verbo principal: I had a meeting
        elif w in ("have", "has"):
            prev = tok(i - 1)
            if prev in {"will", "would", "to"} | MODALS:
                i += 1
                continue
            j = skip(i + 1)
            if tok(j) in SUBJ and prev not in SUBJ:
                j = skip(j + 1)
            nxt = tok(j)
            if nxt == "been" and is_ing(tok(j + 1)):
                add("ppc", i, j + 2)
            elif nxt == "been":
                add("pp", i, j + 1)
            elif nxt and is_part(nxt) and nxt not in ("to",):
                bi = bad_irregular(nxt)
                if bi:
                    flag("bad_irregular", j, j + 1, f"{bi[0]} es irregular: el participio es {bi[2]}, no {nxt}.")
                add("pp", i, j + 1)
            elif nxt in IRR_PAST and IRR_PAST[nxt] in IRR and IRR[IRR_PAST[nxt]][1] != nxt:
                b = IRR_PAST[nxt]
                flag("have_past", i, j + 1, f"Después de have va el participio: {b}, {nxt}, {IRR[b][1]} -> have {IRR[b][1]}.")
                add("pp", i, j + 1)
            elif nxt in BASE and nxt not in IRR_PART and (prev in SUBJ or prev == "") and \
                    tok(j + 1) not in ("to", "a", "an", "the", "some", "any", "no", "many", "much", "lots", "experience"):
                flag("have_base", i, j + 1, f"Después de have/has va el participio: have {participle(nxt)}.")
                add(None, i, j + 1)
            else:
                add("ps", i, i + 1)  # have como verbo principal: I have a meeting / I have to...
        elif w == "did":
            j = skip(i + 1)
            if tok(j) in SUBJ and tok(i - 1) not in SUBJ:
                j = skip(j + 1)
            if tok(j) in ("use", "used") and tok(j + 1) == "to":
                if tok(j) == "used":
                    flag("did_used", i, j + 2, "Con did/didn't va use to, sin d: didn't use to.")
                add("usedto", i, j + 3)
                i += 1
                continue
            if is_past_form(tok(j)) and tok(j) not in BASE:
                flag("did_past", i, j + 1, f"Después de did va el verbo base: did {base_of(tok(j))}.")
            add("past", i, j + 1 if tok(j) in BASE or is_past_form(tok(j)) else i + 1)
        elif w in ("do", "does"):
            if tok(i - 1) in {"will", "would", "to", "did"} | MODALS:
                i += 1
                continue
            j = skip(i + 1)
            if tok(j) in SUBJ and tok(i - 1) not in SUBJ:
                j = skip(j + 1)
            if tok(j).endswith("s") and tok(j) in BASE3 and w == "does":
                flag("does_s", i, j + 1, f"Después de does/doesn't va el verbo sin -s: does {BASE3[tok(j)]}.")
            add("ps", i, j + 1 if tok(j) in BASE or tok(j) in BASE3 else i + 1)
        elif w in ("am", "is", "are"):
            j = skip(i + 1)
            if tok(j) in SUBJ and tok(i - 1) not in SUBJ:
                j = skip(j + 1)
            nxt = tok(j)
            if nxt == "going" and tok(j + 1) == "to" and tok(j + 2) not in DET | {"office", "bed", "school"}:
                add("goingto", i, j + 3)
                if tok(j + 2) == "be" and is_ing(tok(j + 3)):
                    used[j + 3] = True
            elif is_ing(nxt):
                add("pc", i, j + 1)
            elif nxt in BASE and nxt not in IRR_PART and nxt != "agree" and tok(j - 1) != "not" and (
                    tok(i - 1) in ("i", "we", "they", "you") or (tok(i - 1) in SUBJ and nxt not in NOUNISH)):
                flag("be_base", i, j + 1, f"Con am/is/are va -ing: {w} {ing_of(nxt)} (o sacá el {w}: I {nxt}).")
                add(None, i, j + 1)
            else:
                add("ps", i, i + 1)  # be en presente: I am a QA / it is tested
        elif w in ("was", "were"):
            j = skip(i + 1)
            if tok(j) in SUBJ and tok(i - 1) not in SUBJ:
                j = skip(j + 1)
            if tok(j) == "going" and tok(j + 1) == "to":
                add("past", i, j + 3)
            elif is_ing(tok(j)):
                add("pastc", i, j + 1)
            else:
                add("past", i, i + 1)
        elif w == "been" and tok(i - 1) in PRONOUNS:
            flag("no_have", i - 1, i + 2, f"Falta have (o no se escuchó el 've): {tok(i - 1)} have been...")
            add(None, i, i + 2 if is_ing(tok(i + 1)) else i + 1)
        elif w == "going" and tok(i + 1) == "to" and tok(i - 1) in PRONOUNS:
            flag("no_be_going", i - 1, i + 3, f"Going to necesita am/is/are (o no se escuchó el 'm/'re): {be_for(tok(i - 1))} going to...")
            add(None, i, i + 3)
        elif is_ing(w) and tok(i - 1) in PRONOUNS:
            flag("no_be", i - 1, i + 1, f"El continuo necesita am/is/are (o no se escuchó el 'm/'re): {be_for(tok(i - 1))} {w}.")
            add(None, i, i + 1)
        elif bad_irregular(w) and tok(i - 1) not in DET:
            b, p, pp = bad_irregular(w)
            flag("bad_irregular", i, i + 1, f"{b} es irregular: {b}, {p}, {pp}. No existe {w}.")
            add("past", i, i + 1)
        elif is_past_form(w) and past_context(toks, i, found):
            add("past", i, i + 1)
            if tok(i - 1) in PRONOUNS or (tok(i - 1) in ADV and tok(i - 2) in PRONOUNS):
                used[i] = True
                if is_part(w):
                    flags.append(("pron_part", words_display(toks, i - 1, i + 1), w))
        elif tok(i - 1) in PRONOUNS - {"he", "she", "it"} or (tok(i - 1) in ADV and tok(i - 2) in PRONOUNS - {"he", "she", "it"}):
            if w not in FUNCTION and not w.isdigit() and not is_ing(w):
                add("ps", i, i + 1)
                if tok(i - 1) in PRONOUNS and w in BASE:
                    flags.append(("pron_base", words_display(toks, i - 1, i + 1), w))
        elif w in BASE3 and w not in ("is", "has", "does") and (
                tok(i - 1) in SUBJ3 or (tok(i - 2) in DET and tok(i - 1) not in FUNCTION)
                or (tok(i - 1) in ADV and tok(i - 2) in SUBJ3) or tok(i - 1) in ("which", "that", "who")
                or (tok(i - 1) in ("and", "or") and found and found[-1] == "ps")
                or (not any(used[:i]) and tok(i - 1) not in FUNCTION and not verb_form(tok(i - 1)))):
            add("ps", i, i + 1)
        elif (tok(i - 1) in ("he", "she", "it") or (tok(i - 1) in SUBJ_NOUNS and tok(i - 2) in DET and not found)) \
                and w in BASE and w not in BASE3 and w not in FUNCTION:
            flag("no_s", i - 1, i + 1, f"Con he/she/it el presente lleva -s: {tok(i - 1)} {third(w)}.")
            add("ps", i, i + 1)
        i += 1
    return found, flags


def verb_form(x):
    return x in BASE or x in BASE3 or is_past_form(x) or is_ing(x)


PAST_PREV = {"and", "or", "then", "but", "so", "because", "when", "while", "before", "after", "yesterday", "ago",
             "week", "month", "year", "sprint", "night", "morning", "once", "until"}


def past_context(toks, i, found):
    """¿Esta forma en -ed / irregular es un verbo en pasado (y no un adjetivo como automated tests)?"""
    prev = toks[i - 1] if i else ""
    prev2 = toks[i - 2] if i > 1 else ""
    w = toks[i]
    if prev in SUBJ or prev in ADV:
        return True
    if prev in DET - {"and", "or"} or prev in ("to", "be", "being", "get", "got"):
        return False
    if w in BASE and w in IRR_PAST:  # read, put, cut, let: igual en presente; sin sujeto no sabemos
        return False
    if prev in PAST_PREV:
        return True
    if prev in FUNCTION:
        return False
    if w in IRR_PAST and w not in IRR_PART:  # took, broke, wrote: siempre son verbos
        return True
    if verb_form(prev) and prev2 not in DET:
        return False  # I wrote automated tests: automated es adjetivo
    return True


def base_of(w):
    if w in IRR_PAST:
        return IRR_PAST[w]
    if w in IRR_PART:
        return IRR_PART[w]
    if w.endswith("ied"):
        return w[:-3] + "y"
    if w.endswith("ed"):
        stem = w[:-2]
        if len(stem) > 2 and stem[-1] == stem[-2] and stem[-1] not in "ls":
            return stem[:-1]
        return stem if stem in BASE else (stem + "e" if stem + "e" in BASE else stem)
    return w


def participle(b):
    if b in IRR:
        return IRR[b][1]
    if b.endswith("e"):
        return b + "d"
    if b.endswith("y") and b[-2:-1] not in "aeiou":
        return b[:-1] + "ied"
    if b in ("stop", "plan", "ship", "drop", "skip", "debug", "commit", "prefer", "refer", "log", "plug", "submit"):
        return b + b[-1] + "ed"
    return b + "ed"


def ing_of(b):
    if b.endswith("ie"):
        return b[:-2] + "ying"
    if b.endswith("e") and b not in ("be", "see", "agree"):
        return b[:-1] + "ing"
    if b in ("run", "stop", "plan", "ship", "drop", "skip", "debug", "commit", "get", "put", "set", "cut", "sit",
             "begin", "swim", "win", "log", "submit", "hit", "let", "split", "forget", "refer", "prefer"):
        return b + b[-1] + "ing"
    return b + "ing"


def be_for(p):
    return {"i": "I'm", "he": "he's", "she": "she's", "it": "it's"}.get(p, p + "'re")


# ---------------------------------------------------------------- calificar

BIEN, CASI, MAL = "bien", "casi", "mal"
DURATION = re.compile(r"\bsince\s+(?:\d+|last|then|this|yesterday|monday|tuesday|wednesday|thursday|friday|january|"
                      r"february|march|april|may|june|july|august|september|october|november|december|i|we|the)\b"
                      r"|\bfor\s+(?:the\s+(?:last|past)\s+)?(?:more\s+than\s+|about\s+|almost\s+)?(?:\d+|a|an|one|two|"
                      r"three|four|five|six|seven|eight|nine|ten|several|many|a\s+few)\s+(?:years?|months?|weeks?|days?|"
                      r"hours?|minutes?|while)\b|\bfor (?:ages|a long time|so long|long)\b|\ball (?:day|morning|afternoon|week|night)\b")
SHORT_RX = re.compile(r"^(?:yes|no|yeah|nope|sure)[\s,]*(?:i|we|it|they|he|she|you)\s+(?:have|has|did|do|does|am|is|"
                      r"are|was|were|will|had|would)(?:\s+not)?\s*$")
# avisos que cuentan como "casi" según el tiempo que pide la consigna
NEAR = {
    "pp": {"have_base", "have_past", "no_have"}, "ppc": {"no_have", "have_base"},
    "pastp": set(), "pastpc": set(),
    "pc": {"no_be", "be_base"}, "goingto": {"no_be_going"}, "pastc": set(),
    "will": {"modal_ing"}, "futc": {"modal_ing"}, "futp": set(), "futpc": set(),
    "usedto": {"use_to", "used_to_ing2", "used_to_past"},
    "past": {"bad_irregular", "did_past"}, "ps": {"no_s", "does_s"},
}
# avisos que siempre son error de forma (si el tiempo está bien, quedás en "casi")
ALWAYS = {"if_will", "did_used", "modal_ing", "bad_irregular", "did_past", "does_s", "have_past", "have_base", "be_base", "used_to_ing",
          "used_to_ing2", "used_to_past", "no_s", "no_be", "no_be_going", "no_have", "use_to"}


def phrase_in(phrase_toks, toks):
    k = len(phrase_toks)
    return k > 0 and any(toks[i:i + k] == phrase_toks for i in range(len(toks) - k + 1))


def tense_rule_errors(text):
    return [e for e in C.check_grammar(text) if e["tipo"] == "tiempo"]


def target_of(item):
    if item["nivel"] == 2:
        return item["t"]
    if item.get("target"):
        return item["target"]
    if item.get("answers"):
        a = item["answers"][0]
        probes = [a, "it " + a, "they " + a]
    else:
        probes = [item["model"]]
    founds = [detect(p)[0] for p in probes]
    pick = next((f for fs in founds for f in fs if f in item["tags"]), None) \
        or next((fs[0] for fs in founds if fs), item["tags"][0])
    if pick == "would" and "usedto" in item["tags"]:
        pick = "usedto"
    item["target"] = pick
    return pick


def x_regions(item):
    """Para "corregí el error": qué fragmentos tiene que tener tu versión y cuál era el error."""
    wrong, right = tokens(item["wrong"]), tokens(item["model"])
    need, bad = [], []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(a=wrong, b=right, autojunk=False).get_opcodes():
        if op == "equal":
            continue
        if j2 > j1:
            need.append(right[max(0, j1 - 1):j2] if j2 - j1 == 1 else right[j1:j2])
        if i2 > i1:
            bad.append(wrong[max(0, i1 - 1):i2] if i2 - i1 == 1 else wrong[i1:i2])
        elif j2 > j1:
            bad.append(wrong[max(0, i1 - 1):i1 + 1])
    return need, bad


def grade(item, said):
    """-> dict(veredicto, motivo, regla, tiempos, avisos)"""
    target = target_of(item)
    toks = tokens(said)
    found, flags = detect(said)
    errs = tense_rule_errors(said)
    m = re.search(r"\bif (?:the \w+|i|we|you|they|he|she|it) will\b", " ".join(toks))
    if m:
        flags.append(("if_will", m.group(0), "Después de if va presente, no will: if the deploy fails, I'll..."))
    rule = item.get("rule") or FORM[target]
    res = {"tiempos": found, "objetivo": target, "regla": rule, "avisos": flags, "errores": errs}
    accepted = {target} | set(item.get("alt", []))
    if target == "usedto" and item["nivel"] == 1:
        accepted.add("would")
    duration_alt = None
    if target in ("pp", "ppc") and DURATION.search(" ".join(toks)):
        duration_alt = "ppc" if target == "pp" else "pp"  # con for/since valen los dos
        if target == "ppc" or item.get("wrong") or len(item.get("answers", [])) > 1:
            accepted.add(duration_alt)
    form_flags = [f for f in flags if f[0] in ALWAYS]
    wrong_time = [e for e in errs if e["id"] in ("T-FINISHED", "T-SINCE", "T-AGO")]

    def out(v, why):
        res["veredicto"], res["motivo"] = v, why
        return res

    if not toks:
        return out(MAL, "No escuché ninguna oración.")
    if SHORT_RX.match(" ".join(toks)) or len(toks) < 3:
        return out(CASI, "Respondé con una oración completa, no solo Yes, I have. En la entrevista suma mucho más.")

    if item["nivel"] == 1 and item.get("answers"):
        for a in item["answers"]:
            if phrase_in(tokens(a), toks) and (target in found or not found or accepted & set(found)):
                if form_flags or errs:
                    msg = form_flags[0][2] if form_flags else errs[0]["regla"]
                    return out(CASI, "La parte del ejercicio está bien, pero hay otro error: " + msg)
                return out(BIEN, f"Correcto: {a}.")
    if item["nivel"] == 1 and item.get("wrong"):
        need, bad = x_regions(item)
        if all(phrase_in(p, toks) for p in need) and not any(phrase_in(b, toks) for b in bad if b):
            return out(BIEN, "Corregiste el error.")
        if bad and any(b and phrase_in(b, toks) for b in bad):
            return out(MAL, "Repetiste el error de la oración original: " + " ".join(next(b for b in bad if b and phrase_in(b, toks))) + ".")

    hit = accepted & set(found)
    if hit and wrong_time:
        return out(MAL, wrong_time[0]["regla"])
    if hit:
        if item.get("need") and not re.search(item["need"], " ".join(toks)):
            return out(CASI, item["need_msg"])
        if item.get("avoid") and re.search(item["avoid"], " ".join(toks)):
            return out(CASI, item["avoid_msg"])
        if form_flags:
            return out(CASI, form_flags[0][2])
        if errs:
            return out(CASI, errs[0]["regla"])
        if item["nivel"] == 1 and duration_alt in hit and target not in found:
            return out(BIEN, f"También está bien con {NAMES[duration_alt]}. El modelo usa {NAMES[target]}.")
        if item["nivel"] == 1:
            exp = item.get("answers", [None])[0] or item["model"]
            return out(CASI, f"El tiempo está bien ({NAMES[target]}), pero la forma esperada era: {exp}.")
        return out(BIEN, f"{NAMES[target]} bien usado.")

    near = [f for f in flags if f[0] in NEAR.get(target, set())]
    if near:
        return out(CASI, near[0][2])
    if wrong_time:
        return out(MAL, wrong_time[0]["regla"])
    # ¿Whisper se comió el 've / 'll? Solo si el verbo es el de la consigna o el modelo.
    ref = set(tokens(item["model"] + " " + (item.get("q") or item.get("prompt") or "")))
    ref |= {base_of(w) for w in ref}
    dropped = [f for f in flags if f[0] == "pron_part" and (f[2] in ref or base_of(f[2]) in ref)]
    if target == "pp" and "past" in found and C.FINISHED_RX.search(said):
        return out(CASI, "Con una fecha terminada (last year, in 2022) el pasado está bien, pero esta consigna "
                         "practica Present Perfect: sacá la fecha y usá have + participio.")
    if target in ("pp", "pastp") and dropped:
        aux = "'ve" if target == "pp" else "'d"
        return out(CASI, f"Escuché \"{dropped[0][1]}\" (Past Simple). Si dijiste {aux} {dropped[0][2]}, "
                         f"marcalo más fuerte o decí {'have' if target == 'pp' else 'had'} completo.")
    pb = [f for f in flags if f[0] == "pron_base" and f[2] in ref]
    if target in ("will", "futc", "futp", "futpc") and pb:
        return out(CASI, f"Escuché \"{pb[0][1]}\" (presente). Si dijiste 'll, marcalo más (o decí will completo).")
    used = ", ".join(NAMES[f] for f in found) if found else "ningún verbo conjugado que yo reconozca"
    return out(MAL, f"Usaste {used}; esta consigna pide {NAMES[target]}.")


# ---------------------------------------------------------------- pantalla

FANCY = os.name != "nt" or bool(os.environ.get("WT_SESSION")) or os.environ.get("TERM_PROGRAM") == "vscode"
LABEL = {BIEN: ("✅ BIEN" if FANCY else "[BIEN]", C.ok), CASI: ("⚠️  CASI" if FANCY else "[CASI]", C.warn),
         MAL: ("❌ MAL" if FANCY else "[MAL] ", C.bad)}
PLAIN = {BIEN: "BIEN", CASI: "CASI", MAL: "MAL"}


def show_prompt(item, k, total, level):
    target = target_of(item)
    print()
    head = f"{k}/{total}"
    if level != 3:
        head += f" · {NAMES[target]}"
    print(C.rule_line(head))
    if item["nivel"] == 1:
        if item["kind"] == "x":
            print(C.dim("Corregí el error y decí la oración completa:"))
        elif item["kind"] == "c":
            print(C.dim("Decí la oración completa con la opción correcta:"))
        else:
            print(C.dim("Decí la oración completa, con el verbo conjugado:"))
    elif item["kind"] == "tr":
        print(C.dim("Transformá la oración y decila en voz alta:"))
    else:
        print(C.dim("Respondé con una oración" + (f" en {NAMES[target]}:" if level == 2 else ":")))
    print(C.bold(item.get("prompt") or item["q"]))


def show_result(item, said, res, level):
    label, color = LABEL[res["veredicto"]]
    print(f"\n  Escuché: {C.accent(said)}")
    if res["tiempos"]:
        print(C.dim("  Tiempos que detecté: " + ", ".join(NAMES[t] for t in res["tiempos"])))
    print(f"\n  {color(C.bold(label))}  {res['motivo']}")
    if res["veredicto"] != BIEN or level == 3:
        print(C.dim(f"  Regla: {res['regla']}"))
    print(f"  Modelo: {C.ok(item['model'])}")


# ---------------------------------------------------------------- audio

def record_sentence(max_seconds=20, auto=True):
    """Graba una oración. Corta sola después de ~2 s de silencio (o con Enter)."""
    sd = C.need("sounddevice", "sounddevice")
    np = C.need("numpy", "numpy")
    if not sd or not np:
        return None
    chunks, level = [], [0.0]

    def callback(indata, frames, t, status):
        chunks.append(indata[:, 0].copy())
        level[0] = float(np.sqrt(np.mean(indata[:, 0] ** 2)))

    if os.name == "nt":
        C.key_pressed()
    t0 = time.time()
    noise, spoke, last_voice = [], False, None
    try:
        with sd.InputStream(samplerate=C.SAMPLE_RATE, channels=1, dtype="float32", callback=callback):
            while True:
                el = time.time() - t0
                lv = level[0]
                if el < 0.5:
                    noise.append(lv)
                thr = max(0.012, (sum(noise) / len(noise) if noise else 0) * 3)
                if el >= 0.5 and lv > thr:
                    spoke, last_voice = True, el
                bar = "#" * min(20, int(lv * 160))
                state = "te escucho" if spoke else "hablá"
                sys.stdout.write(f"\r  {C.bad('REC')} {C.fmt_time(el)}  [{bar:<20}]  {state} · Enter para cortar ")
                sys.stdout.flush()
                if C.key_pressed():
                    break
                if auto and spoke and el - last_voice > 2.0:
                    break
                if el >= max_seconds:
                    break
                time.sleep(0.05)
    except Exception as e:
        print(C.bad(f"\nNo pude usar el micrófono: {e}"))
        print("Revisá que esté conectado y que Windows le dé permiso a las apps de escritorio "
              "(Configuración > Privacidad y seguridad > Micrófono).")
        return None
    print()
    audio = np.concatenate(chunks) if chunks else np.zeros(0, dtype="float32")
    if audio.size < C.SAMPLE_RATE // 2 or float(np.max(np.abs(audio))) < 0.01:
        print(C.warn("No se escuchó casi nada. Probá el micrófono desde el menú."))
        return None
    return audio


HALLUCINATIONS = {"thank you", "thanks for watching", "you", "bye", "thank you for watching", ""}


def transcribe_sentence(audio, model_name):
    model = C.load_model(model_name)
    if model is None:
        return None
    sys.stdout.write("  Transcribiendo... ")
    sys.stdout.flush()
    t0 = time.time()
    kw = dict(language="en", beam_size=5, condition_on_previous_text=False, without_timestamps=True)
    text = ""
    try:
        segments, _ = model.transcribe(audio, vad_filter=True, vad_parameters={"min_silence_duration_ms": 500}, **kw)
        text = " ".join(s.text.strip() for s in segments).strip()
    except Exception:
        pass
    if not text:  # sin filtro de silencios, por si el filtro se comió la frase
        try:
            segments, _ = model.transcribe(audio, **kw)
            text = " ".join(s.text.strip() for s in segments).strip()
        except Exception as e:
            print(C.bad(f"\nFalló la transcripción: {e}"))
            return None
    print(C.dim(f"({time.time() - t0:.1f} s)"))
    if re.sub(r"[^a-z ]", "", text.lower()).strip() in HALLUCINATIONS:
        return ""
    return text


# ---------------------------------------------------------------- historial y elección

FIELDS = ["fecha", "serie", "nivel", "id", "tiempo", "resultado", "dije", "corregido_a_mano", "modelo"]


def read_history():
    if not HISTORY.exists():
        return []
    with HISTORY.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def append_history(row):
    OUT.mkdir(parents=True, exist_ok=True)
    new = not HISTORY.exists()
    with HISTORY.open("a", encoding="utf-8-sig" if new else "utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)


def tense_stats(rows):
    by = defaultdict(list)
    for r in rows:
        by[r["tiempo"]].append(r["resultado"])
    return by


def score(results):
    pts = {BIEN: 1.0, CASI: 0.5, MAL: 0.0}
    last = results[-15:]
    return sum(pts.get(r, 0) for r in last) / len(last) if last else None


def pick_series(items, n, rows, tense=None, errors_only=False):
    last = {}
    seen = Counter()
    for r in rows:
        last[r["id"]] = r["resultado"]
        seen[r["id"]] += 1
    stats = tense_stats(rows)
    pool = [i for i in items if not tense or target_of(i) == tense]
    if errors_only:
        pool = [i for i in pool if last.get(i["id"]) in (MAL, CASI)]
    if not pool:
        return []
    weights = []
    for i in pool:
        t = target_of(i)
        s = score(stats.get(t, []))
        w = 1.0 + (1.5 if not seen[i["id"]] else 0) + (3 if last.get(i["id"]) == MAL else 0) \
            + (1.5 if last.get(i["id"]) == CASI else 0) + (2.5 * (1 - s) if s is not None else 0.5)
        weights.append(w / (1 + 0.3 * seen[i["id"]]))
    chosen, per_tense = [], Counter()
    cands = list(zip(pool, weights))
    while cands and len(chosen) < n:
        it, _ = random.choices(cands, weights=[w for _, w in cands])[0]
        cands = [(a, b) for a, b in cands if a is not it]
        t = target_of(it)
        if not tense and per_tense[t] >= 3 and any(target_of(a) != t for a, _ in cands):
            continue
        chosen.append(it)
        per_tense[t] += 1
    return chosen


# ---------------------------------------------------------------- serie

def ask_said(prompt="Escribí lo que dijiste (Enter para cancelar) > "):
    return C.ask(prompt)


def run_series(items, level, args, tense=None, errors_only=False):
    rows = read_history()
    if level == 1:
        pool = [i for i in items if i["nivel"] == 1]
    elif level == 2:
        pool = [i for i in items if i["nivel"] == 2]
    elif level == 3:
        pool = [i for i in items if i["nivel"] == 2 and i.get("mix")]
    else:
        pool = items
    n = args.cantidad or SERIES
    series = pick_series(pool, n, rows, tense, errors_only)
    if not series:
        print(C.warn("No hay ítems para esa selección todavía." + (" ¡No tenés errores pendientes!" if errors_only else "")))
        return
    stamp = dt.datetime.now()
    serie_id = stamp.strftime("%Y-%m-%d_%H%M%S")
    log = []
    print()
    print(C.dim("Decí una sola oración. La grabación corta sola cuando hacés silencio (o con Enter)."
                if not args.texto else "Escribí una sola oración y Enter."))
    k = 0
    while k < len(series):
        item = series[k]
        show_prompt(item, k + 1, len(series), level)
        spoken_q = item["nivel"] == 2 and item["kind"] == "q"
        if spoken_q and not args.sin_voz:
            C.speak(item["q"])
        audio, said, manual = None, None, False
        while said is None:
            if args.texto:
                said = C.ask("> ")
                if not said:
                    said = None
                    continue
                if said.lower() in ("s", "saltear"):
                    break
                if said.lower() in ("v", "0", "salir"):
                    k = len(series)
                    break
                continue
            op = C.ask(C.dim("\nEnter: grabar · r: repetir la consigna · t: escribir · s: saltear · v: terminar > ")).lower()
            if op == "r":
                if spoken_q:
                    C.speak(item["q"])
                show_prompt(item, k + 1, len(series), level)
                continue
            if op == "s":
                break
            if op in ("v", "0"):
                k = len(series)
                break
            if op == "t":
                said, manual = ask_said("Escribí tu oración > "), True
                said = said or None
                continue
            audio = record_sentence(auto=not args.sin_autocorte)
            if audio is None:
                continue
            said = transcribe_sentence(audio, args.modelo)
            if said is None:
                print("No pude transcribir. Escribí lo que dijiste:")
                said, manual = ask_said(), True
                said = said or None
            elif not said:
                print(C.warn("No entendí nada. Probá de nuevo, un poco más cerca del micrófono."))
                said = None
        if said is None:
            k += 1
            continue
        res = grade(item, said)
        show_result(item, said, res, level)
        while True:
            extra = " · e: escuchar tu audio" if audio is not None else ""
            op = C.ask(C.dim(f"\nEnter: siguiente · o: otra vez · c: no dije eso (corregir lo que escuchó){extra}"
                             f" · m: escuchar el modelo · v: terminar > ")).lower()
            if op == "e" and audio is not None:
                C.play(audio)
                continue
            if op == "m":
                C.speak(item["model"])
                continue
            if op == "c":
                fixed = ask_said("Escribí lo que dijiste en realidad > ")
                if fixed:
                    said, manual = fixed, True
                    res = grade(item, said)
                    show_result(item, said, res, level)
                continue
            break
        entry = {"item": item, "said": said, "res": res, "manual": manual}
        log.append(entry)
        append_history({"fecha": stamp.strftime("%Y-%m-%d %H:%M"), "serie": serie_id, "nivel": level, "id": item["id"],
                        "tiempo": res["objetivo"], "resultado": res["veredicto"], "dije": said,
                        "corregido_a_mano": "si" if manual else "", "modelo": item["model"]})
        if op == "o":
            continue  # la misma consigna de nuevo; el intento anterior queda guardado
        if op in ("v", "0"):
            break
        k += 1
    if log:
        finish(log, level, serie_id, stamp)


def finish(log, level, serie_id, stamp):
    cnt = Counter(e["res"]["veredicto"] for e in log)
    print()
    print(C.rule_line("Resultado de la serie"))
    print(f"  {C.ok(str(cnt[BIEN]) + ' bien')} · {C.warn(str(cnt[CASI]) + ' casi')} · {C.bad(str(cnt[MAL]) + ' mal')}"
          f"  de {len(log)}")
    bad = [e for e in log if e["res"]["veredicto"] != BIEN]
    if bad:
        print()
        print(C.bold("Para repasar"))
        for e in bad:
            print(f"  {LABEL[e['res']['veredicto']][0]:<9} {NAMES[e['res']['objetivo']]}: {e['said']}")
            print(C.dim(f"            -> {e['item']['model']}"))
        worst = Counter(e["res"]["objetivo"] for e in log if e["res"]["veredicto"] == MAL).most_common(1)
        if worst and worst[0][1] >= 2:
            t = worst[0][0]
            print(C.warn(f"\n  > Fallaste {worst[0][1]} veces en {NAMES[t]}. Repasá la lección {APUNTE.get(t, '')} "
                         f"del cuaderno y hacé otra serie con la opción 4."))
    text, chat = qa_text(log, level, stamp)
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{serie_id}_tiempos.txt"
    path.write_text(text, encoding="utf-8")
    print()
    if C.copy_to_clipboard(chat):
        print(C.ok("Copié las preguntas y tus respuestas. Pegalas en el chat del proyecto y Claude te las corrige."))
    else:
        print("Para el chat, copiá el bloque del final de este archivo.")
    print(C.dim(f"Guardado en sesiones/tiempos/{path.name}"))
    print(C.rule_line())


def qa_text(log, level, stamp):
    cnt = Counter(e["res"]["veredicto"] for e in log)
    lines = [f"Práctica de tiempos verbales · {stamp.strftime('%Y-%m-%d %H:%M')} · Nivel {level} · {len(log)} respuestas",
             f"Resultado del coach: {cnt[BIEN]} bien, {cnt[CASI]} casi, {cnt[MAL]} mal", ""]
    chat = ["Corregime esta serie de tiempos verbales (unidad 2). Son respuestas habladas de una oración, "
            "transcriptas por el coach; la transcripción puede tener errores de Whisper.", ""]
    for n, e in enumerate(log, 1):
        it, res = e["item"], e["res"]
        q = it.get("prompt") or it["q"]
        lines += [f"{n}. [{NAMES[res['objetivo']]}] {q}",
                  f"   Dije: {e['said']}" + ("  (escrito a mano)" if e["manual"] else ""),
                  f"   Coach: {PLAIN[res['veredicto']]}. {res['motivo']}",
                  f"   Modelo: {it['model']}", ""]
        chat += [f"{n}. ({NAMES[res['objetivo']]}) {q}", f"   Dije: {e['said']}",
                 f"   El coach dijo: {PLAIN[res['veredicto']]}", ""]
    lines += ["", "Para pegar en el chat:", ""] + chat
    return "\n".join(lines) + "\n", "\n".join(chat).strip()


# ---------------------------------------------------------------- progreso y menú

def show_progress():
    rows = read_history()
    print(C.rule_line("Tu progreso en tiempos verbales"))
    if not rows:
        print("Todavía no hiciste ninguna serie.")
        return
    series = {r["serie"] for r in rows}
    print(f"Respuestas: {len(rows)} · series: {len(series)}")
    print()
    stats = tense_stats(rows)
    mark = {BIEN: C.ok("+"), CASI: C.warn("~"), MAL: C.bad("x")}
    worst = []
    for t in ORDER:
        res = stats.get(t)
        if not res:
            continue
        s = score(res)
        worst.append((s, t))
        pct = f"{round(s * 100):>3}%"
        color = C.ok if s >= 0.8 else C.warn if s >= 0.5 else C.bad
        print(f"  {NAMES[t]:<28} {color(pct)}  {len(res):>3} resp.   últimas: {''.join(mark[r] for r in res[-8:])}")
    print(C.dim("\n  % sobre tus últimas 15 respuestas de cada tiempo (casi = medio punto). + bien · ~ casi · x mal"))
    weak = sorted(x for x in worst if x[0] < 0.7)
    if weak:
        t = weak[0][1]
        print(C.warn(f"\n  > Tu punto flojo ahora: {NAMES[t]}. Lección {APUNTE.get(t, '')} del cuaderno y una serie "
                     f"con la opción 4."))
    print(C.rule_line())


def choose_tense(items):
    present = [t for t in ORDER if any(target_of(i) == t for i in items)]
    print()
    for n, t in enumerate(present, 1):
        cnt = sum(1 for i in items if target_of(i) == t)
        print(f"  {n:>2}  {NAMES[t]} ({cnt})")
    op = C.ask("> ")
    if op.isdigit() and 1 <= int(op) <= len(present):
        return present[int(op) - 1]
    return None


def load_items():
    if not DATA.exists():
        sys.exit(f"No encuentro {DATA.name}. Tiene que estar en la misma carpeta que coach.py.")
    return json.loads(DATA.read_text(encoding="utf-8"))


def menu(args):
    items = load_items()
    g = sum(1 for i in items if i["nivel"] == 1)
    print()
    print(C.bold("Coach de tiempos verbales"))
    print(C.dim(f"{g} oraciones guiadas (Tense Runner) y {len(items) - g} preguntas abiertas. Series de {args.cantidad or SERIES}."))
    if args.nivel:
        run_series(items, args.nivel, args)
    while True:
        print()
        print("  1  Nivel 1 · Oraciones guiadas: completá y decí la oración")
        print("  2  Nivel 2 · Preguntas con el tiempo indicado")
        print("  3  Nivel 3 · Preguntas mezcladas, sin decirte el tiempo")
        print("  4  Practicar un tiempo verbal")
        print("  5  Repasar mis errores")
        print("  6  Ver mi progreso por tiempo")
        print("  7  Probar el micrófono")
        print("  0  Volver")
        op = C.ask("> ")
        if op in ("1", "2", "3"):
            run_series(items, int(op), args)
        elif op == "4":
            t = choose_tense(items)
            if t:
                lv = C.ask("¿Guiadas (1), preguntas (2) o las dos (Enter)? > ")
                run_series(items, int(lv) if lv in ("1", "2") else 0, args, tense=t)
        elif op == "5":
            run_series(items, 0, args, errors_only=True)
        elif op == "6":
            show_progress()
        elif op == "7":
            C.mic_test()
        elif op in ("0", "v", "q", "salir"):
            return


def probe(sentence):
    found, flags = detect(sentence)
    print("tokens:", tokens(sentence))
    print("tiempos:", [NAMES[f] for f in found])
    for f in flags:
        print("aviso:", f)
    print("errores:", [e["id"] for e in tense_rule_errors(sentence)])


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--probar":
        probe(" ".join(sys.argv[2:]))
    else:
        print("Abrí el coach con iniciar.bat --tiempos (o practicar-tiempos.bat).")
