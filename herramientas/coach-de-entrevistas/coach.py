#!/usr/bin/env python3
"""Coach de entrevistas en inglés.

Elegís una pregunta, respondés en voz alta y el programa transcribe lo que dijiste
con Whisper, en tu PC (internet solo la primera vez, para bajar el modelo).
Después te muestra un reporte: duración, ritmo, muletillas, pausas largas,
tiempos verbales que usaste y errores típicos de hispanohablantes.
Al final copia tu respuesta lista para pegarle a Claude en el chat.

Uso:
  python coach.py                      menú
  python coach.py --pregunta R5        directo a una pregunta
  python coach.py --archivo nota.ogg   transcribe un audio que ya grabaste
  python coach.py --texto              escribís la respuesta en vez de grabarla
  python coach.py --modelo base.en     modelo más liviano, si tu PC es lenta
  python coach.py --sin-voz            no lee la pregunta en voz alta
  python coach.py --tiempos            práctica de tiempos verbales (oraciones cortas, ver tiempos.py)
"""
import argparse
import csv
import datetime as dt
import json
import os
import random
import re
import subprocess
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SESSIONS = HERE / "sesiones"
MODELS = HERE / "modelos"
HISTORY = SESSIONS / "historial.csv"
SAMPLE_RATE = 16000
MAX_SECONDS = 240
MODEL_SIZES = {"tiny.en": "75 MB", "base.en": "145 MB", "small.en": "480 MB", "medium.en": "1.5 GB"}
# Whisper suele borrar las muletillas; con muletillas en el prompt las conserva.
FILLER_PROMPT = "Umm, let me think like, hmm... Okay, here's what I'm, like, thinking."

# ---------------------------------------------------------------- pantalla

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
if os.name == "nt":
    os.system("")  # activa los colores ANSI en la consola de Windows
COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def c(text, code):
    return f"\033[{code}m{text}\033[0m" if COLOR else text


def bold(t): return c(t, "1")
def dim(t): return c(t, "2")
def ok(t): return c(t, "32")
def warn(t): return c(t, "33")
def bad(t): return c(t, "31")
def accent(t): return c(t, "36")


def ask(prompt=""):
    try:
        return input(prompt).strip()
    except EOFError:
        return "0"


def fmt_time(seconds):
    seconds = int(round(seconds or 0))
    return f"{seconds // 60}:{seconds % 60:02d}"


def rule_line(title=""):
    line = f"── {title} " if title else ""
    return dim(line + "─" * max(0, 56 - len(line)))


# ---------------------------------------------------------------- preguntas

def load_questions():
    path = HERE / "preguntas.json"
    if not path.exists():
        sys.exit(f"No encuentro {path.name}. Tiene que estar en la misma carpeta que coach.py.")
    return json.loads(path.read_text(encoding="utf-8"))


def find_question(questions, code):
    code = code.strip().upper()
    return next((q for q in questions if q["id"].upper() == code), None)


# ---------------------------------------------------------------- análisis

WORD_RX = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")

FILLERS = [
    ("um", r"\bu+m+\b|\bu+h*m+\b|\bhm+\b|\bmm+\b"),
    ("uh", r"\bu+h+\b|\ber+m*\b|\bah+\b"),
    ("eh", r"\beh+\b"),
    ("you know", r"\byou know\b(?!\s+(?:how|what|why|when|where|that|if|the|it|this))"),
    ("I mean", r"\bI mean\b"),
    ("like", r"(?:^|,\s*)like,|\blike,\s"),
    ("basically", r"\bbasically\b"),
    ("kind of / sort of", r"\b(?:kind|sort) of\b"),
    ("este / bueno / o sea", r"\b(?:este|bueno|o sea|digamos)\b"),
]

PAST_IRREGULAR = set("""was were did had went made built led found took gave wrote ran began chose got knew
thought said told saw came became sent spent left met brought taught caught kept felt held paid put cut
set lost won broke understood heard read grew drove fell forgot meant sold stood woke threw hid hit let
quit shut spread sat slept bought fought sought""".split())
NOT_PAST_ED = {"need", "feed", "seed", "speed", "proceed", "succeed", "exceed", "embed", "bleed",
               "breed", "indeed", "red", "bed", "shed", "weed", "reed", "deed", "heed"}
PARTICIPLES = PAST_IRREGULAR | set("""been done taken given written run gotten seen known become begun
chosen grown broken fallen forgotten driven""".split())


def is_past(word):
    w = word.lower()
    return w in PAST_IRREGULAR or (w.endswith("ed") and len(w) >= 4 and w not in NOT_PAST_ED)


def is_participle(word):
    w = word.lower()
    return w in PARTICIPLES or (w.endswith("ed") and len(w) >= 4 and w not in NOT_PAST_ED)


def has_past(text):
    return any(is_past(w) for w in WORD_RX.findall(text))


PERFECT_RX = re.compile(
    r"\b(?:have|has|'ve|had|'d|having)\s+(?:(?:never|already|just|also|always|recently|not)\s+)?(\w+)"
    r"|\b(?:it|he|she|that|there)'s\s+(been)\b", re.I)


def has_perfect(text):
    return any(is_participle(m.group(1) or m.group(2)) for m in PERFECT_RX.finditer(text))


def clauses(sentence):
    return [p for p in re.split(r"[,;:]|\b(?:and|but|where|which|because|so|while)\b", sentence) if p.strip()]


DURATION_RX = re.compile(
    r"\bsince\s+(?:(?:19|20)\d\d|last\b|then\b|january|february|march|april|may|june|"
    r"july|august|september|october|november|december)"
    r"|\bfor\s+(?:the\s+(?:last|past)\s+)?(?:more\s+than\s+)?(?:\d+|a|an|one|two|three|four|five|six|seven|"
    r"eight|nine|ten|several|many|a\s+few)\s+(?:years?|months?|weeks?)", re.I)
PRESENT_MAIN_RX = re.compile(
    r"\b(?:I|we|they|you)\s+(?:work|live|use|lead|study|know|manage|coordinate|test|have|do|am|are)\b"
    r"|\b(?:I|we|they|you)(?:'m|'re)\b|\b(?:I|we|they)\s+(?:am|are)\s+\w+ing\b"
    r"|\b(?:he|she|it)\s+(?:works|is|has|uses|leads)\b", re.I)
FINISHED_RX = re.compile(
    r"(?<!since )\b(?:yesterday|(?:\d+|a|one|two|three|four|five|six|seven|eight|nine|ten|a\s+few|several|many)\s+"
    r"(?:years?|months?|weeks?|days?)\s+ago|last\s+(?:week|month|year|sprint|quarter|night|time|monday|friday)"
    r"|in\s+(?:19|20)\d\d|when\s+I\s+was)\b", re.I)
AGO_RX = re.compile(
    r"(?<!since )\b(?:yesterday|(?:\d+|a|one|two|three|four|five|six|seven|eight|nine|ten|a\s+few|several|many)\s+"
    r"(?:years?|months?|weeks?|days?)\s+ago|last\s+(?:week|month|year|sprint|quarter|night|monday|friday))\b", re.I)
