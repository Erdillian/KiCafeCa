(function () {
  'use strict';

  var headerHTML = `
<header class="site-header">
  <div class="container header-inner">
    <a href="/index.html" class="site-branding">
      <img src="/images/Logo.png" alt="Logo KiCaféÇa" width="48" height="48">
      <span class="site-title">KiCaféÇa</span>
    </a>
    <nav class="nav" aria-label="Menu principal">
      <button class="nav-toggle" aria-expanded="false" aria-controls="main-nav" aria-label="Ouvrir le menu">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="3" y1="12" x2="21" y2="12"></line>
          <line x1="3" y1="6" x2="21" y2="6"></line>
          <line x1="3" y1="18" x2="21" y2="18"></line>
        </svg>
      </button>
      <ul class="nav-list" id="main-nav">
        <li class="nav-item"><a class="nav-link" href="/index.html">Accueil</a></li>
        <li class="nav-item"><a class="nav-link" href="/programmation.html">Programmation</a></li>
        <li class="nav-item"><a class="nav-link" href="/association.html">L'association</a></li>
        <li class="nav-item"><a class="nav-link" href="/newsletters.html">Newsletters</a></li>
      </ul>
    </nav>
  </div>
</header>`;

  var footerHTML = `
<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-grid">
        <div class="footer-column footer-brand">
          <img src="/images/Logo.png" alt="Logo KiCaféÇa" width="44" height="44">
          <div>
            <h4>KiCaféÇa</h4>
            <p>Café associatif · Joyeuse</p>
          </div>
        </div>

        <div class="footer-column footer-links">
          <a href="/index.html">Accueil</a>
          <a href="/programmation.html">Programmation</a>
          <a href="/association.html">L'association</a>
          <a href="/newsletters.html">Newsletters</a>
        </div>

        <div class="footer-column footer-contact">
          <a href="mailto:kicafeca@etik.com">kicafeca@etik.com</a>
          <span>ou passez voir au café !</span>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <p>&copy; 2026 KiCaféÇa — Café associatif à Joyeuse, Ardèche</p>
    </div>
  </div>
</footer>

<button class="back-to-top" aria-label="Retour en haut" title="Retour en haut">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M12 19V5"></path>
    <path d="M5 12l7-7 7 7"></path>
  </svg>
</button>`;

  function relativize(html) {
    var path = window.location.pathname;
    var dirs = path.split('/').slice(0, -1).filter(Boolean);
    var prefix = dirs.map(function () { return '../'; }).join('');
    return html.replace(/href="\//g, 'href="' + prefix)
               .replace(/src="\//g, 'src="' + prefix);
  }

  function inject(id, html) {
    var el = document.getElementById(id);
    if (!el) return false;
    el.outerHTML = html;
    return true;
  }

  // Header : synchrone, le script est placé juste après le placeholder
  inject('header-placeholder', relativize(headerHTML));

  // Footer : le placeholder n'existe pas encore au moment de l'exécution,
  // on attend que le DOM soit complet
  if (!inject('footer-placeholder', relativize(footerHTML))) {
    document.addEventListener('DOMContentLoaded', function () {
      inject('footer-placeholder', relativize(footerHTML));
    });
  }
})();
