// This file helps work around an iOS/Safari bug for screen readers that reads the underlying text
// even if the overlay is open.
(function () {
    const mobile_menu_toggle = document.getElementById("show-mobile-menu");
    const mobile_menu = document.getElementById("mobile-menu")
    const hamburger = document.getElementById("hamburger")
    mobile_menu_toggle.addEventListener( 'change', function() {
        if(this.checked) {
            mobile_menu.setAttribute("aria-modal", "true");
            mobile_menu.setAttribute("aria-hidden", "false");
            hamburger.setAttribute("aria-hidden", "true");
        } else {
            mobile_menu.setAttribute("aria-modal", "false");
            mobile_menu.setAttribute("aria-hidden", "true");
            hamburger.setAttribute("aria-hidden", "false");
        }
    });
})();