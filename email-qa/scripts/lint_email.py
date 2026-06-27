#!/usr/bin/env python3
"""lint_email.py — checks DÉTERMINISTES sur un email avant envoi (la part automatisable du QA).

Usage :
    python lint_email.py emails.json

Format d'entrée (JSON), au choix :
  - une liste : [{"type": "cold|nurture|newsletter", "subject": "...", "preheader": "...",
                  "body": "...", "html": "<...>"(optionnel), "lead": "..."}, ...]
  - un objet  : {"emails": [ ... même format ... ]}

`type` par défaut = "nurture". Sortie : rapport par email + résumé. Code de sortie != 0 s'il
reste des échecs DURS. Le jugement (voix de marque, structure, ton) NE s'automatise pas ici →
voir references/checklist.md. Stdlib only.
"""
import json
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

# Clichés à bannir (FR + EN) — échec DUR (cassent la confiance / sentent le robot).
BANNED = [
    "hope this finds you well", "hope this email finds you well", "hope you're doing well",
    "just following up", "circle back", "touch base", "pick your brain", "low-hanging fruit",
    "move the needle", "to whom it may concern",
    "j'espère que ce mail vous trouve bien", "j'espère que vous allez bien",
    "je me permets de vous contacter", "je me permets de revenir vers vous",
    "je reviens vers vous", "n'hésitez pas à",
]

# Mots « AI slop » (source : email-marketing-bible) — AVERTISSEMENT (voix trop IA).
AI_SLOP = [
    "delve", "leverage", "foster", "ignite", "empower", "unleash", "streamline", "seamless",
    "robust", "cutting-edge", "transformative", "multifaceted", "pivotal", "tapestry",
    "landscape", "beacon", "realm", "furthermore", "moreover",
    "à l'ère du", "à l'ère de", "dans un monde où", "révolutionner", "propulser",
]

SOFT_CTA = ["?", "worth a", "open to", "interested", "make sense", "happy to",
            "ça vaut", "ça t'intéresse", "ça vous intéresse", "dispo pour", "on en parle"]

# Placeholders non remplis — MAIS on tolère les tags système (remplis par la plateforme).
PLACEHOLDER = re.compile(r"\{\{\s*([^}]+?)\s*\}\}|\[([A-Za-z][^\]]*)\]|<([^>@\n]+)>")
ALLOWED_TAGS = {
    "unsubscribe", "unsubscribe_link", "unsubscribe link", "list-unsubscribe", "preferences",
    "view in browser", "voir dans le navigateur", "se désinscrire", "désinscription",
}
URL = re.compile(r"https?://[^\s)>\]]+")
UNSUB = re.compile(r"désinscri|desinscri|se désabonn|se desabonn|unsubscribe|list-unsubscribe",
                   re.IGNORECASE)
PLACEHOLDER_URL = re.compile(r"example\.com|yourlink|votre-lien|lien-ici|todo|xxxx", re.IGNORECASE)

MAX_SUBJECT_HARD = 60
MAX_SUBJECT_WARN = 50
COLD_BODY_MAX = 120


def normalize(t):
    return t.lower().replace("’", "'").replace("ʼ", "'")


def words(t):
    return len(re.findall(r"\b\w+\b", t))


def strip_html(h):
    return re.sub(r"<[^>]+>", " ", h)


def find_placeholders(text):
    """Placeholders non remplis, en ignorant les tags système (unsubscribe, etc.)."""
    out = []
    for m in PLACEHOLDER.finditer(text):
        inner = (m.group(1) or m.group(2) or m.group(3) or "").strip().lower()
        if inner in ALLOWED_TAGS:
            continue
        out.append(m.group(0))
    return out


def check(e, i):
    typ = (e.get("type") or "nurture").lower()
    subject = (e.get("subject") or "").strip()
    pre = (e.get("preheader") or "").strip()
    body = (e.get("body") or "").strip()
    html = e.get("html") or ""
    label = e.get("lead") or e.get("name") or f"email #{i + 1}"
    full = subject + " " + pre + " " + body
    hard, warn = [], []

    # Objet
    if not subject:
        hard.append("sujet vide")
    elif len(subject) > MAX_SUBJECT_HARD:
        hard.append(f"sujet {len(subject)} car. (> {MAX_SUBJECT_HARD})")
    elif len(subject) > MAX_SUBJECT_WARN:
        warn.append(f"sujet {len(subject)} car. (> {MAX_SUBJECT_WARN}, risque troncature mobile)")

    # Preheader (chaud)
    if typ in ("nurture", "newsletter") and not pre:
        warn.append("preheader manquant (2e accroche perdue)")

    # Merge-tags / placeholders non remplis
    residual = find_placeholders(full)
    if residual:
        hard.append("merge-tag / placeholder non rempli → " + ", ".join(residual[:4]))

    # Clichés bannis
    banned = [p for p in BANNED if normalize(p) in normalize(full)]
    if banned:
        hard.append("phrases bannies → " + ", ".join(banned))

    # AI slop
    slop = [w for w in AI_SLOP if normalize(w) in normalize(full)]
    if slop:
        warn.append("AI slop → " + ", ".join(slop))
    if "—" in full or re.search(r"\s--\s", full):
        warn.append("tiret cadratin / -- (tic IA)")

    # CTA
    if not any(normalize(h) in normalize(body) for h in SOFT_CTA):
        warn.append("pas de CTA soft détecté")
    urls = [u for u in URL.findall(body) if not UNSUB.search(u)]
    if len(set(urls)) > 2:
        warn.append(f"{len(set(urls))} liens distincts (vise UN seul CTA principal)")
    if PLACEHOLDER_URL.search(body):
        hard.append("lien factice / placeholder dans le corps")

    # Désinscription
    if typ in ("nurture", "newsletter") and not UNSUB.search(body + " " + html):
        hard.append("pas de lien de désinscription (obligatoire en marketing)")
    elif typ == "cold" and not UNSUB.search(body + " " + html):
        warn.append("pas d'opt-out (recommandé même en cold B2B)")

    # Corps : longueur cold
    if typ == "cold" and words(body) > COLD_BODY_MAX:
        hard.append(f"corps {words(body)} mots (cold doit rester court, < {COLD_BODY_MAX})")

    # Tout-image (si HTML fourni)
    if html and len(strip_html(html).strip()) < 200:
        warn.append("trop peu de live-text (Gmail/Gemini résument les ~150-200 1ers car.)")

    return label, typ, hard, warn


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage : python lint_email.py <emails.json>")
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)
    emails = data.get("emails", data) if isinstance(data, dict) else data
    if not isinstance(emails, list):
        sys.exit('❌ JSON inattendu : liste ou {"emails": [...]}')

    total_hard = total_warn = 0
    for i, e in enumerate(emails):
        label, typ, hard, warn = check(e, i)
        total_hard += len(hard)
        total_warn += len(warn)
        status = "✅ OK" if not hard and not warn else ("❌" if hard else "⚠️ ")
        print(f"{status} {label} [{typ}]")
        for h in hard:
            print(f"      - DUR : {h}")
        for w in warn:
            print(f"      - warn : {w}")

    print()
    print(f"Résumé : {len(emails)} email(s) · {total_hard} échec(s) dur(s) · {total_warn} avertissement(s)")
    print("⚠️  Le jugement (voix de marque, structure, ton) reste à faire à la main → references/checklist.md")
    sys.exit(1 if total_hard else 0)


if __name__ == "__main__":
    main()
