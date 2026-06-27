---
name: email-qa
description: >-
  Use BEFORE sending or queuing ANY marketing email (cold, nurturing, or newsletter) — this is
  the Claude Code quality gate that reviews a drafted email and returns a PASS/FAIL verdict with
  prioritized fixes, so nothing embarrassing, off-brand or non-compliant ever reaches a prospect.
  It sits between drafting and the validation Sheet. Trigger it whenever an email draft must be
  checked/QA'd, or whenever Hermes routes an email for review before send. Triggers (FR) :
  « relis cet email », « vérifie cet email avant envoi », « QA cet email », « check avant
  d'envoyer », « l'email est-il bon / prêt ? », « valide la copie de ce mail », « anti-gaffe
  email ». Do NOT trigger for: writing an email from scratch (use `copywriting` /
  `cold-email-grounded`), pure visual design (use `atelier-klar-design`), or non-email content.
---

# email-qa — la relecture anti-gaffe d'un email avant envoi

> Le **garde-fou qualité** entre la rédaction et le Sheet de validation. Hermes rédige →
> **toi (Claude Code, le muscle qualité) tu audites** → l'email part au Sheet → Allan valide.
> Rien d'embarrassant, hors-marque ou non conforme ne doit atteindre un prospect. Méthode en
> français, code/commandes en anglais.

## Quand tu interviens

À chaque email **avant qu'il entre dans le Sheet de validation** (cold, nurturing, newsletter).
Tu ne réécris pas l'email de zéro (ça, c'est `copywriting` / `cold-email-grounded`) — tu le
**vérifies** et tu proposes des **corrections précises**.

## Entrée / sortie

- **Entrée** : le brouillon (`type`, `subject`, `preheader`, `body`, `html` éventuel,
  destinataire) + l'**artefact de marque** (`BRAND-VOICE.md` / skills `atelier-klar-design`,
  `copywriting`).
- **Sortie** : un **verdict structuré** — PASS/FAIL par catégorie (avec **preuve**) + top
  corrections + un **GATE go/no-go**. Format exact → `references/checklist.md` (fin du fichier).

## Le réflexe en 3 temps

**1. Lance le check déterministe** (rapide, objectif, réutilisable) :

```bash
python "<dossier-de-ce-skill>/scripts/lint_email.py" emails.json
```

Il attrape ce qui est automatisable : objet trop long, **merge-tags non remplis**, **phrases
bannies (FR+EN)**, **AI slop**, tirets cadratins, **lien de désinscription manquant**, liens
factices, multi-CTA, cold trop long, tout-image. Corrige jusqu'à **0 échec dur**.

**2. Fais l'audit de jugement** (ce que le script ne peut pas trancher) en suivant
`references/checklist.md` : **voix & cohérence de marque** (Voice chart IS/IS NOT, vocabulaire,
archétype), **structure & lisibilité** (one email/one job, mobile, scannable), **anti AI-slop**
(spécificité, une opinion, burstiness), **conformité**. **Cite toujours une preuve** (un extrait
de l'email) pour chaque FAIL — jamais d'affirmation non sourcée.

**3. Rends le verdict + le GATE** (format dans `references/checklist.md`). **NO-GO** dès qu'un
seul **hard gate** échoue (voir §0 de la checklist) — surtout : **rien à > 1 destinataire sans
l'accord explicite d'Allan**.

## Règles d'or

- **Tu proposes, Allan décide.** Le QA prépare un email propre pour le Sheet ; il ne déclenche
  jamais l'envoi.
- **Le visuel (design system) = `atelier-klar-design`** ; **la voix = `copywriting` /
  `BRAND-VOICE.md`**. Toi tu **vérifies** qu'ils ont bien été appliqués, tu ne les refais pas.
- **Cold = texte sobre** (délivrabilité avant branding) ; **chaud = HTML brandé Atelier Klar**.
- Les « spam words » comptent moins que **réputation + engagement** : privilégie les checks
  **structurels et de conformité** aux interdictions de mots.

## Pour aller plus loin

Grille complète + format de verdict → `references/checklist.md`.
Sources de la grille : `email-marketing-bible`, `email-marketing-skill`, `ai-marketing-claude`.
