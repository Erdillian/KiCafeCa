# Plan d'attaque — Branche MaJuillet

## Objectif
Implémenter 3 chantiers en parallèle sur le site vitrine KiCaféCa.

---

## Chantier 1 : Générateur d'affiches — PDF sans friction

**But :** le background de l'affiche doit s'intégrer directement au PDF, sans que l'utilisateur ait à cocher "Imprimer les arrière-plans".

**Approche :** quick-win CSS (`print-color-adjust: exact` / `-webkit-print-color-adjust: exact` / `color-adjust: exact`) appliqué sur `.sheet` et les éléments colorés.

**Fichiers concernés :**
- `generateur-affiches.html`

**Tâches :**
1. Ajouter `print-color-adjust: exact` dans la règle `@media print` pour `.sheet`, `.band`, `.title-block`, `.footer-block`.
2. Vérifier que le hint texte mentionne maintenant simplement "Enregistrer en PDF" sans l'astuce "print backgrounds".

**Subagent :** `agent-affiches`

---

## Chantier 2 : Navigation "L'association" + page "Comment s'investir ?"

**But :**
- Transformer "L'association" en dropdown (même comportement que "Média").
- Renommer `association.html` en `qui-sommes-nous.html`.
- Créer une nouvelle page `comment-s-investir.html`.
- Conserver une redirection automatique depuis `association.html` vers `qui-sommes-nous.html` pour les liens directs (emails, signets, etc.).
- Mettre à jour tous les liens internes.

**Fichiers concernés :**
- `js/components.js` (header + footer)
- `association.html` → `qui-sommes-nous.html` (`git mv`)
- `comment-s-investir.html` (création)
- `association.html` (redirection HTML meta refresh)
- `newsletters.html` (lien vers association)
- `index.html` (éventuels liens)
- `NewsLetter/NL5/NL5.html` (éventuels liens)
- `NewsLetter/NL6/NL6.html` (liens futurs)

**Tâches :**
1. `git mv association.html qui-sommes-nous.html`
2. Créer `comment-s-investir.html` en s'inspirant visuellement de `qui-sommes-nous.html` avec une structure claire : pourquoi s'investir, comment proposer un atelier, réunions d'adhérents, dons/matériel/bénévolat, contact.
3. Créer un nouveau `association.html` minimal avec une redirection `meta refresh` vers `qui-sommes-nous.html`.
4. Mettre à jour `js/components.js` :
   - remplacer le lien "L'association" par un dropdown identique à "Média"
   - liens : "Qui sommes-nous ?" → `/qui-sommes-nous.html`, "Comment s'investir ?" → `/comment-s-investir.html`
   - mettre à jour le footer
5. Mettre à jour les liens internes dans `index.html`, `newsletters.html`, et les newsletters web NL4/NL5/NL6.

**Subagent :** `agent-association`

---

## Chantier 3 : Newsletter NL6 (version web)

**But :** créer la version web de la newsletter de Juillet 2026, sans toucher à `NewsLetter/NL6.html` (version email / canvas de l'utilisateur).

**Méthode :** utiliser le skill `/add-newsletter` qui guide la création du fichier HTML au bon format (chemins `../../css/`, structure sémantique, styles du site) et met à jour `newsletters.html`.

**Contenu source :** `NewsLetter/NL6.html` (email). À adapter en version web sans modifier le fichier source.

**Sections à reprendre :**
1. Intro
2. Temps fort : Jeudi 16 juillet, anniversaire Laurie + soirée conviviale
3. Ce qui change cet été : fin mercredi café libre, nouvelles pages site
4. On construit la suite ensemble : horizontalité, réunions d'adhérents, fête 6 mois
5. Retour sur juin : semaine fiertés, Académie Libre et Éclairé, Jam Session
6. On cherche ! : matériel, coup de main façade
7. Note adhésion

**Fichiers concernés :**
- `NewsLetter/NL6/NL6.html` (création via `/add-newsletter`)
- `newsletters.html` (mise à jour automatique par le skill)
- Potentiellement `NewsLetter/NL6/PJ/` si une pièce jointe est ajoutée plus tard

**Tâches :**
1. Invoquer `/add-newsletter` en fournissant :
   - numéro : NL6
   - mois/année : Juillet 2026
   - contenu adapté depuis `NewsLetter/NL6.html`
   - lien vers le planning du mois si disponible
2. Vérifier le résultat du skill et ajuster si nécessaire.
3. S'assurer que `NewsLetter/NL6.html` (email) n'a pas été modifié.

**Exécution :** ce chantier est lancé **dans le main flow** par invocation directe du skill `/add-newsletter`, car les skills ne peuvent pas être invoqués depuis les subagents.

---

## Exécution parallèle

1. Lancer en parallèle :
   - `agent-affiches` (Chantier 1)
   - `agent-association` (Chantier 2)
   - invocation du skill `/add-newsletter` dans le main flow (Chantier 3)
2. Une fois terminés, vérifier l'absence de conflits et la cohérence globale.
3. Vérifier les liens internes et les chemins.
4. Commit final sur `MaJuillet`.

## Non-régression
- Ne pas modifier `NewsLetter/NL6.html` (version email).
- Ne pas supprimer `association.html` sans redirection.
- Conserver le style mobile-first et les chemins relatifs.

## Non-régression
- Ne pas modifier `NewsLetter/NL6.html` (version email).
- Ne pas supprimer `association.html` sans redirection.
- Conserver le style mobile-first et les chemins relatifs.