PRESENT_VERB_RX = re.compile(
    r"\b(?:I|we|they)\s+(?:work|start|join|lead|use|go|move|decide|build|begin|find|get|have|am|are|do|"
    r"make|take|study|learn|create|design|write|test|fix|change|see|notice|realize|say|tell)\b|\b(?:I|we|they)(?:'m|'re)\b",
    re.I)
PRESENT_PERFECT_RX = re.compile(
    r"\b(?:have|has|'ve)\s+(?:(?:never|already|just|also|always|recently)\s+)?(\w+)", re.I)


SUBJECT_RX = re.compile(r"\b(?:I|we|they|you|he|she|it)\b|\b(?:I|we|they|you)'(?:m|re)\b", re.I)


def check_since_present(s):
    parts = clauses(s)
    for i, cl in enumerate(parts):
        dur = DURATION_RX.search(cl)
        if not dur:
            continue
        if not SUBJECT_RX.search(cl) and i + 1 < len(parts):
            cl = cl + " " + parts[i + 1]  # "Since 2019, I work..." -> mirar la cláusula siguiente
        if PRESENT_MAIN_RX.search(cl) and not has_perfect(cl) and not has_past(cl):
            return dur


def check_perfect_finished(s):
    for cl in clauses(s):
        fin = FINISHED_RX.search(cl)
        if fin and any(is_participle(m.group(1)) for m in PRESENT_PERFECT_RX.finditer(cl)):
            return fin


def check_ago_present(s):
    ago = AGO_RX.search(s)
    if ago and PRESENT_VERB_RX.search(s) and not has_past(s) and not has_perfect(s):
        return ago


def check_will_time(s):
    for m in re.finditer(r"\b(?:when|after|before|as soon as|until|once)\s+(?:I|we|you|they|he|she|it|"
                         r"the\s+\w+)\s+will\b", s, re.I):
        before = s[max(0, m.start() - 30):m.start()].lower()
        if not re.search(r"\b(?:know|sure|ask|asked|wonder|tell|decide|idea|clear|see)\b", before):
            return m


def check_aux_past(s):
    for m in re.finditer(r"\b(?:didn'?t|did not)\s+(\w+)|\bdid\s+(?:you|he|she|they|we|I|it)\s+(\w+)", s, re.I):
        if is_past(m.group(1) or m.group(2)):
            return m


SKIP_S = {"always", "sometimes", "as", "has", "is", "was", "this", "its", "yes", "plus", "focus", "access",
          "pass", "process", "discuss", "us", "less", "unless", "address", "progress", "miss", "guess"}


def check_aux_s(s):
    for m in re.finditer(r"\b(?:doesn'?t|does not|don'?t|do not|didn'?t|did not)\s+(\w+)", s, re.I):
        w = m.group(1).lower()
        if w.endswith("s") and not w.endswith(("ss", "us", "is")) and w not in SKIP_S:
            return m


def check_no_subject(s):
    if s.rstrip().endswith("?"):
        return None
    return re.match(r"\s*(?:Is|Was)\s+(?:very|really|so|too|more|important|necessary|difficult|hard|easy|"
                    r"possible|impossible|better|good|bad|normal|common|true|clear|key|critical)\b", s)


def check_one_of(s):
    for m in re.finditer(r"\b(?i:one of the (?:best|biggest|most \w+|main|key|top)) ([a-z]+)\b", s):
        w = m.group(1)
        if not w.endswith("s") and w not in {"of", "in", "at", "for", "is", "was"}:
            return m


SUBJ3 = (r"he|she|it|the team|my team|our team|the company|our company|the test|the pipeline|the app|"
         r"the system|the agent|the framework|the tool|the orchestrator")
BASE3 = (r"work|run|use|need|take|make|have|do|go|check|fail|pass|create|send|show|test|cover|call|return|"
         r"help|allow|let|give|get|start|handle|support|include|depend|execute|trigger|validate|generate|track")


ING_NOT_VERB = {"bring", "sing", "ring", "swing", "sting", "spring", "string", "thing", "cling", "fling", "king",
                "nothing", "something", "anything", "everything", "morning", "evening"}


def check_modal_ing(s):
    for m in re.finditer(r"\b(?:will|won't|'ll|can|can't|could|should|must|might|would)\s+(\w+ing)\b", s, re.I):
        if m.group(1).lower() not in ING_NOT_VERB:
            return m


def check_third_person(s):
    return re.search(rf"(?:^\s*|[,;:]\s*|\b(?:and|but|so|because|when|where|that|which)\s+)(?:{SUBJ3})\s+(?:{BASE3})\b",
                     s, re.I)


def rx(pattern, flags=re.I):
    compiled = re.compile(pattern, flags)
    return lambda s: compiled.search(s)


