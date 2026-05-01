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

## Déploiement
1. Pousser sur `main`
2. Activer GitHub Pages dans les settings du repo (source : branche `main`, dossier racine)
3. Ajouter `www.kicafeca.fr` comme custom domain dans GitHub Pages settings
4. Chez le registrar DNS : créer un enregistrement CNAME `www` → `<username>.github.io`
