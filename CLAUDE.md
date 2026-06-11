# KiCaféCa — Site Vitrine

## Projet
Site vitrine statique pour le KiCaféCa, local associatif proposant café et ateliers.
Hébergé sur **GitHub Pages** avec le domaine personnalisé `www.kicafeca.fr`.

## Stack technique
- HTML / CSS / JavaScript vanilla (pas de framework — site statique simple)
- Hébergement : GitHub Pages (branche `main`, dossier racine ou `/docs`)
- Domaine : `www.kicafeca.fr` (CNAME à configurer chez le registrar)

## Structure du projet
```
/
├── index.html          # Page d'accueil
├── programmation.html  # Agenda / événements
├── association.html    # Présentation de l'asso
├── css/
│   └── style.css
├── js/
│   └── main.js
├── images/
├── CNAME               # Domaine pour GitHub Pages
└── .gitignore
```

## Conventions
- Pas de dépendance externe si possible (pas de npm, pas de build step)
- Mobile-first, accessible
- Textes en français
- Commits en français ou anglais, pas de mélange dans un même fichier

## Automatisation de programmation.html
Le calendrier mensuel est généré automatiquement depuis un **Google Doc** partagé.

### Script
`scripts/update_programmation.py` — télécharge le Google Doc (export HTML), extrait le tableau, formate les événements via Ollama Cloud et régénère `programmation.html`.

**Usage local :**
```bash
$env:OLLAMA_API_KEY="ta_clé"
py -3 scripts/update_programmation.py
```

**Variables d'environnement :**
| Variable | Obligatoire | Valeur par défaut |
|---|---|---|
| `OLLAMA_API_KEY` | Oui | — |
| `OLLAMA_MODEL` | Non | `kimi-k2.6:cloud` |
| `USE_OLLAMA` | Non | `true` (`false` = texte brut) |

### GitHub Action
`.github/workflows/update-programmation.yml` — lance le script tous les jours à 8h UTC et sur demande manuelle (`workflow_dispatch`).

**Secrets à configurer dans GitHub :**
- `OLLAMA_API_KEY` — clé API Ollama Cloud

### Architecture Ollama
- **Endpoint** : `/api/chat` (pas `/api/generate`) car `kimi-k2.6:cloud` est un modèle *chat/thinking*.
- **Host** : toujours `https://ollama.com`, hardcodé — pas besoin de `OLLAMA_HOST`.
- **Formatage** : une seule requête batch pour tous les événements uniques (éviter 29 requêtes séquentielles).
- **Modèles thinking** : ils raisonnent dans `message.thinking` ; le script tombe back sur ce champ si `message.content` est vide.
- **Piège** : `num_predict` tronquait artificiellement la réponse — **supprimé** du payload.
- **Timeout** : 600 s (10 min) pour laisser le temps au modèle thinking.
- **Post-processing** : normalisation des heures (`17h/21h` → `17h-21h`, `18 H 30` → `18h30`).

### Google Doc source
ID du doc : `1iXZjXpH8-j4PTD1x4FjOXIbGm1VlK3Dp1ajanU1_FRc`  
Le titre doit contenir le mois et l'année (ex: `Programmation - Juin 2026`).

### Fichiers générés (ne pas commiter)
Les fichiers suivants sont créés à chaque exécution pour le debug :
- `scripts/ollama_prompt.txt`
- `scripts/ollama_response.txt`
- `scripts/ollama_raw.json`

## Newsletters
Le site publie une newsletter mensuelle. Structure :
```
NewsLetter/
├── TEMPLATE.html       # Template à copier
├── NL1.html, NL2.html, NL3.html   # Anciennes newsletters (racine)
└── NL4/
    ├── NL4.html        # Newsletter principale
    └── PJ/             # Pièces jointes (plannings, documents)
```

**Pour ajouter une newsletter :** invoquer le skill `/add-newsletter`.
Le skill guide la création du fichier HTML au bon format (chemins `../../css/`, structure sémantique, styles du site) et met à jour `newsletters.html`.

## Déploiement
1. Pousser sur `main`
2. Activer GitHub Pages dans les settings du repo (source : branche `main`, dossier racine)
3. Ajouter `www.kicafeca.fr` comme custom domain dans GitHub Pages settings
4. Chez le registrar DNS : créer un enregistrement CNAME `www` → `<username>.github.io`