# (id, tipo, nombre, chequeo, explicación + corrección, seguro)
# tipo: "tiempo" = tiempos verbales (tu foco), "gramatica", "vocabulario".
RULES = [
    ("T-SINCE", "tiempo", "since/for con presente", check_since_present,
     "Since/for con algo que sigue hasta hoy va en Present Perfect: I've worked here since 2021 / "
     "I've been working in QA for seven years.", True),
    ("T-FINISHED", "tiempo", "Present Perfect con tiempo terminado", check_perfect_finished,
     "Con un momento terminado (ago, last..., in 2022, yesterday) va Past Simple: I worked there in 2022.", True),
    ("T-AGO", "tiempo", "ago/last con presente", check_ago_present,
     "Ago, last y yesterday siempre con Past Simple: Two years ago I worked at Accusys.", True),
    ("T-WILL", "tiempo", "will después de when/after", check_will_time,
     "Después de when, after, before, as soon as o until va presente, no will: when I finish the tests...", True),
    ("T-IF-WOULD", "tiempo", "would después de if", rx(r"\bif\s+(?:I|we|they|he|she|it)\s+would\b"),
     "Después de if nunca va would: If I had more time, I would automate it.", True),
    ("T-AUX-PAST", "tiempo", "did/didn't + pasado", check_aux_past,
     "Después de did o didn't el verbo va en base: I didn't find it / Did you find it?", True),
    ("T-AUX-S", "tiempo", "doesn't/don't + verbo con -s", check_aux_s,
     "Después de doesn't o don't el verbo va sin -s: it doesn't work.", True),
    ("T-DONT3", "tiempo", "he/she/it + don't",
     rx(r"(?:^|[,;:]\s*|\b(?:and|but|so|because|when|that)\s+)(?:he|she|it|(?:the|my|our) \w*[a-rt-z])\s+don'?t\b"),
     "Con he, she, it o un sujeto singular va doesn't: she doesn't write unit tests.", True),
    ("T-NO-BE", "tiempo", "falta am/is/are antes del -ing",
     rx(r"(?<!\bare )(?<!\bis )(?<!\bam )(?<!\bwas )(?<!\bwere )(?<!\baren't )(?<!\bisn't )"
        r"\b(?:I|we|they|you|he|she)\s+(?:working|going|testing|doing|running|using|trying|looking|planning|"
        r"thinking|waiting|leading|building|learning|studying)\b"),
     "El continuo necesita be: I'm working on it / I'm going to test it.", True),
    ("T-MODAL-ING", "tiempo", "will/can + -ing", check_modal_ing,
     "Después de will, can, should, etc. va el verbo en base: I will work on it (o I'll be working on it).", True),
    ("T-USE-TO", "tiempo", "use to para el presente",
     rx(r"(?<!which )(?<!that )(?<!did )(?<!didn't )(?<!would )(?<!could )(?<!will )(?<!can )(?<!do )"
        r"\b(?:I|we|they|you)\s+use to\b"),
     "Si es una costumbre actual, va usually: I usually write... (used to es algo que hacías antes). "
     "Si quisiste decir 'usamos X para', está bien.", False),
    ("T-USED-TO-ING", "tiempo", "be used to + verbo base",
     rx(r"\b(?:am|'m|is|'s|are|'re|get|got|getting)\s+used to\s+(?:work|write|test|lead|do|use|run|deal|manage|"
        r"speak|talk|travel|wake|get|have|be|handle)\b"),
     "Be used to (estar acostumbrado) va con -ing: I'm used to working with tight deadlines.", True),
    ("T-3RD", "tiempo", "falta la -s (he/she/it)", check_third_person,
     "Con he, she, it o un sujeto singular, el presente lleva -s: the pipeline runs, it works.", False),
    ("T-AGREE", "tiempo", "I'm agree", rx(r"\b(?:I'm|I am|we're|we are)\s+(?:totally\s+|completely\s+)?agree\b"),
     "Agree es un verbo: I agree / I don't agree.", True),
    ("T-SINCE-YEARS", "tiempo", "since + cantidad de años",
     rx(r"\bsince\s+(?:\d+|two|three|four|five|six|seven|eight|nine|ten|a\s+few|many|several)\s+(?:years?|months?|weeks?)\b"),
     "Para una cantidad de tiempo va for (for five years); since va con un punto de inicio (since 2019).", True),
    ("G-NO-SUBJECT", "gramatica", "falta el sujeto", check_no_subject,
     "En inglés el sujeto nunca se omite: It is very important to test early.", True),
    ("G-PEOPLE", "gramatica", "people is", rx(r"\bpeople\s+(?:is|was|has)\b"),
     "People es plural: people are / people were / people have.", True),
    ("G-UNCOUNT", "gramatica", "plural de incontables",
     rx(r"\b(?:feedbacks|informations|advices|evidences|softwares|knowledges|equipments|researches)\b"),
     "Feedback, information, advice, software y knowledge no llevan plural: a lot of feedback.", True),
    ("G-AT", "gramatica", "in + empresa",
     rx(r"\b(?:work|works|worked|working)\s+in\s+(?:Worldsys|Accusys|uTest|Cat Technologies|Coto|Globant|"
        r"Mercado\s+Libre)\b"),
     "Con empresas va at: I work at Worldsys. In va con ciudad, equipo o área.", True),
    ("G-SAID-ME", "gramatica", "said me", rx(r"\bsaid\s+(?:me|us|him|her|them)\b"),
     "Say no lleva persona: he told me that... / he said that...", True),
    ("G-EXPLAIN-ME", "gramatica", "explain me", rx(r"\bexplain(?:ed|s|ing)?\s+(?:me|us|him|her|them)\b"),
     "Explain to me how it works / Can you explain how it works?", True),
    ("G-DEPENDS-OF", "gramatica", "depends of", rx(r"\bdepend(?:s|ed|ing)?\s+of\b"),
     "Depend va con on: it depends on the team.", True),
    ("G-MORE-SHORT", "gramatica", "more + adjetivo corto",
     rx(r"\bmore\s+(?:easy|fast|quick|cheap|big|small|hard|short|long|safe|new|old|high|low|slow)\b"),
     "Los adjetivos cortos van con -er: easier, faster, cheaper, bigger.", True),
    ("G-MORE-BETTER", "gramatica", "more better", rx(r"\bmore\s+(?:better|worse|easier|faster|bigger|smaller)\b"),
     "Better ya es comparativo: sin more.", True),
    ("G-WHAT-MEANS", "gramatica", "what means", rx(r"\bwhat\s+means\b"),
     "Preguntas con does: What does it mean?", True),
    ("G-INDIRECT", "gramatica", "pregunta indirecta invertida",
     rx(r"\b(?:tell me|know|wonder|asked?)\s+(?:where|when|why|how)\s+(?:is|are|was|were|does|did|do)\b"),
     "En preguntas indirectas no se invierte: Can you tell me where the report is?", False),
    ("G-DOUBLE-NEG", "gramatica", "doble negación",
     rx(r"\b(?:didn't|don't|doesn't|can't|won't|haven't|hasn't|never|wasn't|weren't)\s+(?:\w+\s+){0,2}"
        r"(?:nothing|nobody|nowhere)\b"),
     "En inglés no hay doble negación: I didn't see anything.", True),
    ("G-LIKE-VERY", "gramatica", "like very much + objeto", rx(r"\blike\s+very\s+much\s+(?!\.)\w+"),
     "Very much no va entre el verbo y el objeto: I really like testing.", True),
    ("G-ED-ING", "gramatica", "-ing en vez de -ed",
     rx(r"\b(?:I'm|I am|I was|I've been|I feel|I felt|we're|we were)\s+(?:very\s+|really\s+|so\s+|quite\s+)?"
        r"(?:boring|interesting|exciting|tiring|confusing|frustrating)\b"),
     "Para cómo te sentís va -ed: I'm interested in this role / I'm bored.", True),
    ("G-ONE-OF", "gramatica", "one of the + singular", check_one_of,
     "One of the + plural: one of the best testers.", False),
    ("G-AGE", "gramatica", "I have N years (edad)",
     rx(r"\bI\s+have\s+(?:\d{2}|twenty[\w-]*|thirty[\w-]*)\s+years\b(?!\s+(?:of|in|as|working|at|with|doing|old))"),
     "La edad va con be: I'm 27.", True),
    ("G-THE-LAST", "gramatica", "the last week I...", rx(r"(?:^|[.!?]\s+)The\s+last\s+(?:week|month|year|sprint)\s+(?:I|we)\b", 0),
     "Sin the: Last week I fixed...", True),
    ("G-PREP-TIME", "gramatica", "preposición de tiempo",
     rx(r"\bin\s+(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)s?\b(?!')|\bat the \d{1,2}\b"),
     "On + día, at + hora: on Monday at 10.", True),
    ("V-MAKE", "vocabulario", "make + test/question/deploy",
     rx(r"\b(?:make|makes|making|made)\s+(?:a\s+(?:test|deploy|question|review|code review)|questions|deploys)\b"),
     "Collocations: run/write a test, ask a question, do a review, deploy.", True),
    ("V-DO-MISTAKE", "vocabulario", "do a mistake",
     rx(r"\b(?:do|does|did|doing|done)\s+(?:a\s+|some\s+|many\s+|a\s+lot\s+of\s+)?mistakes?\b"),
     "Make a mistake (no do).", True),
    ("V-DOUBT", "vocabulario", "I have a doubt", rx(r"\b(?:have|had)\s+a\s+(?:small\s+|quick\s+)?doubt\b"),
     "Para preguntar: I have a question. Doubt es dudar de algo.", True),
    ("V-ASSIST", "vocabulario", "assist to", rx(r"\bassist(?:ed|ing|s)?\s+to\b"),
     "Ir a una reunión es attend: I attended the meeting.", True),
    ("V-RESPONSIBLE", "vocabulario", "responsible of", rx(r"\bresponsible\s+of\b"),
     "Responsible for: I was responsible for the regression suite.", True),
    ("V-REALIZE", "vocabulario", "realize = realizar",
     rx(r"\breali[sz](?:e|ed|es|ing)\s+(?:the\s+|a\s+|an\s+|some\s+|all\s+the\s+)?"
        r"(?:tests?|testing|tasks?|analysis|project|meeting|deploy\w*)\b"
        r"(?!\s+(?:was|were|is|are|had|has|didn't|wasn't|weren't|could|would|did|failed|passed))"),
     "Realize es darse cuenta. Para realizar: run / do / carry out the tests.", True),
    ("V-ACTUALLY", "vocabulario", "actually = actualmente",
     rx(r"\bactually,?\s+(?:I|I'm|I am|we|we're)\s+(?:work|am working|'m working|working|lead|am|'m|are|study)\b"),
     "Actually es en realidad. Para actualmente: currently / right now.", False),
    ("V-DISCUSS", "vocabulario", "discuss about", rx(r"\bdiscuss(?:ed|ing|es)?\s+about\b"),
     "Discuss va sin about: we discussed the scope.", True),
]
RULE_NAMES = {r[0]: r[2] for r in RULES}


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]


