// Fase 11: pequeñas partículas en elementos interactivos.
(() => {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  document.addEventListener('pointerdown', event => {
    if (!event.target.closest('.comic-card button, .primary-button, .icon-button, .trend-card, .genre-tile, .editorial-card, .add-header-button, .showcase-arrows button')) return;
    for (let i = 0; i < 8; i++) {
      const dot = document.createElement('span');
      dot.className = 'spark';
      dot.style.left = `${event.clientX}px`;
      dot.style.top = `${event.clientY}px`;
      const angle = Math.PI * 2 * i / 8;
      const radius = 28 + Math.random() * 35;
      dot.style.setProperty('--tx', `${Math.cos(angle)*radius}px`);
      dot.style.setProperty('--ty', `${Math.sin(angle)*radius}px`);
      document.body.append(dot);
      dot.addEventListener('animationend', () => dot.remove(), {once:true});
    }
  });
})();
