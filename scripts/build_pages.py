#!/usr/bin/env python3
"""Generate the twelve readable, standalone HTML phases of Umbral Comics."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dist"

PHASES = [
    ("HTML puro", "Estructura semántica sin CSS, imágenes ni JavaScript."),
    ("Contenido e imágenes", "Portadas, imagen principal y descripciones."),
    ("Tipografía", "Fuentes, tamaños y espacios básicos."),
    ("Centrado y cuadrícula", "Contenedor, columnas y alineación."),
    ("Paleta de color", "Variables y acentos que dan identidad."),
    ("Navegación y tarjetas", "Cabecera, portada destacada y tarjetas visuales."),
    ("Diseño adaptable", "Distribución para móvil, tableta y escritorio."),
    ("Modo oscuro", "Tema alternativo con preferencia guardada."),
    ("Búsqueda y filtros", "Exploración por texto y género en tiempo real."),
    ("Favoritos y ficha", "Estantería local y ventana con detalles de cada historia."),
    ("Movimiento y destellos", "Respuestas al pasar y pulsar sobre la interfaz."),
    ("Portal final", "Catálogo ampliado, portada dinámica, colecciones y tus propias historias."),
]

STORIES = [
    dict(id="corona", title="La corona de ceniza", genre="Fantasía", blurb="Una heredera descubre que su reino vive dentro de un libro que alguien está reescribiendo.", status="Nuevo episodio", update="Martes", episodes=24, cover=1),
    dict(id="neon", title="Código neón", genre="Acción", blurb="Un mensajero cruza una ciudad imposible para entregar un secreto capaz de apagarla.", status="En tendencia", update="Jueves", episodes=38, cover=2),
    dict(id="jardin", title="El jardín imposible", genre="Fantasía", blurb="Cada planta de una biblioteca olvidada conserva los recuerdos de una persona.", status="Original", update="Viernes", episodes=17, cover=3),
    dict(id="lluvia", title="Bajo la misma lluvia", genre="Romance", blurb="Dos desconocidos comparten un paraguas y vuelven a encontrarse en todas las tormentas.", status="Popular", update="Miércoles", episodes=31, cover=4),
    dict(id="eclipse", title="Eclipse de medianoche", genre="Misterio", blurb="Cuando la luna se vuelve roja, los alumnos recuerdan una vida que nunca vivieron.", status="Nuevo episodio", update="Sábado", episodes=20, cover=5),
    dict(id="expreso", title="Expreso de las estrellas", genre="Aventura", blurb="Un tren atraviesa constelaciones y cada estación ofrece una segunda oportunidad.", status="Original", update="Domingo", episodes=15, cover=6),
    dict(id="farol", title="El caso del farol rojo", genre="Misterio", blurb="Una detective sigue pistas que solo aparecen reflejadas en la lluvia de medianoche.", status="Nuevo", update="Lunes", episodes=12, cover=7),
    dict(id="chispas", title="Chispas y tornillos", genre="Comedia", blurb="Una inventora y su robot convierten los problemas cotidianos en aventuras absurdas.", status="Para sonreír", update="Sábado", episodes=22, cover=8),
    dict(id="marea", title="Marea de otro mundo", genre="Ciencia ficción", blurb="Una astronauta escucha una señal bajo el océano de un planeta sin mapas.", status="Nuevo episodio", update="Jueves", episodes=19, cover=9),
    dict(id="ultima", title="La última melodía", genre="Drama", blurb="Una violinista recibe una partitura que cambia cada vez que recuerda a alguien.", status="Original", update="Viernes", episodes=28, cover=10),
    dict(id="zorro", title="El espíritu del zorro", genre="Fantasía", blurb="En un bosque de faroles, una niña protege el secreto de un antiguo guardián.", status="Popular", update="Miércoles", episodes=34, cover=11),
    dict(id="nieve", title="La espada de nieve", genre="Acción", blurb="Una guerrera cruza la montaña para recuperar el nombre que le arrebataron.", status="En tendencia", update="Domingo", episodes=26, cover=12),
]

# La fase 12 amplía el catálogo; las fases anteriores conservan sus 12 historias.
EXTRA_STORIES = [
    dict(id="vampira", title="La noche escarlata", genre="Terror", blurb="Una heredera inmortal vuelve a la catedral donde comenzó una promesa imposible.", status="Nuevo", update="Viernes", episodes=14, cover=13),
    dict(id="titan", title="Órbita titán", genre="Ciencia ficción", blurb="Un piloto encuentra la señal de una civilización al otro lado de una lluvia de meteoros.", status="En tendencia", update="Martes", episodes=27, cover=14),
    dict(id="cafe", title="Café de lo imposible", genre="Comedia", blurb="Dos amigos sirven café a criaturas mágicas y cada pedido termina en desastre.", status="Para sonreír", update="Lunes", episodes=18, cover=15),
    dict(id="dunas", title="Las ruinas del viento", genre="Aventura", blurb="Una arqueóloga sigue un mapa hacia ciudades que flotan sobre el desierto.", status="Original", update="Domingo", episodes=23, cover=16),
    dict(id="promesa", title="Promesa de primavera", genre="Romance", blurb="Dos estudiantes se reencuentran cada primavera bajo el mismo árbol de cerezos.", status="Popular", update="Miércoles", episodes=32, cover=17),
    dict(id="marina", title="La reina de las mareas", genre="Fantasía", blurb="Una princesa del océano desafía a las estrellas para salvar a su pueblo.", status="Nuevo episodio", update="Sábado", episodes=21, cover=18),
]
FINAL_STORIES = STORIES + EXTRA_STORIES


def nav_phase(n):
    before = f'<a href="v{n-1:02}.html">← Fase {n-1:02}</a>' if n > 1 else '<span>Inicio del recorrido</span>'
    after = f'<a href="v{n+1:02}.html">Fase {n+1:02} →</a>' if n < 12 else '<a href="index.html">Ver todas las fases →</a>'
    return f'<nav class="phase-nav" aria-label="Navegación entre fases"><a href="index.html">Todas las fases</a><span class="phase-current">Fase {n:02} / 12 · {PHASES[n-1][0]}</span><div class="phase-arrows">{before}{after}</div></nav>'


def document(n, body):
    links = '\n'.join(f'<link rel="stylesheet" href="styles/v{i:02}.css">' for i in range(3, n+1))
    scripts = []
    if n >= 8: scripts.append('<script src="scripts/theme.js" defer></script>')
    if n >= 9: scripts.append('<script src="scripts/catalog.js" defer></script>')
    if n >= 11: scripts.append('<script src="scripts/effects.js" defer></script>')
    if n >= 12:
        scripts.append('<script src="scripts/portal.js" defer></script>')
        scripts.append('<script src="scripts/final.js" defer></script>')
    return f'''<!doctype html>
<html lang="es" data-phase="{n}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Umbral Comics, fase {n}: {escape(PHASES[n-1][1])}">
  <title>Fase {n:02} · {escape(PHASES[n-1][0])} · Umbral Comics</title>
  {links}
</head>
<body>
{body}
{''.join(scripts)}
</body>
</html>
'''


def basic(n):
    images = n >= 2
    cards = '\n'.join(f'''<article>
    {f'<img src="assets/cover-{s["cover"]}.webp" alt="Ilustración de {escape(s["title"])}" width="180" loading="lazy">' if images else ''}
    <h3>{escape(s['title'])}</h3>
    <p>{escape(s['genre'])} · {s['episodes']} episodios</p>
    <p>{escape(s['blurb'])}</p>
  </article>''' for s in STORIES)
    main = f'''{nav_phase(n)}
<header>
  <p>Umbral Comics</p>
  <nav aria-label="Principal"><a href="#inicio">Inicio</a> · <a href="#catalogo">Explorar</a> · <a href="#ranking">Ranking</a></nav>
</header>
<main id="inicio">
  <section aria-labelledby="titulo-principal">
    <h1 id="titulo-principal">Cruza el umbral de una nueva historia</h1>
    <p>Fantasía, acción, romance y misterio para leer a tu ritmo.</p>
    <p><a href="#catalogo">Explorar historias</a></p>
    {f'<img src="assets/portal-hero.webp" alt="Un portal luminoso se abre sobre la ciudad" width="640">' if images else ''}
  </section>
  <section id="catalogo" aria-labelledby="titulo-catalogo">
    <h2 id="titulo-catalogo">Historias para descubrir</h2>
    {cards}
  </section>
  <section id="ranking" aria-labelledby="titulo-ranking">
    <h2 id="titulo-ranking">Top de la semana</h2>
    <ol><li>La corona de ceniza</li><li>Código neón</li><li>Bajo la misma lluvia</li></ol>
  </section>
</main>
<footer><p>Umbral Comics · Proyecto de demostración con historias ficticias.</p></footer>'''
    return document(n, main)


def card(s, n):
    extras = ''
    if n >= 10:
        extras = f'''<div class="card-actions">
          <button type="button" class="detail-btn" data-detail="{s['id']}">Ver ficha</button>
          <button type="button" class="favorite-btn" data-favorite="{s['id']}" aria-label="Guardar {escape(s['title'])} en favoritos" aria-pressed="false" title="Guardar en favoritos">♡</button>
        </div>'''
    return f'''<article class="comic-card" id="historia-{s['id']}" data-story="{s['id']}" data-title="{escape(s['title'])}" data-genre="{escape(s['genre'])}" data-description="{escape(s['blurb'])}" data-episodes="{s['episodes']}" data-cover="{s['cover']}">
      <div class="cover-wrap">
        <img src="assets/cover-{s['cover']}.webp" alt="Ilustración de {escape(s['title'])}" width="500" height="500" loading="lazy">
        {'<span class="cover-badge">'+escape(s['status'])+'</span>' if n >= 6 else ''}
      </div>
      <div class="card-body">
        <p class="genre">{escape(s['genre'])} <span class="meta-dot">·</span> {s['episodes']} episodios</p>
        <h3>{escape(s['title'])}</h3>
        <p class="blurb">{escape(s['blurb'])}</p>
        {extras}
      </div>
    </article>'''


def rich(n):
    theme = '<button type="button" class="icon-button theme-toggle" data-theme-toggle aria-label="Cambiar tema" title="Cambiar tema">☾</button>' if n >= 8 else ''
    replay = '<button type="button" class="icon-button replay-button" data-replay aria-label="Repetir entrada del portal" title="Repetir portal">✦</button>' if n >= 12 else ''
    search = '<label class="header-search"><span class="sr-only">Buscar historias</span><input type="search" data-search placeholder="Buscar historias..." autocomplete="off"><span aria-hidden="true">⌕</span></label>' if n >= 9 else ''
    filters = '<div class="filters" role="group" aria-label="Filtrar por género">' + ''.join(f'<button type="button" class="filter-chip" data-filter="{genre}" aria-pressed="{str(i==0).lower()}">{genre}</button>' for i,genre in enumerate(['Todos','Fantasía','Acción','Romance','Misterio','Aventura','Comedia','Ciencia ficción','Drama'])) + '</div>' if n >= 9 else ''
    empty = '<p class="empty-state" data-empty hidden>No encontramos historias con esa búsqueda. Prueba otro título o género.</p>' if n >= 9 else ''
    aside_extra = '''<section class="shelf" id="estanteria"><div class="side-heading"><h2>Tu estantería</h2><span>♡</span></div><p data-shelf-empty>Guarda una historia con el corazón y aparecerá aquí.</p><ul data-shelf-list></ul></section>''' if n >= 10 else ''
    modal = '''<dialog class="story-dialog" id="storyDialog" aria-labelledby="dialogTitle">
      <button type="button" class="dialog-close" data-close aria-label="Cerrar ficha">×</button>
      <div class="dialog-layout"><img data-dialog-cover src="assets/cover-1.webp" alt="" width="500" height="500"><div class="dialog-copy"><p class="eyebrow" data-dialog-genre></p><h2 id="dialogTitle" data-dialog-title></h2><p data-dialog-description></p><p class="dialog-episodes" data-dialog-episodes></p><button type="button" class="primary-button" data-read-sample>Leer muestra</button><div class="sample" data-sample hidden><h3>Un primer vistazo</h3><p data-sample-text></p><p>Esta es una muestra original del proyecto. La historia completa aún no está publicada.</p></div></div></div>
    </dialog>''' if n >= 10 else ''
    intro = '<div class="portal-intro" data-portal-intro aria-hidden="true"><div class="portal-ring"></div><div class="portal-core"></div><span class="intro-word">UMBRAL</span></div><div class="portal-flash" data-portal-flash aria-hidden="true"></div>' if n >= 12 else ''
    latest = '''<section class="updates" id="novedades"><div class="section-heading"><div><p class="eyebrow">NUEVOS CAPÍTULOS</p><h2>Esta semana</h2></div></div><div class="update-list"><a href="#historia-corona"><span>MAR</span><strong>La corona de ceniza</strong><small>Capítulo 24</small></a><a href="#historia-neon"><span>JUE</span><strong>Código neón</strong><small>Capítulo 38</small></a><a href="#historia-jardin"><span>VIE</span><strong>El jardín imposible</strong><small>Capítulo 17</small></a></div></section>''' if n >= 6 else ''
    return document(n, f'''{intro}
{nav_phase(n)}
<header class="topbar" id="inicio"><div class="topbar-inner shell">
  <a class="brand" href="index.html" aria-label="Umbral Comics, todas las fases"><span class="brand-mark">✦</span><span>UMBRAL<span class="brand-light">COMICS</span></span></a>
  <nav class="main-nav" aria-label="Principal"><a href="#inicio">Inicio</a><a href="#catalogo">Explorar</a><a href="#ranking">Ranking</a>{'<a href="#novedades">Novedades</a>' if n>=6 else ''}</nav>
  <div class="header-actions">{search}{theme}{replay}</div>
</div></header>
<main class="shell">
  <section class="hero" aria-labelledby="hero-title">
    <div class="hero-copy"><p class="eyebrow">HISTORIAS PARA PERDERSE</p><h1 id="hero-title">Cruza el umbral de una <em>nueva historia.</em></h1><p>Encuentra mundos que te esperan detrás de cada viñeta. Elige por dónde empezar.</p><a class="primary-button" href="#catalogo">Explorar historias</a></div>
    <img class="hero-image" src="assets/portal-hero.webp" alt="Un portal luminoso se abre sobre una ciudad nocturna" width="1600" height="900">
    {('<span class="hero-count">01 / 12 &nbsp; UNIVERSOS POR DESCUBRIR</span>' if n>=6 else '')}
  </section>
  <div class="content-layout">
    <div class="main-column">
      <section class="catalog" id="catalogo" aria-labelledby="catalog-title"><div class="section-heading"><div><p class="eyebrow">PARA EMPEZAR A LEER</p><h2 id="catalog-title">Historias para descubrir</h2></div><span class="section-note">12 historias originales</span></div>
        {filters}
        <div class="catalog-grid" data-catalog>{''.join(card(s,n) for s in STORIES)}</div>
        {empty}
      </section>
      {latest}
    </div>
    <aside class="sidebar" aria-label="Selecciones"><section class="ranking" id="ranking"><div class="side-heading"><h2>Top de la semana</h2><span>↗</span></div><ol><li><a href="#historia-corona"><b>01</b><span>La corona de ceniza<small>Fantasía</small></span></a></li><li><a href="#historia-neon"><b>02</b><span>Código neón<small>Acción</small></span></a></li><li><a href="#historia-lluvia"><b>03</b><span>Bajo la misma lluvia<small>Romance</small></span></a></li><li><a href="#historia-eclipse"><b>04</b><span>Eclipse de medianoche<small>Misterio</small></span></a></li></ol></section>{aside_extra}
      <div class="side-quote"><span>✦</span><p>Cada historia es una puerta. ¿Cuál abrirás hoy?</p></div>
    </aside>
  </div>
</main>
<footer class="footer"><div class="shell"><strong>✦ UMBRAL COMICS</strong><p>Proyecto de demostración. Títulos, sinopsis e ilustraciones originales creados para este recorrido.</p><a href="index.html">Ver las 12 fases</a></div></footer>
{modal}''')


def final_page():
    featured = [
        dict(label="PORTAL DE LA SEMANA", title="Historias que te llevan a otro mundo.", copy="Un catálogo para encontrar esa serie que no querrás dejar a medias.", image="portal-hero.webp", id="corona", cta="Explorar el catálogo", href="#catalogo", palette="violet"),
        dict(label="FANTASÍA · 24 EPISODIOS", title="La corona de ceniza", copy="Una heredera, un reino escrito en páginas y un destino que puede cambiarse.", image="cover-1.webp", id="corona", cta="Conocer la historia", href="#historia-corona", palette="rose"),
        dict(label="ACCIÓN · 38 EPISODIOS", title="Código neón", copy="Un mensaje secreto atraviesa la ciudad que nunca se apaga.", image="cover-2.webp", id="neon", cta="Conocer la historia", href="#historia-neon", palette="cyan"),
    ]
    slides = ''.join(f'''<article class="showcase-slide {'is-active' if i==0 else ''} theme-{s['palette']}" data-slide="{i}" aria-hidden="{str(i!=0).lower()}">
      <div class="showcase-ambient"></div><img class="showcase-image" src="assets/{s['image']}" alt="" {'fetchpriority="high"' if i==0 else 'loading="lazy"'}>
      <div class="showcase-copy"><p class="eyebrow"><span class="eyebrow-line"></span>{s['label']}</p><h1>{s['title']}</h1><p>{s['copy']}</p>{f'<a class="showcase-cta" href="{s["href"]}">{s["cta"]} <span aria-hidden="true">↗</span></a>' if i==0 else f'<button type="button" class="showcase-cta" data-open-story="{s["id"]}">{s["cta"]} <span aria-hidden="true">↗</span></button>'}</div>
      <span class="showcase-index">{i+1:02} / 03</span>
    </article>''' for i,s in enumerate(featured))
    trending_ids = ['corona','neon','marea','nieve','zorro','vampira']
    trending = ''.join(f'''<button type="button" class="trend-card" data-open-story="{s['id']}"><span class="trend-image"><img src="assets/cover-{s['cover']}.webp" alt="" loading="lazy"><b>{i:02}</b></span><span class="trend-name">{escape(s['title'])}</span><span class="trend-genre">{escape(s['genre'])}</span></button>''' for i,s in enumerate([next(x for x in FINAL_STORIES if x['id']==id) for id in trending_ids],1))
    genres = [
        ('Fantasía','Mundos sin límites','cover-1.webp','violet'),
        ('Acción','Historias que aceleran','cover-2.webp','red'),
        ('Romance','Momentos para recordar','cover-4.webp','pink'),
        ('Misterio','Pistas entre sombras','cover-7.webp','blue'),
        ('Ciencia ficción','Más allá del cielo','cover-9.webp','cyan'),
        ('Aventura','Rutas por descubrir','cover-6.webp','gold'),
    ]
    genre_tiles = ''.join(f'''<button type="button" class="genre-tile genre-{tone}" data-jump-genre="{escape(genre)}"><span><small>EXPLORAR</small><strong>{escape(genre)}</strong><em>{escape(desc)}</em></span><img src="assets/{image}" alt="" loading="lazy"><span class="genre-arrow" aria-hidden="true">↗</span></button>''' for genre,desc,image,tone in genres)
    filters = ''.join(f'<button type="button" class="filter-chip" data-filter="{escape(g)}" aria-pressed="{str(i==0).lower()}">{escape(g)}</button>' for i,g in enumerate(['Todos','Fantasía','Acción','Romance','Misterio','Aventura','Comedia','Ciencia ficción','Drama','Terror']))
    editorial_ids = ['jardin','ultima','marina']
    editorial = ''.join(f'''<button type="button" class="editorial-card" data-open-story="{s['id']}"><img src="assets/cover-{s['cover']}.webp" alt="" loading="lazy"><span class="editorial-content"><small>SELECCIÓN UMBRAL · {i:02}</small><strong>{escape(s['title'])}</strong><span>{escape(s['genre'])} / {s['episodes']} episodios</span></span></button>''' for i,s in enumerate([next(x for x in FINAL_STORIES if x['id']==id) for id in editorial_ids],1))
    rank_ids = ['corona','neon','nieve','marea','lluvia']
    rank_list = ''.join(f'''<li><a href="#historia-{s['id']}"><b>{i:02}</b><img src="assets/cover-{s['cover']}.webp" alt="" loading="lazy"><span><strong>{escape(s['title'])}</strong><small>{escape(s['genre'])} · {s['episodes']} episodios</small></span><span class="rank-rise" aria-hidden="true">↗</span></a></li>''' for i,s in enumerate([next(x for x in FINAL_STORIES if x['id']==id) for id in rank_ids],1))
    updates = ''.join(f'''<a href="#historia-{s['id']}"><span class="update-day">{s['update'][:3].upper()}</span><img src="assets/cover-{s['cover']}.webp" alt="" loading="lazy"><span><strong>{escape(s['title'])}</strong><small>{escape(s['genre'])} · Nuevo capítulo {s['episodes']}</small></span><span aria-hidden="true">↗</span></a>''' for s in FINAL_STORIES[:6])
    return document(12, f'''<div class="portal-intro" data-portal-intro aria-hidden="true"><div class="portal-ring"></div><div class="portal-core"></div><span class="intro-word">UMBRAL</span></div><div class="portal-flash" data-portal-flash aria-hidden="true"></div>
{nav_phase(12)}
<div class="utility-bar"><div class="shell"><span><span class="utility-star">✦</span> CADA PÁGINA ABRE UN MUNDO</span><span>{len(FINAL_STORIES)} historias originales para descubrir</span></div></div>
<header class="topbar" id="inicio"><div class="topbar-inner shell"><a class="brand" href="index.html" aria-label="Umbral Comics, todas las fases"><span class="brand-mark">✦</span><span>UMBRAL<small>COMICS</small></span></a><nav class="main-nav" aria-label="Principal"><a href="#inicio">Inicio</a><a href="#tendencias">Tendencias</a><a href="#generos">Géneros</a><a href="#catalogo">Catálogo</a><a href="#novedades">Novedades</a></nav><div class="header-actions"><label class="header-search"><span class="sr-only">Buscar historias</span><input type="search" data-search placeholder="Busca tu próxima historia" autocomplete="off"><span aria-hidden="true">⌕</span></label><button type="button" class="add-header-button" data-open-add><span aria-hidden="true">＋</span><span>Agregar</span></button><button type="button" class="icon-button theme-toggle" data-theme-toggle aria-label="Cambiar tema" title="Cambiar tema">☾</button><button type="button" class="icon-button replay-button" data-replay aria-label="Repetir entrada del portal" title="Repetir portal">✦</button></div></div></header>
<div class="discovery-bar"><div class="shell"><strong>DESCUBRE</strong><a href="#catalogo" data-jump-genre="Fantasía">Fantasía</a><a href="#catalogo" data-jump-genre="Acción">Acción</a><a href="#catalogo" data-jump-genre="Romance">Romance</a><a href="#catalogo" data-jump-genre="Ciencia ficción">Ciencia ficción</a><a href="#catalogo">Todas las historias <span aria-hidden="true">↗</span></a></div></div>
<main><div class="shell">
  <section class="showcase-area" aria-label="Historias destacadas"><div class="showcase-grid"><div class="showcase" data-showcase>{slides}<div class="showcase-controls"><div class="showcase-dots" role="group" aria-label="Elegir historia destacada"><button type="button" data-slide-to="0" aria-label="Mostrar destacado 1" aria-pressed="true"></button><button type="button" data-slide-to="1" aria-label="Mostrar destacado 2" aria-pressed="false"></button><button type="button" data-slide-to="2" aria-label="Mostrar destacado 3" aria-pressed="false"></button></div><div class="showcase-arrows"><button type="button" data-slide-prev aria-label="Destacado anterior">←</button><button type="button" data-slide-next aria-label="Destacado siguiente">→</button></div></div></div><div class="showcase-aside"><div class="aside-cover"><img src="assets/cover-11.webp" alt="Ilustración de El espíritu del zorro"><span>DESCUBRIMIENTO DEL DÍA</span></div><div class="aside-copy"><p>Fantasía · 34 episodios</p><h2>El espíritu del zorro</h2><button type="button" data-open-story="zorro">Conocer la historia <span aria-hidden="true">↗</span></button></div></div></div></section>
  <div class="stat-ribbon"><span><b data-story-count>{len(FINAL_STORIES)}</b><small>HISTORIAS</small></span><span><b>10</b><small>GÉNEROS</small></span><span><b>∞</b><small>MUNDOS POSIBLES</small></span><p>Encuentra la historia que no sabías que necesitabas.</p></div>
  <section class="trending-section reveal" id="tendencias"><div class="section-heading"><div><p class="eyebrow">LO QUE MÁS ATRAPA</p><h2>En tendencia <span class="title-spark">✦</span></h2></div><a class="text-link" href="#catalogo">Ver el catálogo <span aria-hidden="true">↗</span></a></div><div class="trending-rail">{trending}</div></section>
  <section class="genres-section reveal" id="generos"><div class="section-heading"><div><p class="eyebrow">ELIGE UNA PUERTA</p><h2>Explora por género</h2></div><p class="section-note">Cada mundo empieza con una elección.</p></div><div class="genre-grid">{genre_tiles}</div></section>
  <div class="magazine-layout"><div class="magazine-main"><section class="catalog reveal" id="catalogo" aria-labelledby="catalog-title"><div class="section-heading catalog-heading"><div><p class="eyebrow">BIBLIOTECA DE UNIVERSOS</p><h2 id="catalog-title">Explora el catálogo</h2><p class="catalog-subtitle">Originales, descubrimientos y las historias que tú agregues.</p></div><span class="catalog-counter"><b data-visible-count>{len(FINAL_STORIES)}</b> historias</span></div><div class="catalog-tools"><div class="filters" role="group" aria-label="Filtrar por género">{filters}</div><label class="sort-control">Ordenar <select data-sort aria-label="Ordenar historias"><option value="featured">Destacados</option><option value="az">Título A–Z</option><option value="episodes">Más episodios</option><option value="recent">Agregados recientes</option></select></label></div><div class="catalog-grid" data-catalog>{''.join(card(s,12) for s in FINAL_STORIES)}</div><p class="empty-state" data-empty hidden>No encontramos historias con esa búsqueda. Prueba otro título o género.</p></section>
  <section class="creator-banner reveal"><div><p class="eyebrow">TU ESTANTERÍA, TUS REGLAS</p><h2>¿Tienes una historia favorita que falta aquí?</h2><p>Agrega su portada, género, sinopsis y enlace de lectura. Aparecerá en tu catálogo.</p><button type="button" class="primary-button" data-open-add>Agregar una historia <span aria-hidden="true">＋</span></button></div><div class="banner-art" aria-hidden="true"><span>✦</span><span>✧</span><span>✦</span></div></section>
  <section class="editorial-section reveal" id="colecciones"><div class="section-heading"><div><p class="eyebrow">SELECCIÓN UMBRAL</p><h2>Joyas para descubrir</h2></div></div><div class="editorial-grid">{editorial}</div></section>
  <section class="updates reveal" id="novedades"><div class="section-heading"><div><p class="eyebrow">NO PIERDAS EL HILO</p><h2>Últimas actualizaciones</h2></div></div><div class="update-list">{updates}</div></section></div>
  <aside class="magazine-sidebar" aria-label="Ranking y estantería"><section class="ranking" id="ranking"><div class="side-heading"><div><p class="eyebrow">LOS MÁS LEÍDOS</p><h2>Top de la semana</h2></div><span>↗</span></div><ol>{rank_list}</ol></section><section class="shelf" id="estanteria"><div class="side-heading"><div><p class="eyebrow">GUARDADAS POR TI</p><h2>Tu estantería</h2></div><span>♡</span></div><p data-shelf-empty>Guarda una historia con el corazón y aparecerá aquí.</p><ul data-shelf-list></ul></section><section class="personal-box"><span class="personal-icon">✦</span><p class="eyebrow">TU PROPIA COLECCIÓN</p><h2>Haz espacio para tus mundos favoritos.</h2><p>Agrega historias y llévatelas en un archivo para conservarlas.</p><button type="button" data-open-add>Gestionar mis historias <span aria-hidden="true">↗</span></button></section></aside></div>
  <section class="closing-panel reveal"><img src="assets/portal-hero.webp" alt="" loading="lazy"><div><p class="eyebrow">EL SIGUIENTE CAPÍTULO TE ESPERA</p><h2>Siempre hay otra puerta por abrir.</h2><a class="primary-button" href="#catalogo">Seguir explorando</a></div></section>
</div></main>
<footer class="footer final-footer"><div class="shell"><div class="footer-brand"><strong>✦ UMBRAL <span>COMICS</span></strong><p>Historias para leer, descubrir y guardar.</p></div><div><h3>EXPLORAR</h3><a href="#tendencias">Tendencias</a><a href="#generos">Géneros</a><a href="#catalogo">Catálogo</a></div><div><h3>PROYECTO</h3><a href="index.html">Las 12 fases</a><a href="v01.html">HTML inicial</a><button type="button" data-replay>Repetir portal</button></div><p class="footer-note">Historias e ilustraciones de demostración. Las historias que tú agregues se guardan en este navegador; puedes exportarlas desde «Agregar».</p></div><div class="footer-bottom shell"><span>© Umbral Comics · Proyecto de práctica</span><span>Hecho para explorar historias ✦</span></div></footer>
<dialog class="story-dialog" id="storyDialog" aria-labelledby="dialogTitle"><button type="button" class="dialog-close" data-close aria-label="Cerrar ficha">×</button><div class="dialog-layout"><img data-dialog-cover src="assets/cover-1.webp" alt=""><div class="dialog-copy"><p class="eyebrow" data-dialog-genre></p><h2 id="dialogTitle" data-dialog-title></h2><p data-dialog-description></p><p class="dialog-episodes" data-dialog-episodes></p><a class="external-story-link" data-dialog-link href="#" target="_blank" rel="noopener noreferrer" hidden>Leer en el sitio original ↗</a><button type="button" class="primary-button" data-read-sample>Leer muestra</button><div class="sample" data-sample hidden><h3>Un primer vistazo</h3><p data-sample-text></p><p data-demo-note>Esta es una muestra original del proyecto. La historia completa aún no está publicada.</p></div></div></div></dialog>
<dialog class="add-dialog" id="addStoryDialog" aria-labelledby="addStoryTitle"><div class="add-dialog-head"><div><p class="eyebrow">TU COLECCIÓN PERSONAL</p><h2 id="addStoryTitle">Agregar una historia</h2><p>Las historias se guardan en este navegador. Exporta un archivo para conservarlas o llevarlas a otro dispositivo.</p></div><button type="button" class="dialog-close" data-close-add aria-label="Cerrar formulario">×</button></div><form id="addStoryForm"><div class="form-grid"><label>Título <input name="title" maxlength="80" required placeholder="Ej. Mi manga favorito"></label><label>Autor o creador <input name="author" maxlength="80" placeholder="Nombre del creador"></label><label>Formato <select name="format"><option>Webtoon</option><option>Manga</option><option>Cómic</option><option>Novela gráfica</option><option>Historia</option></select></label><label>Género <select name="genre"><option>Fantasía</option><option>Acción</option><option>Romance</option><option>Misterio</option><option>Aventura</option><option>Comedia</option><option>Ciencia ficción</option><option>Drama</option><option>Terror</option></select></label><label class="full-field">Sinopsis <textarea name="description" maxlength="350" rows="3" required placeholder="¿De qué trata esta historia?"></textarea></label><label>Episodios o capítulos <input name="episodes" type="number" min="0" max="9999" value="1" required></label><label>Enlace para leer <input name="url" type="url" placeholder="https://..."></label><label class="full-field">Portada desde tu dispositivo <input name="coverFile" type="file" accept="image/png,image/jpeg,image/webp,image/avif"></label><label class="full-field">O enlace de portada <input name="coverUrl" type="url" placeholder="https://.../portada.jpg"></label><label class="full-field">Fragmento de muestra (opcional) <textarea name="sample" maxlength="1600" rows="3" placeholder="Un párrafo para mostrar al abrir la ficha"></textarea></label></div><p class="form-error" data-form-error role="status" aria-live="polite"></p><div class="form-actions"><button type="button" class="secondary-button" data-close-add>Cancelar</button><button type="submit" class="primary-button">Guardar historia</button></div></form><div class="collection-actions"><div><strong>Respaldo de mis historias</strong><p>Exporta tus historias o importa un archivo creado aquí.</p></div><div><button type="button" data-export>Exportar JSON</button><label class="import-label">Importar JSON <input type="file" data-import accept="application/json,.json"></label></div></div></dialog>''')


def index():
    cards = ''.join(f'''<a class="phase-card {'final-card' if i==12 else ''}" href="v{i:02}.html"><span class="card-num">{i:02}</span><span class="phase-title">{escape(title)}</span><span class="phase-desc">{escape(desc)}</span><span class="card-go">Abrir fase <span aria-hidden="true">↗</span></span></a>''' for i,(title,desc) in enumerate(PHASES,1))
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Doce versiones de una página de cómics, de HTML puro a una experiencia interactiva."><title>Umbral Comics · 12 fases</title><link rel="stylesheet" href="styles/index.css"></head><body><header class="site-header"><a href="index.html" class="brand">✦ UMBRAL <span>COMICS</span></a><a href="v12.html" class="header-link">Ir a la versión final <span>↗</span></a></header><main><section class="intro"><div class="intro-copy"><p class="eyebrow">PROYECTO PASO A PASO / 01—12</p><h1>De HTML puro a un <em>universo de cómics.</em></h1><p>Abre cada fase para ver cómo crece la misma página: estructura, imágenes, diseño, funciones y una entrada en forma de portal.</p><div class="intro-actions"><a class="primary" href="v01.html">Empezar en la fase 01</a><a class="secondary" href="v12.html">Ver resultado final</a></div></div><div class="intro-art" role="img" aria-label="Portal fantástico sobre la ciudad"><span>12 FASES<br>UNA HISTORIA</span></div></section><section class="journey"><div class="journey-heading"><div><p class="eyebrow">RECORRIDO DE CONSTRUCCIÓN</p><h2>Explora la evolución</h2></div><p>Cada tarjeta abre un archivo HTML independiente. Puedes avanzar con los enlaces de fase anterior y siguiente.</p></div><div class="phase-grid">{cards}</div></section><section class="about"><div><p class="eyebrow">HECHO PARA APRENDER</p><h2>El proyecto completo también incluye el código de cada etapa.</h2></div><p>Las hojas de estilo están separadas por fase y se acumulan gradualmente. Las historias y las ilustraciones son de demostración.</p></section></main><footer><span>✦ UMBRAL COMICS</span><span>Proyecto visual · 12 fases</span></footer></body></html>'''


def main():
    OUT.mkdir(exist_ok=True)
    for n in range(1,13):
        (OUT / f"v{n:02}.html").write_text(basic(n) if n <= 2 else final_page() if n == 12 else rich(n), encoding="utf-8")
    (OUT / "index.html").write_text(index(), encoding="utf-8")
    print("Generated index.html and v01.html–v12.html")


if __name__ == "__main__":
    main()
