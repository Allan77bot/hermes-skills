# Passe qualité — relire un skill sous 3 angles

> Référence de `skill-forge`. Avant de livrer un skill, fais-le relire par **Claude Code**
> sous **trois angles orthogonaux** : un relecteur unique ne voit qu'une face ; trois mandats
> distincts attrapent des défauts qu'aucun ne verrait seul (un skill peut être techniquement
> juste *et* imbuvable, ou élégant *et* inutile en vrai).

## Comment lancer

Idéalement **3 sous-agents Claude Code en parallèle**, un par angle, chacun reçoit le draft
complet du skill + le contexte (à quoi il sert, qui le déclenchera). Si pas de sous-agents :
une relecture séquentielle des 3 angles. Puis **toi tu synthétises** (pas 3 pavés bruts) :
fusionne, hiérarchise (bloquant / important / cosmétique), applique.

## Format de verdict (imposé)

```markdown
## Verdict — <angle>
**Points forts** : ce qui est déjà bon, à garder.
**Problèmes** : liste, chacun étiqueté [bloquant] / [important] / [cosmétique].
**Corrections concrètes** : le fix précis par problème (pas « améliorer la clarté » mais
  « remplace X par Y parce que Z »).
**Verdict global** : prêt / à retoucher / à repenser.
```

## Angle 1 — Structure & déclenchement

- `SKILL.md` **lean** (< 500 lignes) ? Détail bien repoussé en `references/` ?
- **Zéro redite, zéro remplissage** : chaque phrase tire son poids ?
- **`description`** nette et « pushy » : couvre *quoi* + *quand* avec de vraies phrases de
  déclenchement + un « Do NOT trigger for » ? Risque de sous- / sur-déclenchement ?
- Pointeurs explicites (« lis X quand Y ») ? Rien qui fasse **perdre du temps** au modèle
  (instructions vagues, étapes inutiles, contradictions internes) ?

## Angle 2 — Justesse technique

- Les techniques sont-elles de la **bonne pratique actuelle**, ou du périmé ?
- Quelque chose de **factuellement faux** ou trop beau pour être vrai ?
- **Commandes, flags, noms d'outils, modèles** : exacts **ET vérifiés contre la doc
  officielle** ? (Une source peut faire halluciner un flag plausible mais faux — un skill
  figerait l'erreur.)
- Les **scripts** sont-ils **testés** (lancés au moins une fois) et corrects ?
- Manque-t-il un **garde-fou** évident (sécurité, coût, confidentialité, rate-limit, conformité) ?
- Le skill **explique-t-il le pourquoi** (robuste quand le contexte change) ?

## Angle 3 — Utilité réelle

- Un agent qui déclenche ce skill **sait-il quoi faire, pas à pas, sans deviner** ?
- Colle-t-il aux **habitudes** et règles de l'utilisateur (langue, conventions, garde-fous) ?
- Le **déclencheur** matche-t-il ce qu'il **taperait réellement** ?
- Est-ce **« joli mais inutile »** — ferait-il moins bien que l'agent sans skill ? Si oui, dis-le.
- Le rapport **valeur / friction** est-il bon ? (10 étapes pour un gain marginal = mauvais skill.)

## Garde-fous de la relecture

- Le panel sert à **durcir**, pas à **gonfler**. Si les 3 angles sont satisfaits, **arrête** —
  ne fabrique pas des problèmes pour justifier une passe de plus.
- Un « à repenser » sur un point central justifie une vraie réécriture, pas un patch cosmétique.
