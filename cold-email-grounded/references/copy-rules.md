# Règles de copie — cold email grounded

Le mail vit ou meurt sur ces règles. Elles viennent toutes de la même logique : **gagner une
réponse**, pas conclure une vente. Tu cherches le réflexe *« attends, comment ils savent
ça ? »*.

## Les règles

- **Langue** : celle du prospect — **français par défaut** pour Atelier Klar (les phrases
  bannies et le validateur couvrent FR + EN).
- **< 100 mots.** Personne ne lit un pavé d'un inconnu. Vise 80-100 mots de corps.
- **Format mobile.** Lignes courtes, espaces blancs. La majorité lit sur téléphone.
- **La 1ʳᵉ ligne fait tout.** Spécifique au prospect, ancrée sur le signal. Si elle pourrait
  être envoyée à 1000 personnes, recommence.
- **Zéro small talk.** Pas de « j'espère que ce mail vous trouve bien », pas de « j'ai vu que
  votre boîte fait de belles choses », pas de flatterie LinkedIn.
- **Un seul axe de valeur** : *gagner du temps · gagner de l'argent · faire de l'argent*.
- **CTA soft.** Une question low-friction (« ça vaut un échange ? »), pas « réservez un
  créneau de 30 min ». Ton conversationnel, jamais corporate.
- **Sujet < 60 caractères**, spécifique, donne envie d'ouvrir sans clickbait.
- **Chaque mail unique** = rôle + entreprise + **un signal précis**.

## Anatomie d'un mail

```
Sujet : <court, spécifique, < 60 car.>

<1ʳᵉ ligne : le signal — la preuve que tu as fait tes devoirs sur LUI>
<2-3 lignes : le pont signal → douleur probable → ce que tu fais (valeur, 1 axe)>
<CTA soft : une question facile à dire oui>

<prénom>
```

## Phrases bannies (l'IA les adore, les prospects les détestent)

**EN** : `hope this finds you well` · `just following up` · `circle back` · `touch base` ·
`deep dive` · `pick your brain` · `reach out` · `low-hanging fruit` · `move the needle` ·
`synergy` · `game changer` · `I came across your profile` · `love what you're doing`

**FR** : `j'espère que ce mail vous trouve bien` · `j'espère que vous allez bien` · `je me
permets de vous contacter` · `je me permets de revenir vers vous` · `je reviens vers vous` ·
`n'hésitez pas à`

Le script `scripts/validate_emails.py` détecte ces deux listes (FR + EN) automatiquement.

## L'« AI slop » à traquer

L'IA a des tics qui sentent le robot à plein nez :

- **Tirets cadratins** `—` et doubles tirets `--` partout → remplace par une virgule, un
  point, ou des parenthèses.
- **Phrases trop lisses / symétriques** (« non seulement…, mais aussi… »).
- **Sur-promesse** (« +300 % de réponses garanties ») → crédibilité détruite.
- **Faux signaux** : ne jamais inventer un fait sur le prospect. Pas de signal vérifié → un
  signal inféré honnête, jamais un mensonge.

## Exemple

**Mauvais (générique) :**
Input : prénom + entreprise insérés au chausse-pied.
Output : « Bonjour Marc, j'espère que ce mail vous trouve bien. J'ai vu que TechCorp fait de
belles choses. On aide les entreprises comme la vôtre à grandir. Vous avez 30 min ? »

**Bon (ancré) :**
Output : « Marc — vu que TechCorp recrute 3 SDR ce trimestre. Vos AE font donc encore du
full-cycle : du temps de closer cher passé à prospecter. On installe des systèmes d'outbound
qui amènent des RDV tièdes aux AE, sans recruter. Ça vaut un échange ? »

*(Et même dans le bon exemple : le `—` après « Marc » serait à retirer en prod — c'est
justement le tic d'AI slop que le script signale.)*
