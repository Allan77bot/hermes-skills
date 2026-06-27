# Push vers Instantly (`instantly-cli`)

Brancher la campagne validée sur Instantly.ai. **Vérifie les flags exacts** avec
`instantly --help` avant de lancer : une CLI évolue, et ces commandes sont un point de départ,
pas une garantie figée.

## Installation

`instantly-cli` est une CLI **communautaire** (pas l'officielle Instantly). Vérifier qu'elle
existe avant de s'y fier — sinon, plan B plus bas :

```bash
npm view instantly-cli version      # existe ? → installer
npm install -g instantly-cli        # global
```

## Clé API

Instantly → **Settings → Integrations → API Keys** → *Create API Key* (la nommer, ex.
`atelier-klar` ; scopes selon le besoin). Stocker en **variable d'environnement** — jamais en
clair dans un fichier tracké :

```bash
export INSTANTLY_API_KEY="…"          # Windows PowerShell : $env:INSTANTLY_API_KEY="…"
```

Vérifier l'auth :

```bash
instantly workspace get --pretty | head -20
```

## Créer la campagne, puis la mettre en pause

⚠️ Il n'existe **pas** de flag « créer en pause » fiable : `campaigns create` ne prend
essentiellement que `--name`. La sécurité ne vient donc PAS d'un flag, mais d'une règle :
**on crée, on met en pause, on n'exécute jamais `activate`** (c'est l'acte d'Allan, dans l'UI).

```bash
# 1) créer (ne s'envoie pas tant que personne ne l'active) — noter l'<id> renvoyé
instantly campaigns create --name "<AAAA-MM-JJ Pilote 20 — …>"
# 2) s'assurer qu'elle est à l'arrêt (idempotent)
instantly campaigns pause <id>
# ⛔ NE JAMAIS lancer : instantly campaigns activate <id>   ← c'est Allan, à la main
```

Réglages sains à viser : text-only, stop on reply, stop on auto-reply, **lien de
désinscription activé**. Séquence à 3 étapes via **merge-tags** (chaque lead reçoit sa copie) :

| Étape | Délai | Sujet | Corps |
|---|---|---|---|
| 1 | J0 | `{{email1_subject}}` | `{{email1_body}}` |
| 2 | +3 j | `{{email2_subject}}` | `{{email2_body}}` |
| 3 | +4 j (= J7) | `{{email3_subject}}` | `{{email3_body}}` |

```bash
instantly campaigns create --name "<AAAA-MM-JJ Pilote 20 — …>" --status paused [flags…]
```

## Charger les leads (avec leur copie perso)

Depuis le fichier **`leads_instantly.json`** (une ligne par lead, champs merge-tags) :

```bash
instantly leads bulk-add --campaign-id <id> --leads "$(cat leads_instantly.json)"
```

Chaque lead porte ses champs `email1_subject`, `email1_body`, `email2_…`, etc.

## Plan B (si `instantly-cli` indisponible)

Si `npm view instantly-cli` ne renvoie rien ou que l'install casse :

- **UI** : Instantly → *New campaign* → importer le CSV enrichi → coller la séquence avec les
  merge-tags. Garder la campagne **en pause**.
- **API REST v2** : `https://api.instantly.ai/api/v2` (créer la campagne, `bulk` leads) via
  `curl` + `INSTANTLY_API_KEY`. Même règle : **ne jamais activer par script**.

## Après le push

1. Ouvrir la campagne dans l'UI Instantly, **relire** sujets + corps rendus.
2. Vérifier le planning d'envoi, les limites (warm-up, volume/jour), l'**auth domaine**
   (SPF/DKIM/DMARC, **domaine secondaire**) et que le **lien de désinscription** est actif.
3. **Allan active.** Le skill *prépare* ; l'humain *envoie*.