def snippet(sentence, match, width=70):
    if len(sentence) <= width:
        return sentence
    a = max(0, match.start() - 25)
    z = min(len(sentence), match.end() + 35)
    return ("..." if a else "") + sentence[a:z].strip() + ("..." if z < len(sentence) else "")


def normalize(text):
    return text.replace("\u2019", "'").replace("\u2018", "'")


def check_grammar(text):
    text = normalize(text)
    findings = []
    for s in sentences(text):
        for rid, kind, name, check, msg, sure in RULES:
            m = check(s)
            if m:
                findings.append({"id": rid, "tipo": kind, "nombre": name, "frase": snippet(s, m),
                                 "regla": msg, "seguro": sure})
    return findings


TENSE_PATTERNS = [
    ("Present Perfect Continuous", r"\b(?:have|has|'ve)\s+been\s+\w+ing\b"),
    ("Present Perfect", None),
    ("Past Simple", None),
    ("Present Continuous", r"\b(?:am|is|are|'m|'re)\s+(?!going to\b)\w+ing\b"),
    ("Past Continuous", r"\b(?:was|were)\s+\w+ing\b"),
    ("Past Perfect", r"\b(?:had|'d)\s+(?:already\s+|just\s+|never\s+)?(?:been|\w+ed|done|made|built|found|taken|"
                     r"given|written|seen|known|gone|left|sent|told|said)\b"),
    ("Futuro (will / going to)", r"\b(?:will|'ll|won't)\s+\w+|\b(?:am|is|are|'m|'re|'s)\s+going to\b"),
    ("Condicional (would)", r"\b(?:would|'d)\s+(?!have\b)[a-z]+\b"),
]


PRESENT_SIMPLE_RX = re.compile(
    r"\b(?:I|we|they|you)\s+(?:usually\s+|always\s+|often\s+|also\s+|normally\s+|never\s+|sometimes\s+|"
    r"really\s+|just\s+)?([a-z]+)\b|\b(?:he|she|it)\s+(?:usually\s+|always\s+|also\s+)?([a-z]+s)\b"
    r"|\b(?:I'm|we're|they're|you're|it's|he's|she's|am|is|are)\s+(?!going\b|used\b|been\b)([a-z]+)\b")
NOT_PRESENT = {"am", "is", "are", "was", "were", "will", "would", "have", "has", "had", "did", "do", "does",
               "can", "could", "should", "must", "might", "may", "shall", "don't", "didn't", "won't", "can't",
               "to", "and", "or", "but", "so", "also", "as", "at", "in", "on", "with", "for", "been", "not"}


def present_simple_count(text):
    n = 0
    for m in PRESENT_SIMPLE_RX.finditer(text):
        w = (m.group(1) or m.group(2) or m.group(3) or "").lower()
        if w in NOT_PRESENT or w.endswith("ing") or is_past(w):
            continue
        n += 1
    return n


def tense_tally(text):
    tally = Counter()
    tally["Present Simple"] = present_simple_count(text)
    for name, pat in TENSE_PATTERNS:
        if pat:
            tally[name] = len(re.findall(pat, text, re.I))
    pp = sum(1 for m in PRESENT_PERFECT_RX.finditer(text) if is_participle(m.group(1))
             and m.group(1).lower() != "been")
    pp += len(re.findall(r"\b(?:have|has|'ve)\s+been\s+(?!\w+ing\b)\w+", text, re.I))
    tally["Present Perfect"] = pp
    past = 0
    for s in sentences(text):
        toks = WORD_RX.findall(s)
        for i, w in enumerate(toks):
            prev = toks[i - 1].lower() if i else ""
            if prev in {"already", "just", "never", "also", "recently", "always"} and i > 1:
                prev = toks[i - 2].lower()
            if is_past(w) and prev not in {"have", "has", "had", "been", "be", "is", "are", "was", "were",
                                           "get", "got", "'ve", "i've", "we've", "it's", "being"}:
                if w.lower() in {"was", "were"} and i + 1 < len(toks) and toks[i + 1].lower().endswith("ing"):
                    continue
                past += 1
    tally["Past Simple"] = past
    return {k: v for k, v in tally.items() if v}


def is_story(q):
    return bool(q) and bool(re.match(r"(?:Tell me about a (?:time|project|difficult|mistake)|Describe a time|"
                                     r"Give me an example)", q.get("pregunta", ""), re.I))


def target_for(q):
    if not q:
        return None
    i = q["id"]
    if i == "R-TMAY-30":
        return (25, 45)
    if i.startswith("R-TMAY") or i == "R-CV":
        return (60, 120)
    if is_story(q):
        return (90, 180)
    return (40, 120)


def term_used(term, text):
    alts = re.findall(r"\(([^)]*)\)", term) + re.sub(r"\([^)]*\)", "", term).split("/")
    for alt in (a.strip() for a in alts):
        if alt and re.search(r"(?<!\w)" + re.escape(alt).replace(r"\ ", r"[\s-]+") + r"(?!\w)", text, re.I):
            return True
    return False


