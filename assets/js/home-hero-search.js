(function () {
  var heroInput = document.getElementById('community-search-hero-input');
  var heroButton = document.getElementById('community-search-hero-button');
  var overlayInput = document.getElementById('community-search-input');
  var overlayToggle = document.getElementById('community-search-toggle');
  var overlayButton = document.getElementById('community-search-button');

  function openOverlay() {
    if (!overlayToggle) return;
    overlayToggle.click();
    window.setTimeout(function () {
      if (!heroInput || !overlayInput || overlayInput.disabled) return;
      overlayInput.value = heroInput.value;
      overlayInput.focus();
    }, 50);
  }

  if (heroInput) {
    heroInput.addEventListener('focus', openOverlay);
    heroInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        if (overlayInput) overlayInput.value = heroInput.value;
        if (overlayButton) overlayButton.click();
        else openOverlay();
      }
    });
  }

  if (heroButton) {
    heroButton.addEventListener('click', function () {
      if (overlayInput && heroInput) overlayInput.value = heroInput.value;
      if (overlayButton) overlayButton.click();
      else openOverlay();
    });
  }
})();
