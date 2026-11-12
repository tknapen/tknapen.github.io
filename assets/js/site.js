/* Knapen Lab: color scheme switch, menu toggle, publication filters, home figure carousel, keyboard access to wide code blocks. No dependencies. */
(function () {
  'use strict';

  /* ---- Color scheme switch ----
     Automatic follows the system setting; Light and Dark set data-theme on <html> (read early by the script in
     head.html). The choice is stored in localStorage when storage is available, otherwise it lasts for this page. */
  var SCHEME_KEY = 'color-scheme';
  var systemDark = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  /* The first click always changes what the visitor sees: automatic -> the opposite of the system setting ->
     the system's own scheme -> automatic. */
  function nextScheme(m) {
    var sys = systemDark && systemDark.matches ? 'dark' : 'light';
    var other = sys === 'dark' ? 'light' : 'dark';
    return m === 'auto' ? other : (m === other ? sys : 'auto');
  }
  var SCHEME_NAME = { auto: 'automatic, follows your system', light: 'light', dark: 'dark' };
  var SCHEME_BG = { light: '#ffffff', dark: '#121316' };

  function storedScheme() {
    try {
      var v = window.localStorage.getItem(SCHEME_KEY);
      return v === 'light' || v === 'dark' ? v : 'auto';
    } catch (e) {
      return null;
    }
  }

  function storeScheme(mode) {
    try {
      if (mode === 'auto') window.localStorage.removeItem(SCHEME_KEY);
      else window.localStorage.setItem(SCHEME_KEY, mode);
    } catch (e) { /* storage blocked: the choice applies to this page only */ }
  }

  function initScheme() {
    var button = document.querySelector('.theme-toggle');
    if (!button) return;
    var root = document.documentElement;
    var status = document.getElementById('theme-status');
    var metas = Array.prototype.slice.call(document.querySelectorAll('meta[name="theme-color"]'));
    var metaDefaults = metas.map(function (m) { return m.getAttribute('content'); });
    var initial = root.getAttribute('data-theme');
    var mode = initial === 'light' || initial === 'dark' ? initial : 'auto';

    function apply(announce) {
      if (mode === 'auto') root.removeAttribute('data-theme');
      else root.setAttribute('data-theme', mode);
      root.style.colorScheme = mode === 'auto' ? '' : mode;
      // The browser bar follows the chosen scheme; in automatic mode the media queries on the metas decide.
      metas.forEach(function (m, i) {
        m.setAttribute('content', mode === 'auto' ? metaDefaults[i] : SCHEME_BG[mode]);
      });
      button.setAttribute('aria-label', 'Color scheme: ' + SCHEME_NAME[mode] + '. Switch to ' + SCHEME_NAME[nextScheme(mode)].replace(/,.*/, ''));
      if (announce && status) status.textContent = 'Color scheme: ' + SCHEME_NAME[mode] + '.';
    }

    button.addEventListener('click', function () {
      mode = nextScheme(mode);
      storeScheme(mode);
      apply(true);
    });

    // A choice made in another tab applies here too.
    window.addEventListener('storage', function (e) {
      if (e.key !== SCHEME_KEY && e.key !== null) return;
      var s = storedScheme();
      if (s && s !== mode) { mode = s; apply(false); }
    });

    // The label names the next scheme, which depends on the system setting.
    var onSystemChange = function () { apply(false); };
    if (systemDark) {
      if (systemDark.addEventListener) systemDark.addEventListener('change', onSystemChange);
      else if (systemDark.addListener) systemDark.addListener(onSystemChange);
    }

    apply(false);
  }

  /* ---- Mobile menu ---- */
  function initMenu() {
    var button = document.querySelector('.nav-toggle');
    var nav = document.getElementById('site-nav');
    if (!button || !nav) return;

    function setOpen(open) {
      button.setAttribute('aria-expanded', open ? 'true' : 'false');
      nav.classList.toggle('is-open', open);
    }

    button.addEventListener('click', function () {
      setOpen(button.getAttribute('aria-expanded') !== 'true');
    });

    // Escape closes the menu; focus returns to the button only if it was in the menu.
    document.addEventListener('keydown', function (e) {
      if ((e.key === 'Escape' || e.key === 'Esc') && button.getAttribute('aria-expanded') === 'true') {
        var active = document.activeElement;
        var inMenu = active === button || nav.contains(active);
        setOpen(false);
        if (inMenu) button.focus();
      }
    });

    // Close the menu when the layout switches to the desktop navigation.
    if (window.matchMedia) {
      var wide = window.matchMedia('(min-width: 900px)');
      var onChange = function (e) { if (e.matches) setOpen(false); };
      if (wide.addEventListener) wide.addEventListener('change', onChange);
      else if (wide.addListener) wide.addListener(onChange);
    }
  }

  /* ---- Publication filters ---- */
  function initFilters() {
    var panel = document.getElementById('pub-filters');
    if (!panel) return;

    var buttons = Array.prototype.slice.call(panel.querySelectorAll('.filter-btn'));
    var input = document.getElementById('pub-search');
    var status = document.getElementById('pub-status');
    var empty = document.getElementById('pub-empty');
    var entries = Array.prototype.slice.call(document.querySelectorAll('.pub-years .pub'));
    var years = Array.prototype.slice.call(document.querySelectorAll('.pub-years .pub-year'));
    var total = entries.length;
    var current = 'all';
    var timer = null;
    var touched = false;  // announce "all" only after the visitor has changed something

    // Cache searchable text once: title, authors, journal and links, but not the theme labels
    // (the theme buttons filter by theme; matching their names in search would inflate results).
    var texts = entries.map(function (li) {
      var copy = li.cloneNode(true);
      Array.prototype.forEach.call(copy.querySelectorAll('.pub-themes'), function (n) { n.parentNode.removeChild(n); });
      return normalize(copy.textContent);
    });

    function normalize(s) {
      s = (s || '').toLowerCase();
      if (s.normalize) s = s.normalize('NFD').replace(/[̀-ͯ]/g, '');
      return s.replace(/\s+/g, ' ');
    }

    function matchesFilter(li) {
      if (current === 'all') return true;
      if (current === 'selected') return li.getAttribute('data-selected') === 'true';
      if (current.indexOf('theme:') === 0) {
        var themes = ' ' + (li.getAttribute('data-themes') || '') + ' ';
        return themes.indexOf(' ' + current.slice(6) + ' ') !== -1;
      }
      if (current.indexOf('type:') === 0) return li.getAttribute('data-type') === current.slice(5);
      return true;
    }

    function apply() {
      var terms = normalize(input ? input.value : '').trim().split(' ').filter(Boolean);
      var shown = 0;
      entries.forEach(function (li, i) {
        var ok = matchesFilter(li);
        for (var t = 0; ok && t < terms.length; t++) {
          if (texts[i].indexOf(terms[t]) === -1) ok = false;
        }
        li.hidden = !ok;
        if (ok) shown++;
      });
      years.forEach(function (sec) {
        sec.hidden = !sec.querySelector('.pub:not([hidden])');
      });
      if (empty) empty.hidden = shown !== 0;
      if (status) {
        if (current === 'all' && terms.length === 0) {
          status.textContent = touched ? 'Showing all ' + total + ' publications.' : '';
        } else {
          status.textContent = 'Showing ' + shown + ' of ' + total + ' publications.';
        }
      }
    }

    function select(filter, updateHash) {
      var found = false;
      buttons.forEach(function (b) {
        var on = b.getAttribute('data-filter') === filter;
        if (on) found = true;
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });
      if (!found) return select('all', updateHash);
      current = filter;
      apply();
      if (updateHash && window.history && history.replaceState) {
        var hash = filter === 'all' ? '' : '#' + filter.replace(/^(theme|type):/, '');
        history.replaceState(null, '', location.pathname + location.search + hash);
      }
    }

    buttons.forEach(function (b) {
      b.addEventListener('click', function () { touched = true; select(b.getAttribute('data-filter'), true); });
    });

    if (input) {
      input.addEventListener('input', function () {
        touched = true;
        clearTimeout(timer);
        timer = setTimeout(apply, 120);
      });
    }

    // A hash such as #topographic-maps, #selected or #preprint preselects a filter.
    function fromHash() {
      var h = decodeURIComponent((location.hash || '').slice(1));
      if (!h) return 'all';
      if (h === 'selected' || h === 'all') return h;
      if (h === 'preprint' || h === 'preprints') return 'type:preprint';
      return 'theme:' + h;
    }

    panel.hidden = false;
    select(fromHash(), false);
  }

  /* ---- Home figure carousel (WAI-ARIA APG carousel pattern) ----
     Rotation stops while the pointer is over the carousel, while focus is inside it and while the tab is hidden.
     Pressing the pause button or any other control stops it until the visitor presses play.
     With prefers-reduced-motion, it starts stopped (and CSS drops the fade). */
  function initCarousel() {
    var root = document.querySelector('.hero-carousel');
    if (!root) return;
    var slides = Array.prototype.slice.call(root.querySelectorAll('.hero-slide'));
    var controls = root.querySelector('.hero-controls');
    if (slides.length < 2 || !controls) return;

    var live = root.querySelector('.hero-slides');
    var rotate = root.querySelector('.hero-rotate');
    var prev = root.querySelector('.hero-prev');
    var next = root.querySelector('.hero-next');
    var dots = Array.prototype.slice.call(root.querySelectorAll('.hero-dot'));
    var interval = parseInt(root.getAttribute('data-interval'), 10) || 7000;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var current = 0;
    var stopped = reduce;   // stopped by the visitor (or by reduced motion) until play is pressed
    var hovered = false;
    var focused = false;
    var timer = null;

    function show(i) {
      current = (i + slides.length) % slides.length;
      slides.forEach(function (s, k) {
        var on = k === current;
        s.classList.toggle('is-active', on);
        // Hide inactive slides from assistive technology; they stay rendered for the crossfade.
        if (on) s.removeAttribute('aria-hidden'); else s.setAttribute('aria-hidden', 'true');
      });
      dots.forEach(function (d, k) {
        if (k === current) d.setAttribute('aria-current', 'true'); else d.removeAttribute('aria-current');
      });
    }

    function running() {
      return !stopped && !hovered && !focused && !document.hidden;
    }

    function update() {
      clearTimeout(timer);
      timer = null;
      var on = running();
      if (on) {
        timer = setTimeout(function () { show(current + 1); update(); }, interval);
      }
      // Announce slide changes only when they are not automatic.
      live.setAttribute('aria-live', on ? 'off' : 'polite');
      rotate.classList.toggle('is-stopped', stopped);
      rotate.setAttribute('aria-label', stopped ? 'Start automatic slide show' : 'Stop automatic slide show');
    }

    function stop() { stopped = true; update(); }

    rotate.addEventListener('click', function () {
      stopped = !stopped;
      // Pressing play starts rotation at once, even with focus or the pointer still on the button.
      if (!stopped) { focused = false; hovered = false; }
      update();
    });
    prev.addEventListener('click', function () { show(current - 1); stop(); });
    next.addEventListener('click', function () { show(current + 1); stop(); });
    dots.forEach(function (d, k) {
      d.addEventListener('click', function () { show(k); stop(); });
    });

    // Hover pauses for mouse and pen; a tap on a touch screen should not leave the carousel paused.
    root.addEventListener('pointerenter', function (e) { if (e.pointerType !== 'touch') { hovered = true; update(); } });
    root.addEventListener('pointerleave', function () { if (hovered) { hovered = false; update(); } });
    root.addEventListener('focusin', function () { focused = true; update(); });
    root.addEventListener('focusout', function (e) {
      if (!root.contains(e.relatedTarget)) { focused = false; update(); }
    });
    document.addEventListener('visibilitychange', update);

    slides.forEach(function (s) { s.hidden = false; });
    controls.hidden = false;
    root.classList.add('is-enhanced');
    show(0);
    update();
  }

  /* ---- Code blocks that scroll sideways must be reachable by keyboard ---- */
  function initScrollables() {
    var blocks = Array.prototype.slice.call(document.querySelectorAll('pre'));
    if (!blocks.length) return;
    function update() {
      blocks.forEach(function (pre) {
        if (pre.scrollWidth > pre.clientWidth + 1) pre.setAttribute('tabindex', '0');
        else pre.removeAttribute('tabindex');
      });
    }
    update();
    var t = null;
    window.addEventListener('resize', function () {
      clearTimeout(t);
      t = setTimeout(update, 200);
    });
  }

  function init() {
    initScheme();
    initMenu();
    initFilters();
    initCarousel();
    initScrollables();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