RESULT_RX = re.compile(
    r"\b(?:as a result|in the end|result|since then|now|today|thanks to|finally|became|"
    r"(?:that|this|it|which) (?:reduced|helped|allowed|saved|cut|improved|meant|changed|made)|"
    r"we (?:reduced|cut|fixed|released|avoided|saved|improved|caught|managed|delivered|shipped)|"
    r"percent|from \w+ to \w+)\b|%", re.I)


def analyze(text, words=None, duration=None, q=None):
    text = normalize(text)
    toks = WORD_RX.findall(text)
    rep = {"palabras": len(toks), "duracion": duration, "ppm": None, "pausas": [], "arranque": None}
    if words:
        speech = max(1.0, words[-1][1] - words[0][0])
        rep["ppm"] = round(len(toks) / speech * 60)
        rep["arranque"] = words[0][0]
        for (a0, a1, aw), (b0, b1, bw) in zip(words, words[1:]):
            if b0 - a1 >= 2.0:
                rep["pausas"].append((round(b0 - a1, 1), bw.strip(" ,.?!")))
    elif duration:
        rep["ppm"] = round(len(toks) / max(1.0, duration) * 60)
    fillers = Counter()
    for name, pat in FILLERS:
        n = len(re.findall(pat, text, re.I))
        if n:
            fillers[name] = n
    rep["muletillas"] = dict(fillers)
    rep["tiempos"] = tense_tally(re.sub(r"\b(?:you know|I mean)\b", "", text, flags=re.I))
    rep["errores"] = check_grammar(text)
    rep["objetivo"] = target_for(q)
    rep["consejos"] = []
    star = is_story(q)
    if star and len(toks) > 40 and rep["tiempos"].get("Past Simple", 0) < 4:
        rep["consejos"].append("Una historia STAR se cuenta en Past Simple (I noticed, I decided, I fixed). "
                               "Usaste poco pasado: ¿la contaste en presente?")
    if star and len(toks) > 80 and not RESULT_RX.search(text):
        rep["consejos"].append("No escuché un resultado claro. Cerrá con As a result... y un número o un impacto.")
    if q and q.get("modelo") and not q.get("esqueleto") and len(toks) > 30:
        model = tense_tally(q["modelo"])
        for tense, example in (("Present Perfect", "I've worked..., I've built..."),
                               ("Past Simple", "I built..., I decided...")):
            if tense == "Past Simple" and star:
                continue  # ya lo cubre el consejo de STAR
            if model.get(tense, 0) >= 2 and not rep["tiempos"].get(tense):
                rep["consejos"].append(f"Tu respuesta modelo usa {tense} ({example}) y vos no lo usaste.")
    if q and q.get("clave"):
        rep["clave_usadas"] = [t for t in q["clave"] if term_used(t, text)]
        rep["clave_faltan"] = [t for t in q["clave"] if not term_used(t, text)]
    return rep


def pace_label(ppm):
    if ppm is None:
        return ""
    if ppm < 90:
        return warn("lento: está bien pensar, pero buscá más fluidez")
    if ppm < 110:
        return warn("un poco lento")
    if ppm <= 160:
        return ok("buen ritmo")
    return warn("rápido: bajá un cambio, que se entienda")


def render_report(q, text, rep, audio_path=None):
    out = [rule_line(f"Reporte · {q['id']}" if q else "Reporte")]
    dur = rep["duracion"]
    if dur:
        line = f"Duración     {fmt_time(dur)}"
        if rep["objetivo"]:
            lo, hi = rep["objetivo"]
            mark = ok("bien") if lo <= dur <= hi else warn("corta" if dur < lo else "larga")
            line += f"   (objetivo {fmt_time(lo)} a {fmt_time(hi)}: {mark})"
        out.append(line)
    words_line = f"Palabras     {rep['palabras']}"
    if rep["ppm"]:
        words_line += f" · {rep['ppm']} por minuto · {pace_label(rep['ppm'])}"
    out.append(words_line)
    if rep["muletillas"]:
        total = sum(rep["muletillas"].values())
        detail = ", ".join(f"{k} x{v}" for k, v in sorted(rep["muletillas"].items(), key=lambda x: -x[1]))
        out.append(f"Muletillas   {warn(str(total)) if total > 3 else total}: {detail}")
    else:
        out.append("Muletillas   0")
    if rep["arranque"] and rep["arranque"] > 4:
        out.append(f"Arranque     tardaste {rep['arranque']:.0f} s en empezar a hablar")
    if rep["pausas"]:
        p = ", ".join(f"{s} s antes de \"{w}\"" for s, w in rep["pausas"][:4])
        out.append(f"Pausas largas {len(rep['pausas'])}: {p}")
    if rep["tiempos"]:
        out.append("")
        out.append(bold("Tiempos verbales que usaste") + dim(" (aproximado)"))
        out.append("  " + " · ".join(f"{k} {v}" for k, v in sorted(rep["tiempos"].items(), key=lambda x: -x[1])))
    if q and q.get("tiempos"):
        out.append(dim("  Tu respuesta modelo usa: " + q["tiempos"]))
    errs = rep["errores"]
    out.append("")
    if errs:
        out.append(bold(f"Para revisar ({len(errs)})"))
        for e in errs:
            label = {"tiempo": bad("[TIEMPO]"), "gramatica": warn("[GRAMÁTICA]"),
                     "vocabulario": accent("[VOCABULARIO]")}[e["tipo"]]
            maybe = "" if e["seguro"] else dim(" (posible)")
            out.append(f"  {label}{maybe} \"{e['frase']}\"")
            out.append(f"     {e['regla']}")
    else:
        out.append(ok("No encontré errores de los que el coach sabe detectar.") +
                   dim(" Igual pasale la respuesta a Claude."))
    for tip in rep["consejos"]:
        out.append(warn("  > ") + tip)
    if rep.get("clave_usadas") is not None:
        out.append("")
        used = ", ".join(rep["clave_usadas"]) or "ninguna"
        out.append(f"Palabras clave del modelo: usaste {used}")
        if rep["clave_faltan"]:
            out.append(dim("  Podés sumar: " + ", ".join(rep["clave_faltan"][:8])))
    out.append("")
    out.append(bold("Lo que dijiste"))
    out.append(text or dim("(vacío)"))
    out.append("")
    if audio_path:
        out.append(dim(f"Whisper a veces corrige solo errores chicos (como la -s). Si dudás, escuchá tu audio: "
                       f"{audio_path.name}"))
    out.append(rule_line())
    return "\n".join(out)


def chat_block(q, text, rep):
    meta = []
    if rep["duracion"]:
        meta.append(fmt_time(rep["duracion"]))
    if rep["ppm"]:
        meta.append(f"{rep['ppm']} palabras por minuto")
    head = f"{q['id']}: " if q else ""
    tail = f"\n(Pregunta: {q['pregunta']} · " if q else "\n("
    tail += " · ".join(meta + ["respuesta hablada, transcripta con el coach"]) + ")"
    return head + text + tail


