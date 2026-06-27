---
name: cold-email-grounded
description: >-
  Use when Allan wants to run an AI-driven cold email / outbound campaign that is genuinely
  personalized at scale — researching each prospect, writing a multi-touch sequence grounded
  in ONE specific signal, validating the copy, then pushing it to a sending platform (e.g.
  Instantly) created PAUSED for human review. This is the SynkroniseIA / Atelier Klar
  acquisition playbook (Pilier 1). Trigger it whenever Allan mentions outbound or prospecting
  work, even without naming a tool or this skill. Triggers (FR) : « campagne cold email »,
  « fais une campagne de prospection », « génère des mails de prospection personnalisés »,
  « outreach B2B », « séquence de mails froids », « campagne d'acquisition », « contacte ces
  prospects », « écris des cold emails », « j'ai une liste de leads / un CSV de prospects »,
  « Instantly ». Do NOT trigger for: warm emails to existing customers/clients, newsletters or
  marketing broadcasts, transactional emails, replying inside an existing thread, or pure
  copywriting with no research/outbound context.
---

# Cold email *grounded-in-research*

> Fabriquer des campagnes de cold email **hyper-personnalisées à l'échelle** : un agent
> recherche chaque prospect, écrit une séquence **ancrée sur un signal précis**, valide la
> copie, puis prépare la campagne **en pause** pour relecture humaine. Méthode en français,
> code/commandes en anglais.

## Pourquoi (la thèse)

Le cold email impose d'habitude un compromis : **volume** (mails génériques — ça scale mais
ça ne convertit pas) **ou** personnalisation (ça convertit mais ça ne scale pas, fait à la
main). Un agent IA casse ce compromis : il fait, à grande vitesse, la **recherche par
prospect** que feraient des assistants.

L'objectif n'est **pas** de vendre dans le premier mail. C'est **cold → warm** : gagner une
réponse en provoquant le réflexe **« attends, comment ils savent ça ? »**. Si le prospect
*sent* que tu as fait tes devoirs sur lui précisément, il répond. Sinon, c'est du spam.

**La règle qui gouverne tout :** *est-ce que ce message crée assez de pertinence et de valeur
pour donner envie de répondre ?* Si la 1ʳᵉ ligne pourrait être copiée-collée à 1000
personnes, c'est raté.

## Le pipeline (vue d'ensemble)

```
liste de leads (CSV)
   │
   ▼ 1. Cadrer l'offre   — que vend-on ? quel angle de valeur ? (rechercher le site, ou demander à Allan)
   │
   ▼ 2. Recherche PAR PROSPECT, en parallèle   — 1 signal récent et concret par lead
   │
   ▼ 3. Écrire la séquence   — 3 touches (J0 / J+3 / J+7), ancrées sur le signal, règles de copie
   │
   ▼ 4. Valider   — script de checks (longueur, phrases bannies, CTA, sujet) + signaux vérifiés vs inférés
   │
   ▼ 5. Livrables de revue   — Markdown lisible + CSV enrichi + JSON
   │
   ⛳ RELECTURE HUMAINE   (Allan lit, corrige, approuve)
   │
   ▼ 6. Pousser dans Instantly   — campagne créée EN PAUSE, rien ne part sans activation explicite
```

Détail exécutable de chaque étape + le prompt d'orchestration à donner à l'agent + le format
des fichiers → **`references/workflow.md`**.

## Toujours commencer par un pilote

Avant de traiter 1000 leads, faire un **pilote de ~20**. Ça coûte presque rien et ça révèle
vite si l'offre / l'angle / les signaux tiennent. On scale **après** que le pilote a été relu
et validé. (Pour Hermes : c'est aussi la règle « on démarre **doux et propre** » — pas de
gros volume agressif au lancement.)

## Les règles de copie (le cœur)

Résumé — détail, phrases bannies, anatomie d'un mail, exemples → **`references/copy-rules.md`** :

