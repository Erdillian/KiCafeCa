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