def powershell(script, timeout=60):
    """Corre un script de PowerShell sin problemas de comillas (-EncodedCommand)."""
    import base64
    encoded = base64.b64encode(script.encode("utf-16-le")).decode("ascii")
    return subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded],
                          capture_output=True, timeout=timeout)


def ps_quote(text):
    return "'" + text.replace("'", "''") + "'"


def copy_to_clipboard(text):
    try:
        if os.name == "nt":
            with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
                f.write(text)
            r = powershell(f"Get-Content -Raw -Encoding UTF8 -LiteralPath {ps_quote(f.name)} | Set-Clipboard", 15)
            os.unlink(f.name)
            return r.returncode == 0
        for cmd in (["pbcopy"], ["wl-copy"], ["xclip", "-selection", "clipboard"]):
            try:
                r = subprocess.run(cmd, input=text.encode("utf-8"), capture_output=True, timeout=5)
                if r.returncode == 0:
                    return True
            except FileNotFoundError:
                continue
    except Exception:
        pass
    return False


# ---------------------------------------------------------------- audio

def need(module, pip_name):
    try:
        return __import__(module)
    except ImportError:
        print(bad(f"Falta el paquete {pip_name}. Abrí el coach con iniciar.bat, que lo instala solo."))
        return None
    except OSError as e:  # sounddevice sin PortAudio
        print(bad(f"No pude cargar {pip_name}: {e}"))
        return None


def key_pressed():
    """True si apretaste Enter, sin frenar la grabación."""
    if os.name == "nt":
        import msvcrt
        hit = False
        while msvcrt.kbhit():
            if msvcrt.getwch() in ("\r", "\n"):
                hit = True
        return hit
    import select
    r, _, _ = select.select([sys.stdin], [], [], 0)
    if r:
        sys.stdin.readline()
        return True
    return False


def record(max_seconds=MAX_SECONDS):
    sd = need("sounddevice", "sounddevice")
    np = need("numpy", "numpy")
    if not sd or not np:
        return None
    chunks, level = [], [0.0]

    def callback(indata, frames, t, status):
        chunks.append(indata[:, 0].copy())
        level[0] = float(np.sqrt(np.mean(indata[:, 0] ** 2)))

    if os.name == "nt":
        key_pressed()  # descarta teclas viejas
    t0 = time.time()
    try:
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", callback=callback):
            while True:
                el = time.time() - t0
                bar = "#" * min(20, int(level[0] * 160))
                sys.stdout.write(f"\r  {bad('REC')} {fmt_time(el)}  [{bar:<20}]  Enter para terminar ")
                sys.stdout.flush()
                if key_pressed():
                    break
                if el >= max_seconds:
                    print(warn(f"\n  Llegaste al máximo ({fmt_time(max_seconds)})."))
                    break
                time.sleep(0.1)
    except Exception as e:
        print(bad(f"\nNo pude usar el micrófono: {e}"))
        print("Revisá que esté conectado y que Windows le dé permiso a las apps de escritorio "
              "(Configuración > Privacidad y seguridad > Micrófono).")
        return None
    print()
    audio = np.concatenate(chunks) if chunks else np.zeros(0, dtype="float32")
    if audio.size < SAMPLE_RATE:
        print(warn("La grabación quedó muy corta."))
        return None
    if float(np.max(np.abs(audio))) < 0.01:
        print(warn("No se escuchó casi nada. Probá el micrófono desde el menú (opción 5)."))
    return audio


def save_wav(path, audio):
    import wave
    import numpy as np
    pcm = (np.clip(audio, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm.tobytes())


def play(audio):
    sd = need("sounddevice", "sounddevice")
    if sd is None:
        return
    try:
        sd.play(audio, SAMPLE_RATE)
        sd.wait()
    except Exception as e:
        print(warn(f"No pude reproducir el audio: {e}"))


_MODEL = {}


def load_model(name):
    if name in _MODEL:
        return _MODEL[name]
    fw = need("faster_whisper", "faster-whisper")
    if fw is None:
        return None
    MODELS.mkdir(exist_ok=True)
    fresh = not any(MODELS.glob(f"*{name.replace('.', '*')}*"))
    if fresh:
        print(dim(f"Primera vez con el modelo {name}: lo bajo una sola vez ({MODEL_SIZES.get(name, '?')})..."))
    else:
        print(dim(f"Cargando el modelo {name}..."))
    try:
        model = fw.WhisperModel(name, device="cpu", compute_type="int8", download_root=str(MODELS))
    except Exception as e:
        print(bad(f"No pude cargar el modelo {name}."))
        print("La primera vez necesita internet para bajarlo. Si el problema sigue, probá con --modelo base.en.")
        print(dim(f"Detalle: {e}"))
        return None
    _MODEL[name] = model
    return model


def transcribe(source, model_name, fillers=True):
    model = load_model(model_name)
    if model is None:
        return None
    segments, info = model.transcribe(
        source, language="en", beam_size=5, word_timestamps=True,
        condition_on_previous_text=False, initial_prompt=FILLER_PROMPT if fillers else None)
    texts, words = [], []
    for seg in segments:
        sys.stdout.write(f"\r  Transcribiendo... {fmt_time(seg.end)} de {fmt_time(info.duration)} ")
        sys.stdout.flush()
        texts.append(seg.text.strip())
        words += [(w.start, w.end, w.word.strip()) for w in (seg.words or [])]
    print()
    return {"text": " ".join(t for t in texts if t).strip(), "words": words, "duration": info.duration}


_NO_VOICE = []

# Primero prueba las voces de escritorio (System.Speech); si no hay una en inglés,
# usa las voces de Windows 10/11 (OneCore) a través de SAPI.
SPEAK_PS = r"""
$text = [IO.File]::ReadAllText(__PATH__, [Text.Encoding]::UTF8)
try {
  Add-Type -AssemblyName System.Speech
  $s = New-Object System.Speech.Synthesis.SpeechSynthesizer
  $v = $s.GetInstalledVoices() | Where-Object { $_.Enabled -and $_.VoiceInfo.Culture.Name -like 'en-*' } |
       Select-Object -First 1
  if ($v) { $s.SelectVoice($v.VoiceInfo.Name); $s.Rate = -1; $s.Speak($text); exit 0 }
} catch {}
try {
  $cat = New-Object -ComObject SAPI.SpObjectTokenCategory
  $cat.SetId('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices', $false)
  foreach ($t in $cat.EnumerateTokens()) {
    if ($t.GetAttribute('Language') -match '^(409|809|c09|1009|4809)') {
      $sp = New-Object -ComObject SAPI.SpVoice
      $sp.Voice = $t; $sp.Rate = -1; [void]$sp.Speak($text); exit 0
    }
  }
} catch {}
exit 3
"""


def speak(text):
    """Lee en voz alta con una voz en inglés del sistema. Devuelve False si no hay."""
    if _NO_VOICE:
        return False
    try:
        if os.name == "nt":
            with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
                f.write(text)
            r = powershell(SPEAK_PS.replace("__PATH__", ps_quote(f.name)))
            os.unlink(f.name)
            if r.returncode == 3:
                _NO_VOICE.append(1)
                print(dim("(No encontré una voz en inglés en Windows, así que la pregunta queda solo en pantalla. "
                          "Para escucharla: Configuración > Hora e idioma > Voz > Agregar voces > "
                          "English (United States).)"))
                return False
            return r.returncode == 0
        for cmd in (["say", "-v", "Samantha", text], ["espeak", "-v", "en-us", text]):
            try:
                if subprocess.run(cmd, capture_output=True, timeout=60).returncode == 0:
                    return True
            except FileNotFoundError:
                continue
    except Exception:
        pass
    _NO_VOICE.append(1)
    return False


# ---------------------------------------------------------------- historial

FIELDS = ["fecha", "id", "fuente", "pregunta", "segundos", "palabras", "ppm", "muletillas", "pausas_largas",
          "errores_tiempo", "errores_otros", "reglas", "audio", "reporte"]


def read_history():
    if not HISTORY.exists():
        return []
    with HISTORY.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def save_session(q, text, rep, audio=None, report_text=""):
    SESSIONS.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    base = f"{stamp}_{q['id'] if q else 'libre'}"
    audio_path = None
    if audio is not None:
        audio_path = SESSIONS / f"{base}.wav"
        save_wav(audio_path, audio)
    report_path = SESSIONS / f"{base}.txt"
    clean = re.sub(r"\033\[[0-9;]*m", "", report_text)
    head = f"{q['id']} · {q['pregunta']}\n\n" if q else ""
    report_path.write_text(head + clean + "\n\nPara pegar en el chat:\n" + chat_block(q, text, rep) + "\n",
                           encoding="utf-8")
    new = not HISTORY.exists()
    with HISTORY.open("a", encoding="utf-8-sig" if new else "utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow({
            "fecha": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "id": q["id"] if q else "", "fuente": q["fuente"] if q else "",
            "pregunta": q["pregunta"] if q else "",
            "segundos": round(rep["duracion"]) if rep["duracion"] else "",
            "palabras": rep["palabras"], "ppm": rep["ppm"] or "",
            "muletillas": sum(rep["muletillas"].values()), "pausas_largas": len(rep["pausas"]),
            "errores_tiempo": sum(1 for e in rep["errores"] if e["tipo"] == "tiempo"),
            "errores_otros": sum(1 for e in rep["errores"] if e["tipo"] != "tiempo"),
            "reglas": ";".join(e["id"] for e in rep["errores"]),
            "audio": audio_path.name if audio_path else "", "reporte": report_path.name,
        })
    return audio_path, report_path