- **Langue** : celle du prospect — **français par défaut** pour Atelier Klar.
- **< 100 mots**, format **mobile** (lignes courtes, espaces blancs).
- **La 1ʳᵉ ligne fait tout** : spécifique, ancrée sur le signal. Zéro small talk, zéro
  « j'espère que ce mail vous trouve bien », zéro flatterie LinkedIn.
- Valeur cadrée sur **un** axe : *gagner du temps · gagner de l'argent · faire de l'argent*.
- **CTA soft** (question low-friction), ton conversationnel, jamais corporate.
- **Chaque mail unique** = rôle de la personne + entreprise + **un signal précis**.
- **Sujet < 60 caractères.**

## Valider avant de livrer

Chaque mail passe des **checks objectifs** — lance le script fourni (déterministe,
réutilisable) plutôt que de relire à l'œil. `<skill>` = le dossier de ce skill :

```bash
python "<skill>/scripts/validate_emails.py" emails.json
```

Il vérifie : nombre de mots, **phrases bannies (FR + EN)**, **merge-tags non remplis**
(`{{…}}`, `[Société]`), présence d'un **CTA soft**, longueur du sujet, et signale les
**tirets cadratins** (`—` / `--`) — la signature n°1 de l'« AI slop ». Corriger jusqu'à
**0 échec dur** avant de livrer.

## Discipline qualité : vérifié vs inféré

Tous les signaux ne se valent pas. Marquer chaque lead :

- **Signal vérifié** (levée de fonds, recrutement, lancement, post récent — **sourcé**) → à
  envoyer en premier, c'est ce qui fait *« comment ils savent ça ? »*.
- **Signal inféré** (déduit du secteur / rôle, sans source) → contexte crédible, **pas** une
  actu. À relire de façon critique avant d'envoyer.

Mettre un champ `signal_confidence` dans le CSV. **Ne jamais inventer un fait** sur un
prospect : un faux signal détruit la confiance plus vite que pas de signal du tout.

## Pousser dans Instantly

Setup + commandes (`instantly-cli`, clé API en variable d'env, création de campagne, ajout
des leads) → **`references/instantly.md`**.

**Non négociable :** on **n'active jamais** une campagne par script. On la crée, on la met en
pause, et c'est **Allan** qui l'active dans l'UI. (Il n'existe pas de flag « créer en pause »
fiable : la sécurité, c'est *ne jamais lancer `activate`*.) Le push *prépare* ; **l'humain
envoie**.

## Garde-fous

- **Relecture humaine obligatoire** avant tout envoi. L'IA propose, Allan valide ; on n'active
  jamais une campagne par script.
- **Conformité UE (cold email B2B)** : base légale = *intérêt légitime* (message lié à la
  fonction pro du destinataire), **lien de désinscription visible obligatoire** (le configurer
  dans Instantly), pas de B2C sans opt-in. L'opt-out en un clic est aussi une exigence de
  délivrabilité (règles expéditeurs Google/Yahoo).
- **Délivrabilité** : **SPF/DKIM/DMARC** en place ; envoyer depuis un **domaine secondaire**
  (jamais le principal) ; warm-up actif ; respecter le volume/jour. L'IA peut générer 1000
  mails ; ton domaine ne peut pas tous les envoyer d'un coup.
- **Données prospects = données réelles.** Jamais dans le **free tier** d'une IA qui pourrait
  s'en servir pour s'entraîner (règle Atelier Klar : pas de données client / org en free tier).
  Recherche par sources publiques, oui ; déverser le CRM dans un outil gratuit, non.
- **Coût** : la recherche par prospect en parallèle consomme des tokens. Piloter petit, scaler
  conscient du coût.
- **Pour Hermes** : c'est le **Pilier 1 (acquisition)** — mais « doux et propre », et **seul
  Allan déclenche** un envoi (cf. `manifeste-soul-hermes.md`).
