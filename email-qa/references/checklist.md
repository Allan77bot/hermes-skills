# Checklist QA email — critères vérifiables

> La grille complète d'audit d'un email avant envoi. Le **déterministe** est couvert par
> `../scripts/lint_email.py` ; ce fichier ajoute le **jugement** (voix de marque, structure,
> ton) qui ne s'automatise pas. Synthèse de 3 sources : `email-marketing-bible`,
> `email-marketing-skill`, `ai-marketing-claude`.
>
> Sortie attendue : un **verdict par catégorie** (PASS / FAIL + preuve) puis un **GATE final**
> go / no-go. Toujours **citer une preuve** (un extrait de l'email) pour chaque FAIL — jamais
> d'affirmation sans preuve.

## 0. Hard gates — BLOQUER l'envoi si l'un manque

- ❌ **Aucun envoi à > 1 destinataire sans l'accord explicite d'Allan** (même un test = un « oui »).
- ❌ Merge-tag / placeholder non rempli (`{{prénom}}`, `[Société]`).
- ❌ **Lien de désinscription absent** (email marketing chaud) ou lien factice/cassé.
- ❌ Objet vide ou > 60 caractères.
- ❌ **Non-conformité** : pas d'adresse postale (newsletter), base de consentement floue.
- ❌ Authentification d'envoi absente (SPF/DKIM/DMARC) — à vérifier côté infra.

## 1. Délivrabilité

- **SPF + DKIM + DMARC** présents et alignés (DMARC ≥ `p=quarantine` pour du volume).
- **Cold** = texte sobre, pas tout-image. Gmail/Gemini **résument depuis les 150-200 premiers
  caractères de live-text** → mettre l'intention en texte réel en tête (jamais headline en image).
- **Ratio image/texte raisonnable**, images < 200 KB (≈ < 800 KB total), `alt` sur chaque image.
- **Personnalisation = exigence de délivrabilité** (le texte 100 % IA non personnalisé est
  filtré plus durement) — mais segments vérifiés contre les vrais comptes.
- Domaines séparés par usage (cold ≠ transactionnel ≠ marketing) ; warm-up si identité neuve.

## 2. Objet & preheader

- Objet **≤ 50 car. (idéal < 45)**, mots importants en premier, honnête (pas de bait-and-switch).
- **Pas de faux `Re:` / `Fwd:`**. **0 ou 1 emoji** max.
- **Preheader présent** et apporte une info (ne répète pas l'objet).
- Si l'objet contient un prénom, vérifier le budget caractères (la perso mange l'objet).

## 3. Structure & lisibilité

- **One Email, One Job** : une idée, une action voulue.
- **Mobile-first** : colonne unique ≤ 600px, paragraphes courts, scannable en 5 s, pyramide
  inversée (le message clé d'abord). « Écris puis coupe 30 % ».
- Anatomie attendue : objet → preheader → from-name → accroche → corps → **CTA** → (P.S.).
- **Dark-mode safe** (pas de fond `#000` pur ni logo `#fff`).

## 4. CTA

- **Un seul CTA principal** (le multi-CTA tue le taux de clic). Secondaires visuellement subordonnés.
- CTA **spécifique** (« Réserver un créneau » > « Cliquez ici »), bouton > lien texte.
- **Pour le nurturing Atelier Klar : le CTA pousse vers le RDV**
  `https://calendar.app.google/xzUHcfMkbrhRNPYz9`. Soft, jamais forcé.

## 5. Personnalisation / merge-tags

- **Tout merge-tag a un fallback** (interdiction de « Bonjour , »).
- Syntaxe conforme à l'outil cible. Pas de tag résiduel non rendu.
- Personnalisation là où elle ajoute (comportement, étape de cycle) ; prénom dans ~20-30 % des
  envois, pas partout.

## 6. Voix & marque (cohérence Atelier Klar)

- **Relire l'artefact de marque** (`BRAND-VOICE.md` / skill `atelier-klar-design` + `copywriting`)
  et **conformer chaque email** à la voix documentée. Pas d'artefact → le signaler.
- **Voice chart IS / IS NOT** : l'email penche vers la colonne IS (Confiant≠Arrogant,
  Utile≠Condescendant, Clair≠Simpliste, Audacieux≠Agressif), jamais IS NOT.
- Vocabulaire « We use / We avoid » respecté ; tournures cohérentes avec l'archétype de marque.
- **Design visuel** (couleurs, typo, logo, espacements) : c'est le job du skill
  `atelier-klar-design` — vérifier qu'il a bien été appliqué pour le **chaud** (HTML brandé).
  Le **cold** reste sobre (texte).

## 7. Anti « AI slop » (sonner humain)

- **Blacklist de mots** (delve, leverage, foster, seamless, robust, furthermore… + clichés FR) →
  `lint_email.py` les signale.
- **Empreintes syntaxiques IA** : « ce n'est pas X, c'est Y » (**max 1**), triplettes
  d'adjectifs de remplissage, évitement du verbe « être ».
- **Spécificité** = l'humaniseur le moins cher : **un vrai chiffre / nom / date** par email.
- **Une opinion défendable** par email (l'IA est trop lisse). **Burstiness** : alterner phrases
  longues et courtes. Test « lis à voix haute ».
- Tirets cadratins : tic d'IA → à retirer du corps.

## 8. Conformité (rappel)

- Lien de désinscription **one-click** (RFC 8058 pour le volume), honoré vite.
- **Adresse postale** (newsletter). From-name = marque, reply-to **monitoré** (pas `noreply@`).
- Base légale : B2B « intérêt légitime » (FR/UE), opt-in pour B2C. L'IA ne transfère pas la
  responsabilité — Allan reste responsable.

---

## Format de verdict à rendre

```markdown
## QA email — <destinataire / type>
- Délivrabilité : PASS/FAIL — <preuve>
- Objet & preheader : PASS/FAIL — <preuve>
- Structure & lisibilité : PASS/FAIL — <preuve>
- CTA : PASS/FAIL — <preuve>
- Personnalisation : PASS/FAIL — <preuve>
- Voix & marque : PASS/FAIL — <preuve>
- Anti AI-slop : PASS/FAIL — <preuve>
- Conformité : PASS/FAIL — <preuve>

**Top corrections** (priorisées) : 1… 2… 3…
**GATE : GO / NO-GO** (NO-GO si un seul hard gate échoue)
```
