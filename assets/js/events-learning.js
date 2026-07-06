(function () {
  // ── Custom filter dropdowns ──────────────────────────────────────────
  var filterBtns = document.querySelectorAll('[data-el-dropdown]');

  function closeAllDropdowns(except) {
    filterBtns.forEach(function (btn) {
      if (btn === except) return;
      var panelId = 'el-dropdown-' + btn.dataset.elDropdown;
      var panel = document.getElementById(panelId);
      btn.setAttribute('aria-expanded', 'false');
      if (panel) panel.hidden = true;
    });
  }

  filterBtns.forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var panelId = 'el-dropdown-' + btn.dataset.elDropdown;
      var panel = document.getElementById(panelId);
      var isOpen = btn.getAttribute('aria-expanded') === 'true';
      closeAllDropdowns(null);
      if (!isOpen) {
        btn.setAttribute('aria-expanded', 'true');
        if (panel) panel.hidden = false;
      }
    });
  });

  document.addEventListener('click', function () {
    closeAllDropdowns(null);
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeAllDropdowns(null);
  });

})();

(function () {
  document.querySelectorAll('.hub-page').forEach(function (root) {
  var tabs = Array.prototype.slice.call(root.querySelectorAll('[data-el-tab]'));
  var panels = Array.prototype.slice.call(root.querySelectorAll('[data-el-panel]'));
  if (!tabs.length || !panels.length) return;

  var mobileQuery = window.matchMedia('(max-width: 900px)');
  var activeId = null;
  var scrollOffset = 120;

  function setActive(id) {
    if (!id || id === activeId) return;
    activeId = id;

    tabs.forEach(function (tab) {
      var isActive = tab.dataset.elTab === id;
      tab.classList.toggle('is-active', isActive);
      if (isActive) {
        tab.setAttribute('aria-current', 'true');
      } else {
        tab.removeAttribute('aria-current');
      }
    });
  }

  function measureScrollOffset() {
    var style = window.getComputedStyle(panels[0]);
    var margin = parseFloat(style.scrollMarginTop);
    scrollOffset = Number.isFinite(margin) && margin > 0 ? margin : 120;
  }

  function scrollToPanel(id, behavior) {
    var target = document.getElementById('el-panel-' + id);
    if (!target) return;

    measureScrollOffset();
    var targetTop = target.getBoundingClientRect().top + window.pageYOffset - scrollOffset;
    var maxScroll = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);

    window.scrollTo({
      top: Math.min(Math.max(0, targetTop), maxScroll),
      behavior: behavior || 'smooth'
    });
    setActive(id);
  }

  function updateActiveFromScroll() {
    var offset = scrollOffset;
    var maxScroll = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
    var i;
    var rect;

    if (window.scrollY >= maxScroll - 2) {
      setActive(panels[panels.length - 1].dataset.elPanel);
      return;
    }

    for (i = panels.length - 1; i >= 0; i--) {
      rect = panels[i].getBoundingClientRect();
      if (rect.top <= offset) {
        setActive(panels[i].dataset.elPanel);
        return;
      }
    }

    setActive(panels[0].dataset.elPanel);
  }

  tabs.forEach(function (tab) {
    tab.addEventListener('click', function (e) {
      e.preventDefault();
      var id = tab.dataset.elTab;

      if (mobileQuery.matches) {
        tab.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }

      scrollToPanel(id, 'smooth');
    });
  });

  function syncFromHash() {
    var hash = window.location.hash;
    if (!hash || hash.indexOf('#el-panel-') !== 0) return;
    scrollToPanel(hash.slice('#el-panel-'.length), 'auto');
  }

  var ticking = false;

  function onScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      updateActiveFromScroll();
    });
  }

  measureScrollOffset();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', function () {
    measureScrollOffset();
    onScroll();
  }, { passive: true });
  window.addEventListener('hashchange', syncFromHash);

  if (window.location.hash) {
    syncFromHash();
  } else {
    updateActiveFromScroll();
  }

  root.querySelectorAll('.el-speaker-card__img[src]').forEach(function (img) {
    function markLoaded() {
      img.classList.add('is-loaded');
    }

    if (img.complete && img.naturalWidth > 0) {
      markLoaded();
    } else {
      img.addEventListener('load', markLoaded, { once: true });
      img.addEventListener('error', markLoaded, { once: true });
    }
  });
  });
})();