def show_progress(questions):
    rows = read_history()
    print(rule_line("Tu progreso"))
    if not rows:
        print("Todavía no hay sesiones. Respondé una pregunta y volvé acá.")
        return
    print(f"Sesiones: {len(rows)} · preguntas distintas: {len({r['id'] for r in rows if r['id']})} "
          f"de {len(questions)}")
    print()
    print(bold("Últimas 10"))
    for r in rows[-10:]:
        dur = fmt_time(int(r["segundos"])) if r["segundos"] else "  -  "
        print(f"  {r['fecha']}  {r['id'] or '-':<10} {dur:>5}  {r['ppm'] or '-':>4} ppm  "
              f"muletillas {r['muletillas']:>2}  tiempos {r['errores_tiempo']}  otros {r['errores_otros']}")
    recent = rows[-10:]
    ppms = [int(r["ppm"]) for r in recent if r["ppm"]]
    if ppms:
        print(f"\nRitmo promedio (últimas 10): {round(sum(ppms) / len(ppms))} palabras por minuto")
    counts = Counter(rid for r in rows for rid in r["reglas"].split(";") if rid)
    if counts:
        print()
        print(bold("Tus errores más repetidos"))
        for rid, n in counts.most_common(6):
            tag = bad("[TIEMPO]") if rid.startswith("T-") else "         "
            print(f"  {n:>3} x  {tag} {RULE_NAMES.get(rid, rid)}")
        top = counts.most_common(1)[0]
        if top[1] >= 3:
            print(warn(f"\n  > Se repite \"{RULE_NAMES.get(top[0], top[0])}\". Contáselo a tu profe y a Claude "
                       f"para sumarlo al Registro de errores."))
    print(rule_line())


# ---------------------------------------------------------------- flujo

def times_practiced():
    return Counter(r["id"] for r in read_history() if r["id"])


def show_model(q):
    print(rule_line("Respuesta modelo" if not q["esqueleto"] else "Esqueleto y frases clave"))
    if q.get("buscan"):
        print(dim("Qué buscan: " + q["buscan"]))
    print(q["modelo"])
    print(rule_line())


def type_answer():
    print("Escribí tu respuesta en inglés. Línea vacía para terminar.")
    lines = []
    while True:
        line = ask()
        if not line:
            break
        lines.append(line)
    return " ".join(lines)


def practice(q, args, questions):
    while True:
        print()
        print(rule_line(f"{q['id']} · {q['cat']} · {q['fuente']}"))
        print(bold(q["pregunta"]))
        if q.get("buscan"):
            print(dim("Qué buscan: " + q["buscan"]))
        if not args.sin_voz:
            speak(q["pregunta"])
        while True:
            hint = "Enter: escribir" if args.texto else "Enter: grabar"
            op = ask(f"\n{hint} · r: repetir la pregunta · m: ver el modelo · v: volver > ").lower()
            if op == "r":
                speak(q["pregunta"])
                continue
            if op == "m":
                show_model(q)
                continue
            break
        if op in ("v", "0"):
            return None
        audio = None
        if args.texto:
            text, words, duration = type_answer(), None, None
        else:
            print(dim("Hablá como en la entrevista. Si te trabás, seguí: no hace falta que salga perfecto."))
            audio = record()
            if audio is None:
                continue
            res = transcribe(audio, args.modelo, not args.sin_muletillas)
            if res is None:
                print("Sin transcripción. Guardo el audio igual y podés escribir lo que dijiste.")
                text, words, duration = type_answer(), None, len(audio) / SAMPLE_RATE
            else:
                text, words, duration = res["text"], res["words"], res["duration"]
        if not text.strip():
            print(warn("No quedó ninguna respuesta para analizar. Probá de nuevo."))
            continue
        rep = analyze(text, words, duration, q)
        report = render_report(q, text, rep, None)
        audio_path, report_path = save_session(q, text, rep, audio, report)
        if audio_path:
            report = render_report(q, text, rep, audio_path)
        print()
        print(report)
        if copy_to_clipboard(chat_block(q, text, rep)):
            print(ok("Copié tu respuesta. Pegala en el chat del proyecto y Claude te la corrige."))
        else:
            print("Para el chat, copiá esto:\n" + chat_block(q, text, rep))
        print(dim(f"Guardado en sesiones/{report_path.name}"))
        while True:
            extra = " · e: escuchar tu grabación" if audio is not None else ""
            op = ask(f"\nEnter: otra vez la misma · m: ver el modelo{extra} · s: siguiente al azar · v: menú > ").lower()
            if op == "m":
                show_model(q)
                continue
            if op == "e" and audio is not None:
                play(audio)
                continue
            break
        if op == "s":
            q = pick_random(questions)
            continue
        if op in ("v", "0"):
            return None


