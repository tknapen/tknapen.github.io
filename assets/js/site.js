/* Knapen Lab: menu toggle and publication filters. No dependencies. */
(function () {
  'use strict';

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

    document.addEventListener('keydown', function (e) {
      if ((e.key === 'Escape' || e.key === 'Esc') && button.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        button.focus();
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

    // Cache searchable text once.
    var texts = entries.map(function (li) {
      return normalize(li.textContent);
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
        status.textContent = (current === 'all' && terms.length === 0)
          ? ''
          : 'Showing ' + shown + ' of ' + total + ' publications.';
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
      b.addEventListener('click', function () { select(b.getAttribute('data-filter'), true); });
    });

    if (input) {
      input.addEventListener('input', function () {
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

  function init() {
    initMenu();
    initFilters();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
