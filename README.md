# hermes-skills

Skill forgé pour **Hermes** (l'agent co-gérant d'Atelier Klar) — format `SKILL.md`,
compatible Hermes (`~/.hermes/skills/`) **et** Claude Code (`~/.claude/skills/`).

## Skill disponible

| Skill | Rôle |
|---|---|
| [`cold-email-grounded`](cold-email-grounded/) | Campagnes de cold email hyper-personnalisées : recherche par prospect → séquence ancrée sur un signal → validation → push Instantly **en pause**. Pilier 1 (acquisition), version « doux et propre ». |

## Installer sur Hermes (VPS)

> ⚠️ Sur le VPS, `$HOME` vaut `/opt/data` par défaut — utiliser les chemins absolus.

```bash
git clone https://github.com/Allan77bot/hermes-skills /tmp/hermes-skills
cp -r /tmp/hermes-skills/cold-email-grounded /home/hermes/.hermes/skills/
export HOME=/home/hermes && /opt/hermes/bin/hermes gateway restart
/opt/hermes/bin/hermes skills list      # doit afficher cold-email-grounded = enabled
```

Redémarrer aussi le(s) gateway(s) par profil concerné(s) :
`hermes -p prospection gateway restart`.

## Mettre à jour un skill

```bash
cd /tmp/hermes-skills && git pull
cp -r /tmp/hermes-skills/cold-email-grounded /home/hermes/.hermes/skills/
export HOME=/home/hermes && /opt/hermes/bin/hermes gateway restart
```

## Garde-fous

- Aucun secret, aucune donnée client dans ce repo (lecture publique).
- Les skills ici *préparent* et *proposent* ; l'humain valide toute action lourde (envoi, push).