def pick_random(questions, pool=None):
    pool = pool or questions
    done = times_practiced()
    least = min(done.get(q["id"], 0) for q in pool)
    return random.choice([q for q in pool if done.get(q["id"], 0) == least])


def choose_question(questions):
    groups = []
    for q in questions:
        key = (q["fuente"], q["cat"])
        if key not in groups:
            groups.append(key)
    done = times_practiced()
    print()
    print(bold("Elegí una categoría") + dim(" (o escribí el código directo, por ejemplo R5 o Q23)"))
    letters = "abcdefghij"
    for i, (src, cat) in enumerate(groups):
        n = sum(1 for q in questions if (q["fuente"], q["cat"]) == (src, cat))
        print(f"  {letters[i]}  {src} · {cat} ({n})")
    op = ask("> ")
    q = find_question(questions, op)
    if q:
        return q
    if len(op) != 1 or op.lower() not in letters[:len(groups)]:
        return None
    src, cat = groups[letters.index(op.lower())]
    pool = [q for q in questions if (q["fuente"], q["cat"]) == (src, cat)]
    print()
    for i, q in enumerate(pool, 1):
        times = done.get(q["id"], 0)
        mark = ok(f" x{times}") if times else ""
        print(f"  {i:>2}  {q['id']:<10} {q['pregunta']}{mark}")
    print(dim("  Enter: una al azar de esta lista"))
    op = ask("> ")
    if not op:
        return pick_random(questions, pool)
    if op.isdigit() and 1 <= int(op) <= len(pool):
        return pool[int(op) - 1]
    return find_question(questions, op)


def from_file(path, args, questions, q=None):
    path = Path(path).expanduser()
    if not path.exists():
        print(bad(f"No encuentro el archivo {path}"))
        return
    if q is None:
        code = ask("¿A qué pregunta corresponde? Escribí el código (R5, Q23) o Enter si no corresponde a ninguna > ")
        q = find_question(questions, code) if code else None
    res = transcribe(str(path), args.modelo, not args.sin_muletillas)
    if res is None:
        return
    if not res["text"]:
        print(warn("No escuché nada en ese audio."))
        return
    rep = analyze(res["text"], res["words"], res["duration"], q)
    report = render_report(q, res["text"], rep, None)
    save_session(q, res["text"], rep, None, report)
    print()
    print(report)
    if copy_to_clipboard(chat_block(q, res["text"], rep)):
        print(ok("Copié la transcripción para pegarla en el chat."))


def mic_test():
    print("Decí algo durante unos segundos (por ejemplo: \"I've been working in QA since 2019\").")
    print("Apretá Enter para empezar.")
    ask()
    audio = record(max_seconds=8)
    if audio is None:
        return
    import numpy as np
    peak = float(np.max(np.abs(audio)))
    if peak < 0.02:
        print(bad("Muy bajo. Acercá el micrófono o subile el volumen en Configuración > Sistema > Sonido > Entrada."))
    elif peak > 0.98:
        print(warn("Muy alto, se satura. Bajale un poco el volumen de entrada."))
    else:
        print(ok("El micrófono anda bien."))
    print("Te lo reproduzco...")
    play(audio)


def menu(args, questions):
    print()
    print(bold("Coach de entrevistas en inglés"))
    print(dim(f"{len(questions)} preguntas: tus respuestas del CV (doc 13) y el banco (doc 05)."))
    while True:
        print()
        print("  1  Elegir una pregunta")
        print("  2  Pregunta al azar (primero las que menos practicaste)")
        print("  3  Transcribir un audio que ya grabaste (nota de voz, celular)")
        print("  4  Ver mi progreso")
        print("  5  Probar el micrófono")
        print("  6  Tiempos verbales: respuestas de una oración, calificadas en el momento")
        print("  0  Salir")
        op = ask("> ")
        q = find_question(questions, op)
        if q:
            practice(q, args, questions)
        elif op == "1":
            q = choose_question(questions)
            if q:
                practice(q, args, questions)
        elif op == "2":
            practice(pick_random(questions), args, questions)
        elif op == "3":
            path = ask("Arrastrá el archivo a esta ventana (o pegá la ruta) y Enter > ").strip('"').strip("'")
            if path:
                from_file(path, args, questions)
        elif op == "4":
            show_progress(questions)
        elif op == "5":
            mic_test()
        elif op == "6":
            import tiempos
            tiempos.menu(args)
        elif op in ("0", "q", "salir"):
            print("Nos vemos. Mañana otra.")
            return


def main():
    ap = argparse.ArgumentParser(description="Coach de entrevistas en inglés")
    ap.add_argument("--pregunta", help="código de la pregunta (R5, H3, Q23...)")
    ap.add_argument("--archivo", help="transcribir un audio que ya grabaste")
    ap.add_argument("--texto", action="store_true", help="escribir la respuesta en vez de grabarla")
    ap.add_argument("--modelo", default="small.en", choices=list(MODEL_SIZES),
                    help="modelo de Whisper (small.en por defecto; base.en es más rápido)")
    ap.add_argument("--sin-voz", action="store_true", help="no leer las preguntas en voz alta")
    ap.add_argument("--sin-muletillas", action="store_true", help="no pedirle a Whisper que conserve las muletillas")
    ap.add_argument("--tiempos", action="store_true", help="práctica de tiempos verbales (oraciones cortas)")
    ap.add_argument("--nivel", type=int, choices=[1, 2, 3], help="con --tiempos: arranca directo una serie de ese nivel")
    ap.add_argument("--cantidad", type=int, help="con --tiempos: preguntas por serie (10 por defecto)")
    ap.add_argument("--sin-autocorte", action="store_true",
                    help="con --tiempos: no cortar la grabación al hacer silencio (cortás con Enter)")
    args = ap.parse_args()
    if args.tiempos:
        import tiempos
        try:
            tiempos.menu(args)
        except KeyboardInterrupt:
            print("\nListo, corté.")
        return
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    questions = load_questions()
    q = None
    if args.pregunta:
        q = find_question(questions, args.pregunta)
        if not q:
            sys.exit(f"No existe la pregunta {args.pregunta}. Probá con R5, H3, P1, Q23...")
    try:
        if args.archivo:
            from_file(args.archivo, args, questions, q)
        elif q:
            practice(q, args, questions)
        else:
            menu(args, questions)
    except KeyboardInterrupt:
        print("\nListo, corté.")


if __name__ == "__main__":
    sys.modules.setdefault("coach", sys.modules[__name__])  # tiempos.py importa este mismo módulo
    main()
