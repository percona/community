// This file helps work around an iOS/Safari bug for screen readers that reads the underlying text
// even if the overlay is open.
(function () {
    const mobile_menu_toggle = document.getElementById("show-mobile-menu");
    const mobile_menu = document.getElementById("mobile-menu");
    const hamburger = document.getElementById("hamburger");

    if (!mobile_menu_toggle || !mobile_menu) {
        return;
    }

    function syncMobileMenuState(isOpen) {
        document.body.classList.toggle("is-mobile-menu-open", isOpen);
        mobile_menu.setAttribute("aria-modal", isOpen ? "true" : "false");
        mobile_menu.setAttribute("aria-hidden", isOpen ? "false" : "true");

        if (hamburger) {
            hamburger.setAttribute("aria-hidden", isOpen ? "true" : "false");
        }
    }

    mobile_menu_toggle.addEventListener("change", function () {
        syncMobileMenuState(this.checked);
    });

    mobile_menu.addEventListener("click", function (event) {
        if (event.target === mobile_menu) {
            mobile_menu_toggle.checked = false;
            syncMobileMenuState(false);
        }
    });

    syncMobileMenuState(mobile_menu_toggle.checked);

    document.querySelectorAll(".menu__toggle").forEach(function (btn) {
        if (btn.getAttribute("aria-expanded") === "true") {
            btn.classList.add("is-open");
        }

        btn.addEventListener("click", function () {
            var panel = document.getElementById(btn.getAttribute("aria-controls"));
            if (!panel) return;
            var isOpen = btn.getAttribute("aria-expanded") === "true";
            btn.setAttribute("aria-expanded", isOpen ? "false" : "true");
            panel.hidden = isOpen;
            btn.classList.toggle("is-open", !isOpen);
        });
    });
})();
