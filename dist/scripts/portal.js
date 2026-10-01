// Fase 12: entrada de portal, botón para repetirla y transición al abrir fichas.
(() => {
  const intro = document.querySelector('[data-portal-intro]');
  const flash = document.querySelector('[data-portal-flash]');
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let introTimer;
  function playIntro() {
    if (reduced) { intro.classList.add('is-done'); return; }
    clearTimeout(introTimer);
    intro.classList.remove('is-done', 'is-playing');
    intro.style.display = 'grid';
    void intro.offsetWidth;
    intro.classList.add('is-playing');
    intro.querySelectorAll('.portal-ring, .portal-core, .intro-word').forEach(el => {
      el.style.animation = 'none';
      void el.offsetWidth;
      el.style.animation = '';
    });
    introTimer = setTimeout(() => { intro.classList.add('is-done'); intro.classList.remove('is-playing'); }, 1450);
  }
  playIntro();
  document.querySelectorAll('[data-replay]').forEach(button => button.addEventListener('click', playIntro));
  window.openWithPortal = (callback, event) => {
    if (reduced) { callback(); return; }
    flash.style.setProperty('--px', `${event.clientX}px`);
    flash.style.setProperty('--py', `${event.clientY}px`);
    flash.classList.remove('is-active');
    void flash.offsetWidth;
    flash.classList.add('is-active');
    setTimeout(callback, 190);
    setTimeout(() => flash.classList.remove('is-active'), 500);
  };
})();
