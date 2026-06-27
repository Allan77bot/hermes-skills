#!/usr/bin/env python3
"""validate_emails.py — checks objectifs sur des cold emails générés.

Usage :
    python validate_emails.py emails.json

Format d'entrée accepté (JSON), au choix :
  - une liste d'objets : [{"subject": "...", "body": "...", "lead": "...", "step": 1}, ...]
  - un objet           : {"emails": [ ... même format ... ]}

Sortie : un rapport lisible par mail + un résumé. Code de sortie != 0 s'il reste des échecs
DURS (sujet trop long ou vide, phrases bannies, corps trop long). Stdlib only, zéro dépendance.
"""
import json
import re
import sys

# Windows : la console est souvent en cp1252 et ne sait pas afficher ✅ / — / →.
# On force UTF-8 en sortie pour que le rapport s'affiche partout.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# Phrases bannies : clichés de cold email + "AI slop" + flatterie LinkedIn.
BANNED = [
    "hope this finds you well",
    "hope this email finds you well",
    "hope you're doing well",
    "hope all is well",
    "to whom it may concern",
    "just following up",
    "just checking in",
    "circle back",
    "circling back",
    "touch base",
    "deep dive",
    "pick your brain",
    "reach out",
    "low-hanging fruit",
    "move the needle",
    "at the end of the day",
    "synergy",
    "i came across your profile",
    "i saw your company is doing great things",
    "love what you're doing",
    "game changer",
    "game-changer",
    # — clichés français (les mails Atelier Klar sont en FR) —
    "j'espère que ce mail vous trouve bien",
    "j'espère que vous allez bien",
    "je me permets de vous contacter",
    "je me permets de revenir vers vous",
    "je reviens vers vous",
    "n'hésitez pas à",
    "je me permets de",
]

# Indices d'un CTA soft / low-friction (heuristique).
SOFT_CTA_HINTS = [
    "?",
    "worth a",
    "open to",
    "would it help",
    "want me to",
    "mind if",
    "could i",
    "interested",
    "make sense",
    "happy to",
    "worth exploring",
    "curious if",
    "ça vaut",
    "ouvert à",
    "ça t'intéresse",
    "ça vous intéresse",
]

MAX_WORDS = 100
MIN_WORDS = 25
MAX_SUBJECT = 60

# Merge-tags / placeholders non remplis : {{...}}, [Société], <...> — l'échec cold-email classique.
PLACEHOLDER = re.compile(r"\{\{.*?\}\}|\[[A-Za-z][\w '-]*\]|<[^>\n]+>")


def normalize(text):
    """Minuscule + apostrophes courbes → droites, pour matcher quelle que soit la saisie."""
    return text.lower().replace("’", "'").replace("ʼ", "'")


def word_count(text):
    return len(re.findall(r"\b\w+\b", text))


def find_banned(text):
    low = normalize(text)
    return [p for p in BANNED if normalize(p) in low]


def find_dashes(text):
    hits = []
    if "—" in text:
        hits.append("— (em dash)")
    if "–" in text:
        hits.append("– (en dash)")
    if re.search(r"\s--\s|\w--\w", text):
        hits.append("-- (double hyphen)")
    return hits


def has_soft_cta(body):
    low = normalize(body)
    return any(normalize(h) in low for h in SOFT_CTA_HINTS)


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = data.get("emails", [])
    if not isinstance(data, list):
        sys.exit('❌ JSON inattendu : attendu une liste ou {"emails": [...]}')
    return data


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage : python validate_emails.py <emails.json>")
    emails = load(sys.argv[1])
    hard_fail = 0
    soft_warn = 0

    for i, e in enumerate(emails):
        subject = (e.get("subject") or "").strip()
        body = (e.get("body") or "").strip()
        label = e.get("lead") or e.get("name") or f"email #{i + 1}"
        step = e.get("step")
        head = f"{label}" + (f" — step {step}" if step else "")
        problems = []

        wc = word_count(body)
        if wc > MAX_WORDS:
            problems.append(f"DUR : corps {wc} mots (> {MAX_WORDS})")
            hard_fail += 1
        elif wc < MIN_WORDS:
            problems.append(f"warn : corps {wc} mots (très court)")
            soft_warn += 1

        if not subject:
            problems.append("DUR : sujet vide")
            hard_fail += 1
        elif len(subject) > MAX_SUBJECT:
            problems.append(f"DUR : sujet {len(subject)} car. (> {MAX_SUBJECT})")
            hard_fail += 1

        banned = find_banned(subject + " " + body)
        if banned:
            problems.append("DUR : phrases bannies → " + ", ".join(banned))
            hard_fail += 1

        if PLACEHOLDER.search(subject + " " + body):
            problems.append("DUR : merge-tag / placeholder non rempli")
            hard_fail += 1

        dashes = find_dashes(subject + " " + body)
        if dashes:
            problems.append("warn : AI slop tirets → " + ", ".join(dashes))
            soft_warn += 1

        if not has_soft_cta(body):
            problems.append("warn : pas de CTA soft détecté")
            soft_warn += 1

        status = "✅ OK" if not problems else "⚠️ "
        print(f"{status} {head}")
        for p in problems:
            print(f"      - {p}")

    print()
    print(
        f"Résumé : {len(emails)} mails · {hard_fail} échec(s) dur(s) · "
        f"{soft_warn} avertissement(s)"
    )
    sys.exit(1 if hard_fail else 0)


if __name__ == "__main__":
    main()
