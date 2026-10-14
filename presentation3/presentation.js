(() => {
  'use strict';
  const slides = [...document.querySelectorAll('.slide')];
  const previous = document.getElementById('previous-button');
  const next = document.getElementById('next-button');
  const counter = document.getElementById('slide-counter');
  const progress = document.getElementById('progress');
  const overview = document.getElementById('overview-button');
  const dialog = document.getElementById('sources-dialog');
  let index = 0;
  let overviewMode = false;
  let touchStart = null;

  const dots = slides.map((slide, i) => {
    const dot = document.createElement('button');
    dot.setAttribute('aria-label', `Slide ${i + 1}: ${slide.querySelector('h1,h2').textContent}`);
    dot.addEventListener('click', () => go(i));
    progress.append(dot);
    return dot;
  });

  function render() {
    slides.forEach((slide, i) => {
      const active = i === index;
      slide.classList.toggle('active', active);
      slide.inert = !overviewMode && !active;
      dots[i].setAttribute('aria-current', String(active));
    });
    previous.disabled = index === 0;
    next.disabled = index === slides.length - 1;
    counter.textContent = `${String(index + 1).padStart(2, '0')} / ${String(slides.length).padStart(2, '0')}`;
  }

  function go(i) {
    index = Math.max(0, Math.min(slides.length - 1, i));
    const hash = `#${slides[index].id}`;
    if (location.hash !== hash) history.replaceState(null, '', hash);
    render();
    if (overviewMode) slides[index].scrollIntoView({block: 'start'});
    else window.scrollTo(0, 0);
  }

  function readHash() {
    const found = slides.findIndex(slide => `#${slide.id}` === location.hash);
    go(found < 0 ? 0 : found);
  }

  previous.addEventListener('click', () => go(index - 1));
  next.addEventListener('click', () => go(index + 1));
  window.addEventListener('hashchange', readHash);
  overview.addEventListener('click', () => {
    overviewMode = !overviewMode;
    document.body.classList.toggle('overview', overviewMode);
    overview.setAttribute('aria-pressed', String(overviewMode));
    overview.textContent = overviewMode ? 'Single slide' : 'All slides';
    go(index);
  });
  document.getElementById('print-button').addEventListener('click', () => window.print());
  document.getElementById('sources-button').addEventListener('click', () => dialog.showModal());
  document.querySelectorAll('[data-open-sources]').forEach(button => button.addEventListener('click', () => dialog.showModal()));
  document.getElementById('close-sources').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target === dialog) {
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    }
  });
  document.addEventListener('keydown', async event => {
    if (dialog.open || event.altKey || event.ctrlKey || event.metaKey || /INPUT|TEXTAREA|SELECT/.test(event.target.tagName) || event.target.isContentEditable) return;
    if (event.key === 'ArrowRight' || event.key === 'PageDown') { event.preventDefault(); go(index + 1); }
    if (event.key === 'ArrowLeft' || event.key === 'PageUp') { event.preventDefault(); go(index - 1); }
    if (event.key === 'Home') { event.preventDefault(); go(0); }
    if (event.key === 'End') { event.preventDefault(); go(slides.length - 1); }
    if (event.key.toLowerCase() === 'f') {
      try {
        if (document.fullscreenElement) await document.exitFullscreen();
        else await document.documentElement.requestFullscreen();
      } catch { /* Fullscreen may be unavailable in an embedded preview. */ }
    }
  });
  document.getElementById('deck').addEventListener('touchstart', event => {
    if (event.touches.length === 1) touchStart = {x: event.touches[0].clientX, y: event.touches[0].clientY};
    else touchStart = null;
  }, {passive: true});
  document.getElementById('deck').addEventListener('touchend', event => {
    if (!touchStart || overviewMode || dialog.open) return;
    const touch = event.changedTouches[0];
    const dx = touch.clientX - touchStart.x;
    const dy = touch.clientY - touchStart.y;
    touchStart = null;
    if (Math.abs(dx) > 70 && Math.abs(dx) > Math.abs(dy) * 1.5) go(index + (dx < 0 ? 1 : -1));
  }, {passive: true});

  document.documentElement.classList.add('js');
  readHash();
  window.addEventListener('beforeprint', () => slides.forEach(slide => { slide.inert = false; }));
  window.addEventListener('afterprint', render);
})();
