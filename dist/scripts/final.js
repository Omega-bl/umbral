// Fase 12: portada rotativa, catálogo ordenable y colección editable en este navegador.
(() => {
  const slides = [...document.querySelectorAll('[data-slide]')];
  const dots = [...document.querySelectorAll('[data-slide-to]')];
  const showcase = document.querySelector('[data-showcase]');
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let slideIndex = 0;
  let slideTimer;
  function showSlide(index) {
    slideIndex = (index + slides.length) % slides.length;
    slides.forEach((slide, i) => {
      const active = i === slideIndex;
      slide.classList.toggle('is-active', active);
      slide.setAttribute('aria-hidden', String(!active));
      slide.querySelector('.showcase-cta').tabIndex = active ? 0 : -1;
    });
    dots.forEach((dot, i) => dot.setAttribute('aria-pressed', String(i === slideIndex)));
  }
  function pauseSlides() { clearInterval(slideTimer); }
  function startSlides() {
    pauseSlides();
    if (!reduceMotion && !document.hidden) slideTimer = setInterval(() => showSlide(slideIndex + 1), 7000);
  }
  dots.forEach(dot => dot.addEventListener('click', () => { showSlide(Number(dot.dataset.slideTo)); startSlides(); }));
  document.querySelector('[data-slide-prev]')?.addEventListener('click', () => { showSlide(slideIndex - 1); startSlides(); });
  document.querySelector('[data-slide-next]')?.addEventListener('click', () => { showSlide(slideIndex + 1); startSlides(); });
  showcase?.addEventListener('mouseenter', pauseSlides);
  showcase?.addEventListener('mouseleave', startSlides);
  showcase?.addEventListener('focusin', pauseSlides);
  showcase?.addEventListener('focusout', event => { if (!showcase.contains(event.relatedTarget)) startSlides(); });
  document.addEventListener('visibilitychange', () => document.hidden ? pauseSlides() : startSlides());
  showSlide(0); startSlides();

  const catalog = document.querySelector('[data-catalog]');
  const sortSelect = document.querySelector('[data-sort]');
  const addDialog = document.querySelector('#addStoryDialog');
  const form = document.querySelector('#addStoryForm');
  const errorBox = document.querySelector('[data-form-error]');
  const importInput = document.querySelector('[data-import]');
  const STORAGE_KEY = 'umbral-custom-stories-v1';
  function report(message, success=false) {
    errorBox.textContent = message;
    errorBox.dataset.state = success ? 'success' : 'error';
  }
  const BASE_COUNT = catalog.querySelectorAll('[data-story]').length;
  const baseCards = [...catalog.querySelectorAll('[data-story]')];
  baseCards.forEach((card, index) => card.dataset.order = index);

  function validUrl(value) {
    if (!value) return '';
    try {
      const url = new URL(value);
      return ['http:', 'https:'].includes(url.protocol) ? url.href : '';
    } catch (_) { return ''; }
  }
  function validCover(value) {
    if (typeof value !== 'string') return '';
    if (/^data:image\/(?:png|jpeg|webp|avif);base64,[a-z0-9+/=]+$/i.test(value)) return value;
    return validUrl(value);
  }
  function sanitize(raw) {
    if (!raw || typeof raw !== 'object' || !/^u-[a-z0-9-]{5,90}$/i.test(raw.id || '')) return null;
    const title = String(raw.title || '').trim().slice(0,80);
    const genre = String(raw.genre || '').trim().slice(0,40);
    const description = String(raw.description || '').trim().slice(0,350);
    const cover = validCover(raw.cover);
    if (!title || !genre || !description || !cover) return null;
    return {
      id:raw.id, title, genre, description, cover,
      author:String(raw.author || '').trim().slice(0,80),
      format:String(raw.format || 'Historia').trim().slice(0,30),
      episodes:Math.max(0,Math.min(9999,Number(raw.episodes) || 0)),
      readUrl:validUrl(raw.readUrl),
      sample:String(raw.sample || '').trim().slice(0,1600),
      createdAt:Number(raw.createdAt) || Date.now(),
    };
  }
  function loadStories() {
    try {
      const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
      return Array.isArray(parsed) ? parsed.slice(0,150).map(sanitize).filter(Boolean) : [];
    } catch (_) { return []; }
  }
  let stories = loadStories();
  function persist(next) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      stories = next;
      return true;
    } catch (_) {
      report('No hay espacio suficiente en este navegador. Exporta tus historias y usa una portada más pequeña.');
      return false;
    }
  }
  function renderCard(story, order) {
    const card = document.createElement('article');
    card.className = 'comic-card custom-card';
    card.id = `historia-${story.id}`;
    Object.assign(card.dataset, {
      story:story.id, title:story.title, genre:story.genre, description:story.description,
      episodes:String(story.episodes), coverUrl:story.cover, author:story.author,
      format:story.format, readUrl:story.readUrl, sample:story.sample,
      custom:'true', createdAt:String(story.createdAt), order:String(order),
    });
    card.innerHTML = '<div class="cover-wrap"><img loading="lazy" alt=""><span class="cover-badge">MI COLECCIÓN</span><button type="button" class="custom-delete" data-delete-custom aria-label="Eliminar historia">×</button></div><div class="card-body"><p class="genre"></p><h3></h3><p class="blurb"></p><div class="card-actions"><button type="button" class="detail-btn" data-detail>Ver ficha</button><button type="button" class="favorite-btn" data-favorite aria-pressed="false" title="Guardar en favoritos">♡</button></div></div>';
    const image = card.querySelector('img');
    image.src = story.cover;
    image.alt = `Portada de ${story.title}`;
    image.addEventListener('error', () => { image.src = 'assets/portal-hero.webp'; }, {once:true});
    card.querySelector('.genre').textContent = `${story.genre} · ${story.format}`;
    card.querySelector('h3').textContent = story.title;
    card.querySelector('.blurb').textContent = story.description;
    card.querySelector('[data-detail]').dataset.detail = story.id;
    card.querySelector('[data-favorite]').dataset.favorite = story.id;
    card.querySelector('[data-delete-custom]').setAttribute('aria-label', `Eliminar ${story.title}`);
    return card;
  }
  function updateTotal() {
    const count = BASE_COUNT + stories.length;
    document.querySelector('[data-story-count]').textContent = count;
    document.querySelector('.utility-bar .shell > span:last-child').textContent = `${count} historias para descubrir`;
  }
  function sortCards() {
    const mode = sortSelect.value;
    const cards = [...catalog.querySelectorAll('[data-story]')];
    cards.sort((a,b) => {
      if (mode === 'az') return a.dataset.title.localeCompare(b.dataset.title,'es');
      if (mode === 'episodes') return Number(b.dataset.episodes)-Number(a.dataset.episodes);
      if (mode === 'recent') return Number(b.dataset.createdAt || 0)-Number(a.dataset.createdAt || 0) || Number(a.dataset.order)-Number(b.dataset.order);
      return Number(a.dataset.order)-Number(b.dataset.order);
    });
    catalog.append(...cards);
  }
  function renderCustom() {
    catalog.querySelectorAll('[data-custom]').forEach(card => card.remove());
    stories.forEach((story,index) => catalog.append(renderCard(story,BASE_COUNT+index)));
    sortCards(); updateTotal(); window.umbralCatalog.refresh();
  }
  renderCustom();
  sortSelect.addEventListener('change', sortCards);

  document.querySelectorAll('[data-open-add]').forEach(button => button.addEventListener('click', () => {
    report('');
    addDialog.showModal();
  }));
  document.querySelectorAll('[data-close-add]').forEach(button => button.addEventListener('click', () => addDialog.close()));
  addDialog.addEventListener('click', event => { if (event.target === addDialog) addDialog.close(); });
  document.querySelectorAll('[data-jump-genre]').forEach(link => link.addEventListener('click', event => {
    event.preventDefault();
    window.umbralCatalog.showAll();
    window.umbralCatalog.setGenre(link.dataset.jumpGenre);
    document.querySelector('#catalogo').scrollIntoView({behavior:reduceMotion?'instant':'smooth',block:'start'});
  }));

  function compressCover(file) {
    return new Promise((resolve,reject) => {
      if (file.size > 8*1024*1024) { reject(new Error('La portada debe pesar menos de 8 MB.')); return; }
      const blobUrl = URL.createObjectURL(file);
      const image = new Image();
      image.onload = () => {
        const scale = Math.min(1, 560/image.width, 800/image.height);
        const canvas = document.createElement('canvas');
        canvas.width = Math.max(1,Math.round(image.width*scale));
        canvas.height = Math.max(1,Math.round(image.height*scale));
        canvas.getContext('2d').drawImage(image,0,0,canvas.width,canvas.height);
        URL.revokeObjectURL(blobUrl);
        resolve(canvas.toDataURL('image/webp',.78));
      };
      image.onerror = () => { URL.revokeObjectURL(blobUrl); reject(new Error('No se pudo abrir esa imagen. Prueba con JPG, PNG o WebP.')); };
      image.src = blobUrl;
    });
  }
  form.addEventListener('submit', async event => {
    event.preventDefault();
    report('');
    const data = new FormData(form);
    const file = form.elements.coverFile.files[0];
    const coverUrl = validUrl(String(data.get('coverUrl') || '').trim());
    if (!file && !coverUrl) { report('Elige una portada de tu dispositivo o pega su enlace.'); return; }
    if (data.get('url') && !validUrl(String(data.get('url')))) { report('El enlace de lectura debe comenzar con https:// o http://.'); return; }
    const submit = form.querySelector('[type=submit]');
    submit.disabled = true;
    try {
      const cover = file ? await compressCover(file) : coverUrl;
      const story = sanitize({
        id:`u-${crypto.randomUUID ? crypto.randomUUID() : Date.now() + '-' + Math.random().toString(36).slice(2)}`,
        title:data.get('title'), author:data.get('author'), format:data.get('format'),
        genre:data.get('genre'), description:data.get('description'), episodes:data.get('episodes'),
        readUrl:data.get('url'), sample:data.get('sample'), cover, createdAt:Date.now(),
      });
      if (!story) throw new Error('Revisa los datos de la historia y vuelve a intentarlo.');
      if (persist([...stories,story])) {
        form.reset(); addDialog.close();
        window.umbralCatalog.showAll();
        sortSelect.value = 'recent';
        renderCustom();
        document.querySelector('#catalogo').scrollIntoView({behavior:reduceMotion?'instant':'smooth'});
      }
    } catch (error) { report(error.message); }
    finally { submit.disabled = false; }
  });
  catalog.addEventListener('click', event => {
    const button = event.target.closest('[data-delete-custom]');
    if (!button) return;
    const id = button.closest('[data-story]').dataset.story;
    const story = stories.find(item => item.id === id);
    if (!story || !confirm(`¿Eliminar «${story.title}» de tu colección?`)) return;
    if (persist(stories.filter(item => item.id !== id))) {
      window.umbralCatalog.removeFavorite(id);
      renderCustom();
    }
  });

  document.querySelector('[data-export]').addEventListener('click', () => {
    const blob = new Blob([JSON.stringify({version:1,stories},null,2)],{type:'application/json'});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url; link.download = 'umbral-mis-historias.json';
    document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url),1000);
    report('Archivo de respaldo preparado.', true);
  });
  importInput.addEventListener('change', async () => {
    const file = importInput.files[0];
    if (!file) return;
    report('');
    try {
      if (file.size > 8*1024*1024) throw new Error('El archivo es demasiado grande para importar.');
      const parsed = JSON.parse(await file.text());
      if (parsed.version !== 1 || !Array.isArray(parsed.stories)) throw new Error('El archivo no es un respaldo de Umbral Comics.');
      if (parsed.stories.length > 150) throw new Error('Importa un máximo de 150 historias por archivo.');
      const imported = parsed.stories.map(sanitize);
      if (imported.some(item => !item)) throw new Error('Algunas historias del archivo tienen datos incompletos.');
      const combined = new Map(stories.map(story => [story.id,story]));
      imported.forEach(story => combined.set(story.id,story));
      if (persist([...combined.values()])) {
        renderCustom();
        report(`Se importaron ${imported.length} historias. Ya aparecen en tu catálogo.`, true);
      }
    } catch (error) { report(error.message); }
    finally { importInput.value = ''; }
  });

  if ('IntersectionObserver' in window && !reduceMotion) {
    document.documentElement.classList.add('js-reveal');
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
    }),{threshold:.08,rootMargin:'0px 0px 60px 0px'});
    document.querySelectorAll('.reveal').forEach(section => observer.observe(section));
  }
})();
