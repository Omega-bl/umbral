// Fases 09–12: búsqueda, filtros, favoritos y ficha de historia.
(() => {
  const allCards = () => [...document.querySelectorAll('[data-story]')];
  const input = document.querySelector('[data-search]');
  const filters = [...document.querySelectorAll('[data-filter]')];
  const empty = document.querySelector('[data-empty]');
  const visibleCount = document.querySelector('[data-visible-count]');
  let activeGenre = 'Todos';

  function normalize(value) {
    return value.toLocaleLowerCase('es').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }
  function applyFilters() {
    const query = normalize(input?.value.trim() || '');
    let count = 0;
    allCards().forEach(card => {
      const genreMatch = activeGenre === 'Todos' || card.dataset.genre === activeGenre;
      const textMatch = normalize(`${card.dataset.title} ${card.dataset.genre} ${card.dataset.description} ${card.dataset.author || ''}`).includes(query);
      card.hidden = !(genreMatch && textMatch);
      if (!card.hidden) count++;
    });
    if (empty) empty.hidden = count !== 0;
    if (visibleCount) visibleCount.textContent = count;
  }
  function setGenre(genre) {
    activeGenre = genre;
    filters.forEach(chip => chip.setAttribute('aria-pressed', String(chip.dataset.filter === genre)));
    applyFilters();
  }
  function showAll() {
    if (input) input.value = '';
    setGenre('Todos');
  }
  input?.addEventListener('input', applyFilters);
  filters.forEach(button => button.addEventListener('click', () => setGenre(button.dataset.filter)));

  const dialog = document.querySelector('#storyDialog');
  if (!dialog) return;
  const favorites = new Set();
  try {
    const saved = JSON.parse(localStorage.getItem('umbral-favorites') || '[]');
    if (Array.isArray(saved)) saved.forEach(id => favorites.add(id));
  } catch (_) {}
  const shelfList = document.querySelector('[data-shelf-list]');
  const shelfEmpty = document.querySelector('[data-shelf-empty]');

  function saveFavorites() {
    try { localStorage.setItem('umbral-favorites', JSON.stringify([...favorites])); } catch (_) {}
  }
  function updateShelf() {
    shelfList.replaceChildren();
    allCards().forEach(card => {
      const id = card.dataset.story;
      const active = favorites.has(id);
      const button = card.querySelector('[data-favorite]');
      if (button) {
        button.setAttribute('aria-pressed', String(active));
        button.textContent = active ? '♥' : '♡';
        button.setAttribute('aria-label', `${active ? 'Quitar' : 'Guardar'} ${card.dataset.title} ${active ? 'de' : 'en'} favoritos`);
      }
      if (active) {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.href = `#historia-${id}`;
        a.textContent = card.dataset.title;
        li.append(a);
        shelfList.append(li);
      }
    });
    shelfEmpty.hidden = shelfList.children.length > 0;
  }
  function showStory(card) {
    if (!card) return;
    dialog.querySelector('[data-dialog-title]').textContent = card.dataset.title;
    dialog.querySelector('[data-dialog-genre]').textContent = `${card.dataset.genre.toUpperCase()}${card.dataset.format ? ' · ' + card.dataset.format.toUpperCase() : ''}`;
    dialog.querySelector('[data-dialog-description]').textContent = card.dataset.description;
    dialog.querySelector('[data-dialog-episodes]').textContent = `${card.dataset.episodes} episodios${card.dataset.author ? ' · ' + card.dataset.author : ' · Historia de demostración'}`;
    const cover = dialog.querySelector('[data-dialog-cover]');
    cover.src = card.dataset.coverUrl || `assets/cover-${card.dataset.cover}.webp`;
    cover.alt = `Ilustración de ${card.dataset.title}`;
    const external = dialog.querySelector('[data-dialog-link]');
    if (external) {
      external.hidden = !card.dataset.readUrl;
      if (card.dataset.readUrl) external.href = card.dataset.readUrl;
    }
    const sample = dialog.querySelector('[data-sample]');
    const readButton = dialog.querySelector('[data-read-sample]');
    sample.hidden = true;
    const hasSample = !card.dataset.custom || Boolean(card.dataset.sample);
    readButton.hidden = !hasSample;
    dialog.querySelector('[data-sample-text]').textContent = card.dataset.sample || `Todo comenzó cuando ${card.dataset.title.toLocaleLowerCase('es')} dejó de ser solamente una historia. Una puerta se abrió en el lugar menos esperado, y nada volvió a ser igual.`;
    const note = dialog.querySelector('[data-demo-note]');
    if (note) note.hidden = Boolean(card.dataset.custom);
    dialog.showModal();
  }

  document.addEventListener('click', event => {
    const favorite = event.target.closest('[data-favorite]');
    if (favorite) {
      const id = favorite.dataset.favorite;
      favorites.has(id) ? favorites.delete(id) : favorites.add(id);
      saveFavorites(); updateShelf();
      return;
    }
    const detail = event.target.closest('[data-detail], [data-open-story]');
    if (detail) {
      const id = detail.dataset.detail || detail.dataset.openStory;
      const card = allCards().find(item => item.dataset.story === id);
      if (window.openWithPortal) window.openWithPortal(() => showStory(card), event);
      else showStory(card);
      return;
    }
    const storyLink = event.target.closest('a[href^="#historia-"]');
    if (storyLink) {
      const id = storyLink.getAttribute('href').slice('#historia-'.length);
      const card = allCards().find(item => item.dataset.story === id);
      if (card?.hidden) showAll();
    }
  });
  updateShelf();
  dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.querySelector('[data-read-sample]').addEventListener('click', () => {
    const sample = dialog.querySelector('[data-sample]');
    sample.hidden = !sample.hidden;
    if (!sample.hidden) sample.scrollIntoView({behavior:'smooth',block:'nearest'});
  });

  window.umbralCatalog = {
    refresh() { applyFilters(); updateShelf(); },
    setGenre,
    showAll,
    removeFavorite(id) { favorites.delete(id); saveFavorites(); updateShelf(); },
    count: () => allCards().length,
  };
})();
