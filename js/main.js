/* ═══════════════════════════════════════════
   Dra. Thielen — Shared JS
   ═══════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  // ── HEADER SCROLL ──
  const header = document.getElementById('header');
  if (header) {
    const onScroll = () => header.classList.toggle('scrolled', window.scrollY > 60);
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ── ACTIVE NAV LINK ──
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('nav a, .mobile-menu a').forEach(a => {
    const href = a.getAttribute('href') || '';
    if (href && href !== '#' && currentPath.includes(href.replace('../', '').replace('./', ''))) {
      a.classList.add('active');
    }
  });

  // ── MOBILE MENU ──
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobileMenu');
  const mobileClose = document.getElementById('mobileClose');
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      mobileMenu.classList.add('open');
      hamburger.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden';
      // Focus first link for keyboard users
      const firstLink = mobileMenu.querySelector('a');
      if (firstLink) setTimeout(() => firstLink.focus(), 50);
    });
  }
  if (mobileClose && mobileMenu) {
    mobileClose.addEventListener('click', closeMobileMenu);
  }
  // Close on Escape key
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && mobileMenu && mobileMenu.classList.contains('open')) {
      closeMobileMenu();
      if (hamburger) hamburger.focus();
    }
  });
  // Close on link click
  if (mobileMenu) {
    mobileMenu.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMobileMenu));
  }

  // ── INTERSECTION OBSERVER (animações de entrada) ──
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const animEls = document.querySelectorAll('.fade-up, .fade-left, .fade-right, .scale-in');
  if (animEls.length) {
    if (prefersReducedMotion) {
      animEls.forEach(el => el.classList.add('visible'));
    } else {
      const obs = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            obs.unobserve(entry.target);
          }
        });
      }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
      animEls.forEach(el => obs.observe(el));
    }
  }

  // ── LIGHTBOX ──
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightboxImg');
  if (lightbox && lightboxImg) {
    let currentIdx = 0;
    let images = [];

    window.openLightbox = (idx, imgs) => {
      images = imgs || [];
      currentIdx = idx;
      lightboxImg.src = images[currentIdx];
      lightbox.classList.add('open');
      document.body.style.overflow = 'hidden';
    };
    window.closeLightbox = () => {
      lightbox.classList.remove('open');
      document.body.style.overflow = '';
    };
    window.lightboxNav = (dir) => {
      currentIdx = (currentIdx + dir + images.length) % images.length;
      lightboxImg.src = images[currentIdx];
    };
    lightbox.addEventListener('click', e => { if (e.target === lightbox) window.closeLightbox(); });
    document.addEventListener('keydown', e => {
      if (!lightbox.classList.contains('open')) return;
      if (e.key === 'Escape') window.closeLightbox();
      if (e.key === 'ArrowLeft') window.lightboxNav(-1);
      if (e.key === 'ArrowRight') window.lightboxNav(1);
    });
  }

  // ── COOKIE BANNER (deferred to after page load) ──
  if (!localStorage.getItem('cookieConsent')) {
    window.addEventListener('load', () => {
      setTimeout(() => {
        const banner = document.createElement('div');
        banner.id = 'cookie-banner';

        const p = document.createElement('p');
        p.textContent = 'Utilizamos cookies para melhorar sua experiência de navegação. Ao continuar, você concorda com nossa ';
        const link = document.createElement('a');
        link.href = '/politica-de-privacidade.html';
        link.textContent = 'Política de Privacidade';
        p.appendChild(link);
        p.appendChild(document.createTextNode('.'));

        const btns = document.createElement('div');
        btns.className = 'cookie-btns';

        const btnDecline = document.createElement('button');
        btnDecline.className = 'cookie-btn-decline';
        btnDecline.textContent = 'Recusar';

        const btnAccept = document.createElement('button');
        btnAccept.className = 'cookie-btn-accept';
        btnAccept.textContent = 'Aceitar cookies';

        btns.appendChild(btnDecline);
        btns.appendChild(btnAccept);
        banner.appendChild(p);
        banner.appendChild(btns);
        document.body.appendChild(banner);

        setTimeout(() => banner.classList.add('visible'), 300);

        const dismissBanner = (choice) => {
          localStorage.setItem('cookieConsent', choice);
          banner.classList.remove('visible');
          setTimeout(() => banner.remove(), 400);
        };
        btnAccept.addEventListener('click', () => dismissBanner('accepted'));
        btnDecline.addEventListener('click', () => dismissBanner('declined'));
      }, 1000);
    });
  }

  // ── CONTACT FORM ──
  const form = document.getElementById('contactForm');
  if (form) {
    form.addEventListener('submit', e => {
      e.preventDefault();
      const nome     = (document.getElementById('nome')     || {}).value || '';
      const email    = (document.getElementById('email')    || {}).value || '';
      const telefone = (document.getElementById('telefone') || {}).value || '';
      const assunto  = (document.getElementById('assunto')  || {}).value || '';
      const mensagem = (document.getElementById('mensagem') || {}).value || '';

      let txt = `Olá! Meu nome é ${nome}.`;
      if (assunto)  txt += `\n*Assunto:* ${assunto}`;
      if (mensagem) txt += `\n*Mensagem:* ${mensagem}`;
      if (email)    txt += `\n*E-mail:* ${email}`;
      if (telefone) txt += `\n*Telefone:* ${telefone}`;

      window.open(`https://web.whatsapp.com/send?phone=5511943211890&text=${encodeURIComponent(txt)}`, '_blank');
    });
  }

});



// ── TOUCH HOVER (mobile) ──
(function () {
  const sel = '.card-glass, .blog-card, .quick-card, .valor-card, .info-card';
  document.querySelectorAll(sel).forEach(card => {
    card.addEventListener('touchstart', () => card.classList.add('touched'), { passive: true });
    card.addEventListener('touchend', () => setTimeout(() => card.classList.remove('touched'), 400), { passive: true });
    card.addEventListener('touchcancel', () => card.classList.remove('touched'), { passive: true });
  });
})();

function closeMobileMenu() {
  const m = document.getElementById('mobileMenu');
  const h = document.getElementById('hamburger');
  if (m) m.classList.remove('open');
  if (h) h.setAttribute('aria-expanded', 'false');
  document.body.style.overflow = '';
}
