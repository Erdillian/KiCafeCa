/**
 * KiCaféCa — JavaScript principal
 * Gestion du menu hamburger, highlight de la page active et bouton Back to Top
 */

(function () {
  'use strict';

  // --- 1. Toggle menu hamburger mobile ---

  function initNavToggle() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-list');

    if (!navToggle || !navMenu) {
      return;
    }

    // Écouter le clic sur le bouton hamburger
    navToggle.addEventListener('click', function () {
      const isActive = navMenu.classList.toggle('active');
      navToggle.setAttribute('aria-expanded', isActive ? 'true' : 'false');
      if (isActive) {
        const firstLink = navMenu.querySelector('.nav-link');
        if (firstLink) firstLink.focus();
      }
    });

    // Fermer le menu au clic sur un lien (mobile)
    navMenu.querySelectorAll('.nav-link').forEach(function (link) {
      link.addEventListener('click', function () {
        navMenu.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // --- 2. Highlight de la page active dans la nav ---

  function setActivePage() {
    // Récupérer le nom du fichier courant
    const currentPath = window.location.href;
    const navLinks = document.querySelectorAll('.nav-link');

    if (!navLinks) {
      return;
    }

    // Comparer chaque lien avec la page courante
    navLinks.forEach(function (link) {
      const linkHref = link.getAttribute('href');

      if (currentPath.includes(linkHref)) {
        link.classList.add('active');
      } else {
        link.classList.remove('active');
      }
    });
  }

  // --- 3. Bouton Back to Top ---

  function initBackToTop() {
    const backToTopBtn = document.querySelector('.back-to-top');

    if (!backToTopBtn) {
      return;
    }

    let scrolled = false;

    // Écouter le scroll de la page
    window.addEventListener('scroll', function () {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

      // Afficher le bouton après 300px de scroll
      if (scrollTop > 300) {
        if (!scrolled) {
          backToTopBtn.classList.add('show');
          scrolled = true;
        }
      } else {
        if (scrolled) {
          backToTopBtn.classList.remove('show');
          scrolled = false;
        }
      }
    });

    // Gérer le clic sur le bouton
    backToTopBtn.addEventListener('click', function (e) {
      e.preventDefault();

      // Scroll smooth vers le haut
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // --- Initialisation ---
  function init() {
    initNavToggle();
    setActivePage();
    initBackToTop();
  }

  // Attendre que le DOM soit chargé
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
