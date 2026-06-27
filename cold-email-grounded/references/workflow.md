# Workflow détaillé — cold email grounded

Le pipeline exécutable, étape par étape, avec le prompt d'orchestration à donner à l'agent et
le format des livrables.

## 0. Entrée : la liste de leads (CSV)

**D'où vient la liste ?** Export Apollo / LinkedIn Sales Navigator / scraping. Colonnes
minimales viables : `First Name, Company, Website, Email` (+ `Title, LinkedIn URL` pour
nourrir la recherche). `Email` n'est requis que pour le push final, pas pour la recherche du
pilote.

Colonnes complètes (s'en approcher ; adapter aux données réelles) :
`First Name, Last Name, Company, Website, Email, LinkedIn URL, Title, Phone, Decision Maker Score, Segment`

**Pour le pilote (20 leads), pas besoin de venv ni de `polars`** : le module `csv` de la
stdlib suffit. Réserver `polars` (rapide) au **scaling** (1000+ leads) :

```bash
python -m venv .venv && source .venv/bin/activate   # Windows : .venv\Scripts\activate
pip install polars
```

## 1. Cadrer l'offre

Avant d'écrire le moindre mail, l'agent doit savoir **ce qu'on vend** et **l'angle de
valeur**. Deux voies : rechercher le site de la boîte (ex. via `firecrawl` / web fetch), ou
demander à Allan en une phrase. Sans offre claire, les mails sonnent creux.

## 2. Recherche PAR PROSPECT (en parallèle)

Pour chaque lead, lancer une **recherche indépendante** (sous-agents en parallèle, ~10 à la
fois pour ne pas saturer) : comprendre l'entreprise + le rôle de la personne, et trouver **UN
signal récent et concret**.

Signaux qui marchent (du plus fort au plus faible) :

1. **Levée de fonds** récente.
2. **Recrutement** révélateur — une offre d'emploi qui trahit une douleur (« on cherche un
   SDR » = douleur prospection).
3. **Lancement produit / annonce.**
4. **Post / prise de parole** récente de la personne.
5. **Signal sectoriel** (déduit — voir « inféré » plus bas).

Le signal doit permettre une 1ʳᵉ ligne que **seule cette personne** pourrait recevoir.

## 3. Écrire la séquence (3 touches)

Séquence par défaut : **J0 / J+3 / J+7** (3 mails). Chaque mail suit les règles de copie (→
`copy-rules.md`) et s'ancre sur le signal trouvé. Les relances (mail 2, 3) apportent un
**nouvel angle**, pas un « je relance ».

## 4. Valider

Faire tourner le script de checks (→ `../scripts/validate_emails.py`) sur le JSON des mails.
Corriger les échecs durs (sujet trop long/vide, phrases bannies FR+EN, merge-tag non rempli,
corps > 100 mots) avant de livrer. Marquer chaque lead `signal_confidence` = `verified` ou
`inferred`.

## 5. Livrables de revue

Produire **trois** sorties (l'humain lit la première) :

- `emails/pilot_review.md` — **lisible** : par lead, le résumé de recherche (signal, source,
  confiance, hypothèse de douleur, angle) puis les 3 mails (sujet + corps). C'est ce qu'Allan
  relit.
- `leads/pilot_enriched.csv` — le CSV d'origine + colonnes de recherche + colonnes mails
  (`subject_1, body_1, subject_2, body_2, …`, `signal_used`, `signal_confidence`,
  `research_notes`).
- `emails/pilot_emails.json` — **liste plate** `{lead, step, subject, body}` (une entrée par
  mail) → c'est ce que **mange le script de validation**.
- `leads/leads_instantly.json` — **une ligne par lead** avec les champs merge-tags
  (`email1_subject`, `email1_body`, `email2_…`, …) → c'est ce que **mange Instantly**
  (`bulk-add`). Dérivé du précédent. (Deux formats distincts : ne pas les confondre.)

## 6. Pousser dans Instantly

Après validation humaine → `instantly.md`. On crée la campagne **puis on la met en pause** ;
on n'active **jamais** par script (c'est l'acte d'Allan dans l'UI).

---

## Le prompt d'orchestration (gabarit)

C'est la checklist que l'agent qui exécute ce skill doit suivre (toi, Claude Code, ou Hermes) —
adapter les `<…>` :

```
Tu vas générer une campagne de cold email grounded-in-research.

OFFRE : <ce qu'on vend + angle de valeur, 2-3 phrases>
LEADS : <chemin du CSV> (colonnes : First Name, Last Name, Company, Website, Title, …)
ÉCHELLE : commence par un PILOTE de 20 leads. On scalera après ma relecture.

ÉTAPES :
1. Mets en place un venv Python + polars. Charge le CSV, sélectionne 20 leads.
2. Pour chaque lead, en parallèle (≤10 à la fois) : recherche entreprise + rôle, trouve UN
   signal récent et concret. Note la source et si c'est vérifié ou inféré.
3. Écris une séquence de 3 mails (J0/J+3/J+7) par lead, ancrée sur le signal.
   Règles : <100 mots, format mobile, 1ʳᵉ ligne spécifique, pas de small talk, pas de
   "hope this finds you well", valeur = temps/argent, CTA soft, sujet <60 car., chaque mail
   unique. Pas de tirets cadratins.
4. Valide la copie : LANCE python <dossier-du-skill>/scripts/validate_emails.py sur le JSON
   et corrige jusqu'à 0 échec dur (ne te contente pas de relire à l'œil). Marque
   signal_confidence (verified/inferred) par lead.
5. Sors : un Markdown de revue lisible + un CSV enrichi + le JSON plat (validation) + le JSON
   merge-tags (Instantly).

Confirme d'abord que tu as compris et propose un plan concret AVANT d'agir.
N'envoie rien : la campagne Instantly sera créée EN PAUSE, j'active moi-même.
```

> Le « confirme avant d'agir » et le « rien ne part sans moi » ne sont pas optionnels : c'est
> ce qui garde l'humain dans la boucle sur une action qui parle **en ton nom**.
