---
name: skill-forge
description: >-
  Use when a new reusable capability, method or workflow should become a SKILL — to forge it
  PROPERLY every time instead of writing a sloppy one-off. Covers: capturing intent, writing a
  clean SKILL.md (anatomy + progressive disclosure), a sharp triggering description, a
  quality-review pass before shipping, then install + trace. This is the reflex for creating
  skills well. Trigger it whenever a new skill is being created or an existing one improved,
  even if not asked explicitly. Triggers (FR) : « crée un skill », « fais-en un skill »,
  « transforme ça en skill », « nouveau skill », « ajoute une capacité réutilisable »,
  « améliore ce skill », « il faudrait un skill pour ça ». Do NOT trigger for: simply USING or
  running an existing skill, or turning a VIDEO into a skill (for that, use the regarder-video
  Forge).
---

# Skill-forge — forger un bon skill, à chaque fois

> Le **réflexe** quand une capacité réutilisable doit devenir un skill. Un skill bâclé pollue
> plus qu'il n'aide (il se déclenche au mauvais moment, ou laisse l'agent deviner). Un bon
> skill **se déclenche pile quand il faut** et **dit quoi faire sans deviner**. Méthode en
> français, code/commandes en anglais.

## La règle d'or (soul Hermes)

Forger un skill = **travail qualité soigné** → c'est du ressort de **Claude Code (le muscle)**,
pas du routeur. **Délègue la rédaction et la relecture à Claude Code**, exactement comme pour
tout code ou doc important. Toi (Hermes) tu cadres l'intention et tu valides ; Claude écrit.

## Le réflexe en 4 temps

```
1. CADRER   → quoi / quand / format de sortie
2. ÉCRIRE   → SKILL.md propre (anatomie + progressive disclosure + bonne description)
3. RELIRE   → passe qualité AVANT de livrer (3 angles)  → references/quality-review.md
4. INSTALLER + TRACER
```

### 1. Cadrer (avant d'écrire)

- **Quoi** : que doit permettre ce skill, concrètement ?
- **Quand** : quelles phrases / contextes doivent le déclencher (et lesquels NON) ?
- **Format de sortie** attendu.
Si l'intention est déjà claire dans la conversation, ne re-pose pas la question — extrais-la.

### 2. Écrire le SKILL.md

**Anatomie :**
```
skill-name/
├── SKILL.md            (requis) : frontmatter `name` + `description`, puis le corps
└── (optionnel)
    ├── references/     docs chargées au besoin
    ├── scripts/        code exécutable (tâches déterministes/répétitives)
    └── assets/         gabarits, fichiers de sortie
```

**Progressive disclosure** (le principe clé) : `SKILL.md` reste **lean (< 500 lignes)**. Le
détail va dans `references/`, pointé clairement (« lis `X.md` quand `Y` »). On ne charge le
détail que quand on en a besoin.

**La `description` EST le déclencheur** (c'est ce qui fait que le skill s'active) :
- couvre **quoi** + **quand**, avec les **vraies phrases** que l'utilisateur taperait ;
- sois un peu **« pushy »** (le modèle a tendance à sous-déclencher) ;
- ajoute un **« Do NOT trigger for: … »** avec les faux-amis proches.

**Style** : explique le **pourquoi** plutôt que d'empiler des MUSTs rigides — un modèle
intelligent bien briefé est plus robuste quand le contexte change. Impératif, exemples concrets.

### 3. Relire — la passe qualité (le cœur du réflexe)

**Ne livre jamais un skill non relu.** Fais relire par **Claude Code** sous **3 angles**
(détail + format de verdict → `references/quality-review.md`) :
1. **Structure & déclenchement** (concision, progressive disclosure, description nette).
2. **Justesse technique** (commandes/flags **vérifiés contre la doc officielle** — jamais
   d'hallucination figée dans un skill ; scripts **testés** ; garde-fous sécurité/coût/confidentialité).
3. **Utilité réelle** (un agent qui déclenche sait-il quoi faire sans deviner ? rapport
   valeur/friction ? pas « joli mais inutile » ?).
Puis **synthétise** les verdicts et **applique** les corrections (ne te contente pas de lister).

### 4. Installer + tracer

- **Installer** : copie le dossier dans `~/.hermes/skills/<slug>/`, puis
  `hermes -p <profil> gateway restart` et `hermes skills list` → vérifie **enabled**.
- **Tracer** : note ce qui a été forgé + où (journal / snapshot), comme toute livraison.

## Convention (toujours pareil, quelle que soit la langue de la source)

- **slug + `name`** : anglais-kebab (`cold-email-grounded`).
- **`description`** : en **anglais**, mais cite les **vraies phrases FR** de déclenchement.
- **corps + docs** : en **français**.
- **commandes / code / noms d'outils** : tels quels.
- **Jamais** de secret dans un skill. **Jamais** de donnée client.

## Pour aller plus loin

- Moteur d'écriture complet (éval, benchmark, optimisation de la description) : skill
  **`skill-creator`** (`npx skills add https://github.com/anthropics/skills --skill skill-creator`).
- Transformer une **vidéo** en skill : la **Forge** du skill `regarder-video`.
