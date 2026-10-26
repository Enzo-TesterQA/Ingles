#!/usr/bin/env python3
"""Pronunciador: escribís una palabra (o una frase) en inglés y te la dice en voz alta,
con la pronunciación escrita a la española, la sílaba acentuada y el IPA.

Funciona sin internet: usa el diccionario CMU (cmudict.dict, 126.000 palabras) y la voz
en inglés de Windows. Si la palabra está en el doc 10 del kit, también te muestra el error típico.

Uso:
  pronunciar.bat                 te pregunta palabra por palabra
  pronunciar.bat pipeline        directo esa palabra
  pronunciar.bat "test suite"    una frase
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DICT = HERE / "cmudict.dict"
KIT = HERE / "pronunciar-kit.json"

if os.name == "nt":
    os.system("")
COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def c(t, code):
    return f"\033[{code}m{t}\033[0m" if COLOR else t


def bold(t): return c(t, "1")
def dim(t): return c(t, "2")
def accent(t): return c(t, "36")
def warn(t): return c(t, "33")


# ---------------------------------------------------------------- diccionario

def load_dict():
    if not DICT.exists():
        sys.exit(f"No encuentro {DICT.name}. Tiene que estar en la misma carpeta que pronunciar.py.")
    d, tech = {}, set()
    for path in (HERE / "tecnicas.dict", DICT):  # primero las técnicas: api se dice letra por letra
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.split("#")[0].strip()
            if not line:
                continue
            word, *phones = line.split()
            word = re.sub(r"\(\d+\)$", "", word)
            if path == DICT and word in tech:
                continue
            d.setdefault(word, []).append(phones)
        if path != DICT:
            tech = set(d)
    return d


def load_kit():
    try:
        return json.loads(KIT.read_text(encoding="utf-8"))
    except Exception:
        return {}


# ---------------------------------------------------------------- fonética

VOWELS = {"AA", "AE", "AH", "AO", "AW", "AY", "EH", "ER", "EY", "IH", "IY", "OW", "OY", "UH", "UW"}
# a la española, como en el doc 10 (di-PLOI, KYOO, SWEET)
ES = {"AA": "a", "AE": "a", "AH": "a", "AO": "o", "AW": "au", "AY": "ai", "EH": "e", "ER": "er", "EY": "ei",
      "IH": "i", "IY": "ii", "OW": "ou", "OY": "oi", "UH": "u", "UW": "uu",
      "B": "b", "CH": "ch", "D": "d", "DH": "dh", "F": "f", "G": "g", "HH": "j", "JH": "y", "K": "k", "L": "l",
      "M": "m", "N": "n", "NG": "ng", "P": "p", "R": "r", "S": "s", "SH": "sh", "T": "t", "TH": "th", "V": "v",
      "W": "w", "Y": "y", "Z": "z", "ZH": "zh"}
IPA = {"AA": "ɑ", "AE": "æ", "AH": "ʌ", "AO": "ɔ", "AW": "aʊ", "AY": "aɪ", "EH": "ɛ", "ER": "ɝ", "EY": "eɪ",
       "IH": "ɪ", "IY": "i", "OW": "oʊ", "OY": "ɔɪ", "UH": "ʊ", "UW": "u",
       "B": "b", "CH": "tʃ", "D": "d", "DH": "ð", "F": "f", "G": "g", "HH": "h", "JH": "dʒ", "K": "k", "L": "l",
       "M": "m", "N": "n", "NG": "ŋ", "P": "p", "R": "r", "S": "s", "SH": "ʃ", "T": "t", "TH": "θ", "V": "v",
       "W": "w", "Y": "j", "Z": "z", "ZH": "ʒ"}
# inicios de sílaba que existen en inglés (para cortar bien: in-TEG-rate no, IN-te-greit sí)
ONSETS = {("P", "L"), ("P", "R"), ("B", "L"), ("B", "R"), ("T", "R"), ("D", "R"), ("K", "L"), ("K", "R"),
          ("G", "L"), ("G", "R"), ("F", "L"), ("F", "R"), ("TH", "R"), ("SH", "R"), ("S", "P"), ("S", "T"),
          ("S", "K"), ("S", "M"), ("S", "N"), ("S", "L"), ("S", "W"), ("K", "W"), ("T", "W"), ("D", "W"),
          ("G", "W"), ("P", "Y"), ("B", "Y"), ("K", "Y"), ("F", "Y"), ("M", "Y"), ("V", "Y"), ("HH", "Y"),
          ("S", "P", "R"), ("S", "T", "R"), ("S", "K", "R"), ("S", "P", "L"), ("S", "K", "W")}


def base(p):
    return re.sub(r"\d", "", p)


def syllables(phones):
    """[(fonemas, acento)] con acento 1 = principal, 2 = secundario, 0 = sin acento."""
    nuclei = [i for i, p in enumerate(phones) if base(p) in VOWELS]
    if not nuclei:
        return [(phones, 0)]
    cuts = [0]
    for a, b in zip(nuclei, nuclei[1:]):
        cons = phones[a + 1:b]
        k = len(cons)
        # la sílaba siguiente se lleva el grupo de consonantes más largo que pueda empezar una sílaba
        take = 0
        for n in range(min(3, k), 0, -1):
            grp = tuple(base(p) for p in cons[k - n:])
            if n == 1 or grp in ONSETS:
                take = n
                break
        if base(cons[k - 1]) == "NG" if k else False:
            take = 0
        cuts.append(b - take)
    cuts.append(len(phones))
    out = []
    for s, e in zip(cuts, cuts[1:]):
        chunk = phones[s:e]
        stress = next((int(p[-1]) for p in chunk if p[-1].isdigit()), 0)
        out.append((chunk, stress))
    return out


def spanish(phones):
    parts = []
    for chunk, stress in syllables(phones):
        txt = ""
        for p in chunk:
            b = base(p)
            if b == "AH" and p.endswith("0"):
                txt += "e"  # schwa: vocal débil
            elif b == "ER" and p.endswith("0"):
                txt += "er"
            else:
                txt += ES[b]
        parts.append(txt.upper() if stress == 1 else txt)
    return "-".join(parts)


def ipa(phones):
    out = []
    for chunk, stress in syllables(phones):
        txt = ""
        for p in chunk:
            b = base(p)
            if b == "AH" and p.endswith("0"):
                txt += "ə"
            elif b == "ER" and p.endswith("0"):
                txt += "ɚ"
            else:
                txt += IPA[b]
        out.append(("ˈ" if stress == 1 else "ˌ" if stress == 2 else "") + txt)
    return "/" + "".join(out) + "/"


def tips(word, phones):
    """Avisos de los sonidos que más cuestan a un hispanohablante (doc 10, sección 4)."""
    b = [base(p) for p in phones]
    out = []
    if "TH" in b:
        out.append("TH sorda (th): lengua entre los dientes y soplás, no es t ni s.")
    if "DH" in b:
        out.append("TH sonora (dh): lengua entre los dientes con voz, como una d muy suave.")
    if b and b[0] == "S" and len(b) > 1 and b[1] not in VOWELS:
        out.append("Empieza con s + consonante: no agregues una e adelante (\"estart\"). Arrancá con un sss largo.")
    if "V" in b:
        out.append("V: dientes de arriba sobre el labio de abajo. No es b.")
    if "HH" in b:
        out.append("H (j): es solo aire, suave, como empañar un vidrio. No es la j fuerte del español.")
    if "Z" in b:
        out.append("Z: es una s con vibración, como el zumbido de una abeja.")
    if "ZH" in b:
        out.append("ZH: como la y argentina de \"yo\", pero suave.")
    if "AE" in b:
        out.append("La a de cat (æ): boca abierta como para la a, con la lengua en posición de e.")
    if "IH" in b and "IY" not in b and any(p.startswith("IH1") for p in phones):
        out.append("La i acentuada es corta y relajada (como en ship), casi una e. La larga (ii) es la de sheep.")
    if "W" in b:
        out.append("W: labios redondos como para la u, sin g adelante.")
    if any(p.startswith("AH0") for p in phones):
        out.append("La e sin acento es una vocal débil (schwa): relajala, no la digas clara.")
    if word.endswith("ed") and b[-1] in ("T", "D") and not (len(b) > 2 and b[-2] in ("IH", "AH")):
        out.append(f"-ed sin sílaba extra: suena {'t' if b[-1] == 'T' else 'd'} al final, no \"ed\".")
    elif word.endswith("ed") and len(b) > 2 and b[-2] in ("IH", "AH"):
        out.append("-ed con sílaba extra (id), porque el verbo termina en t o d.")
    if b and b[-1] not in VOWELS and len(b) > 2 and b[-2] not in VOWELS:
        out.append("Termina en dos consonantes: marcá las dos, no te las comas.")
    return out


# ---------------------------------------------------------------- voz

SPEAK_PS = r"""
$text = [IO.File]::ReadAllText(__PATH__, [Text.Encoding]::UTF8)
try {
  Add-Type -AssemblyName System.Speech
  $s = New-Object System.Speech.Synthesis.SpeechSynthesizer
  $v = $s.GetInstalledVoices() | Where-Object { $_.Enabled -and $_.VoiceInfo.Culture.Name -like 'en-*' } |
       Select-Object -First 1
  if ($v) { $s.SelectVoice($v.VoiceInfo.Name); $s.Rate = __RATE__; $s.Speak($text); exit 0 }
} catch {}
try {
  $cat = New-Object -ComObject SAPI.SpObjectTokenCategory
  $cat.SetId('HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices', $false)
  foreach ($t in $cat.EnumerateTokens()) {
    if ($t.GetAttribute('Language') -match '^(409|809|c09|1009|4809)') {
      $sp = New-Object -ComObject SAPI.SpVoice
      $sp.Voice = $t; $sp.Rate = __RATE__; [void]$sp.Speak($text); exit 0
    }
  }
} catch {}
exit 3
"""
_NO_VOICE = []


def speak(text, rate=-1):
    if _NO_VOICE:
        return False
    try:
        if os.name == "nt":
            import base64
            with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
                f.write(text)
            script = SPEAK_PS.replace("__PATH__", "'" + f.name.replace("'", "''") + "'").replace("__RATE__", str(rate))
            enc = base64.b64encode(script.encode("utf-16-le")).decode("ascii")
            r = subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-EncodedCommand", enc],
                               capture_output=True, timeout=60)
            os.unlink(f.name)
            if r.returncode == 3:
                _NO_VOICE.append(1)
                print(dim("(No encontré una voz en inglés en Windows. Para escucharla: Configuración > Hora e idioma > "
                          "Voz > Agregar voces > English (United States).)"))
                return False
            return r.returncode == 0
        for cmd in (["say", "-r", str(175 + rate * 25), text], ["espeak", "-v", "en-us", "-s", str(160 + rate * 20), text]):
            try:
                if subprocess.run(cmd, capture_output=True, timeout=60).returncode == 0:
                    return True
            except FileNotFoundError:
                continue
    except Exception:
        pass
    _NO_VOICE.append(1)
    return False


# ---------------------------------------------------------------- flujo

def lookup(d, word):
    w = word.lower().strip(".,;:!?\"()")
    if w in d:
        return w, d[w]
    for alt in (w.replace("-", ""), w.rstrip("s"), w.replace("’", "'")):
        if alt in d:
            return alt, d[alt]
    return w, None


def show(d, kit, text):
    words = [w for w in re.split(r"\s+", text.strip()) if w]
    print()
    for word in words:
        key, prons = lookup(d, word)
        print(bold(word))
        if not prons:
            print(warn("  No la tengo en el diccionario (¿está bien escrita?). Te la leo igual."))
        else:
            seen = []
            for n, ph in enumerate(prons[:3]):
                es = spanish(ph)
                if es in seen:
                    continue
                seen.append(es)
                tag = "  Suena:" if n == 0 else "  o bien:"
                print(f"{tag} {accent(es)}   {dim(ipa(ph))}")
            print(dim("  La sílaba en MAYÚSCULA es la acentuada."))
            if len(prons) > 1 and key in {"read", "live", "lead", "record", "present", "object", "project", "increase",
                                          "permit", "content", "use", "close", "tear", "wind", "minute", "produce"}:
                print(dim("  Tiene más de una pronunciación según si es verbo, sustantivo o tiempo verbal."))
        k = kit.get(key)
        if k:
            print(f"  Del doc 10: suena {k['suena']} · error típico: {k['error']}")
        if prons:
            for t in tips(key, prons[0])[:3]:
                print(dim("  · " + t))
        print()
    speak(for_voice(text))


ACRONYMS = {"api", "sql", "qa", "ci", "cd", "npm", "llm", "aws", "gcp", "jwt", "ui", "ux", "url", "http", "uat", "pr",
            "qe", "ai", "gui", "json", "yaml", "k8s"}


def for_voice(text):
    """La voz lee mejor las siglas en mayúscula (API, QA) y k8s como Kubernetes."""
    def fix(m):
        w = m.group(0)
        if w.lower() == "k8s":
            return "Kubernetes"
        return w.upper() if w.lower() in ACRONYMS - {"json", "yaml"} else w
    return re.sub(r"[A-Za-z0-9]+", fix, text)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    d = load_dict()
    kit = load_kit()
    args = " ".join(sys.argv[1:]).strip()
    if args:
        show(d, kit, args)
    print(bold("Pronunciador") + dim(" · escribí una palabra o una frase en inglés"))
    last = args
    while True:
        try:
            op = input(dim("Palabra · Enter: repetir · l: lento · 0: salir > ")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if op in ("0", "salir", "q"):
            return
        if not op:
            if last:
                speak(for_voice(last))
            continue
        if op.lower() == "l":
            if last:
                speak(for_voice(last), rate=-5)
            continue
        last = op
        show(d, kit, op)


if __name__ == "__main__":
    main()
