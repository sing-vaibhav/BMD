/* ═══════════════════════════════════════════════════
   RANGAURA — Main JavaScript
   ═══════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {

  /* ── Navbar: shrink on scroll ─────────────────── */
  const nav = document.getElementById('main-nav');
  window.addEventListener('scroll', () => {
    nav && nav.classList.toggle('scrolled', window.scrollY > 60);
  });

  /* ── Mobile burger menu ────────────────────────── */
  const burger = document.getElementById('navBurger');
  const menu = document.getElementById('navMenu');
  if (burger && menu) {
    burger.addEventListener('click', () => {
      menu.classList.toggle('open');
      burger.textContent = menu.classList.contains('open') ? '✕' : '☰';
    });
    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!nav.contains(e.target)) {
        menu.classList.remove('open');
        burger.textContent = '☰';
      }
    });
  }

  /* ── Scroll reveal ─────────────────────────────── */
  const revealEls = document.querySelectorAll(
    '.feature-card, .step, .model-card, .g-item, ' +
    '.audience-card, .full-g-card, .dash-stat-card, ' +
    '.request-card, .quick-link-card'
  );
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          // Stagger with index
          setTimeout(() => {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
          }, (entry.target.dataset.delay || 0));
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    revealEls.forEach((el, i) => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(28px)';
      el.style.transition = 'opacity 0.55s ease, transform 0.55s ease';
      el.dataset.delay = (i % 4) * 80; // stagger in groups of 4
      io.observe(el);
    });
  }

  /* ── Auto-dismiss messages after 5s ───────────── */
  const alerts = document.querySelectorAll('.ra-alert');
  alerts.forEach((alert, i) => {
    setTimeout(() => {
      alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      alert.style.opacity = '0';
      alert.style.transform = 'translateX(20px)';
      setTimeout(() => alert.remove(), 400);
    }, 5000 + i * 300);
  });

  /* ── Button ripple effect ─────────────────────── */
  document.querySelectorAll('.btn-primary, .btn-secondary').forEach(btn => {
    btn.addEventListener('click', function (e) {
      const rect = btn.getBoundingClientRect();
      const ripple = document.createElement('span');
      const size = Math.max(rect.width, rect.height);
      ripple.style.cssText = `
        position:absolute; width:${size}px; height:${size}px;
        border-radius:50%; background:rgba(255,255,255,0.2);
        left:${e.clientX - rect.left - size/2}px;
        top:${e.clientY - rect.top - size/2}px;
        transform:scale(0); animation:ripple 0.5s linear; pointer-events:none;
      `;
      if (btn.style.position !== 'relative') btn.style.position = 'relative';
      btn.style.overflow = 'hidden';
      btn.appendChild(ripple);
      setTimeout(() => ripple.remove(), 500);
    });
  });

  // Add ripple keyframes
  if (!document.getElementById('ripple-style')) {
    const style = document.createElement('style');
    style.id = 'ripple-style';
    style.textContent = '@keyframes ripple { to { transform: scale(2.5); opacity: 0; } }';
    document.head.appendChild(style);
  }

  /* ── Active nav link ──────────────────────────── */
  const currentPath = window.location.pathname;
  document.querySelectorAll('nav ul a').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.style.color = 'var(--orange)';
    }
  });

  /* ── Smooth internal anchor scrolling ─────────── */
  document.querySelectorAll('a[href*="#"]').forEach(link => {
    const href = link.getAttribute('href');
    if (!href.startsWith('#') && !href.includes(window.location.pathname)) return;
    link.addEventListener('click', function (e) {
      const hash = href.split('#')[1];
      if (!hash) return;
      const target = document.getElementById(hash);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        // Close mobile menu if open
        if (menu) menu.classList.remove('open');
      }
    });
  });

  /* ── Painting cards tilt effect ──────────────── */
  document.querySelectorAll('.painting-card, .full-g-card').forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width - 0.5) * 12;
      const y = ((e.clientY - rect.top) / rect.height - 0.5) * -12;
      card.style.transform = `perspective(600px) rotateX(${y}deg) rotateY(${x}deg) translateY(-4px)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });

  /* ── Gallery g-item min height ─────────────── */
  document.querySelectorAll('.g-item').forEach(item => {
    if (!item.style.minHeight) item.style.minHeight = '180px';
  });

  /* ── Form field focus animation ─────────────── */
  document.querySelectorAll('.ra-input').forEach(input => {
    const group = input.closest('.form-group');
    if (!group) return;
    input.addEventListener('focus', () => group.classList.add('focused'));
    input.addEventListener('blur', () => group.classList.remove('focused'));
  });

  /* ── Client-side form validation helpers ─────── */
  const requestForm = document.getElementById('requestForm');
  if (requestForm) {
    const requiredFields = requestForm.querySelectorAll('[required]');
    requestForm.addEventListener('submit', function (e) {
      let valid = true;
      requiredFields.forEach(field => {
        if (!field.value.trim()) {
          valid = false;
          field.style.borderColor = '#ef4444';
          field.addEventListener('input', () => { field.style.borderColor = ''; }, { once: true });
        }
      });
      if (!valid) {
        e.preventDefault();
        // Scroll to first error
        const first = requestForm.querySelector('[style*="border-color: rgb(239, 68, 68)"]');
        if (first) first.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  }

});
