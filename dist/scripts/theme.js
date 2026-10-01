// Fase 08: alterna el tema y recuerda la elección en este navegador.
(() => {
  const root = document.documentElement;
  const button = document.querySelector('[data-theme-toggle]');
  const initial = Number(root.dataset.phase) === 12 ? 'dark' : 'light';
  let saved;
  try { saved = localStorage.getItem('umbral-theme'); } catch (_) {}
  root.dataset.theme = saved === 'dark' || saved === 'light' ? saved : initial;
  function updateLabel() {
    if (!button) return;
    const dark = root.dataset.theme === 'dark';
    button.textContent = dark ? '☀' : '☾';
    button.setAttribute('aria-label', dark ? 'Activar modo claro' : 'Activar modo oscuro');
    button.title = dark ? 'Modo claro' : 'Modo oscuro';
  }
  updateLabel();
  button?.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('umbral-theme', root.dataset.theme); } catch (_) {}
    updateLabel();
  });
})();
