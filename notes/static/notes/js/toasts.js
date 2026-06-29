(function () {
    const AUTO_DISMISS_MS = 5000;

    function dismiss(toast) {
        if (toast.dataset.leaving) return;
        toast.dataset.leaving = "1";
        toast.classList.add("is-leaving");
        toast.classList.remove("is-visible");
        toast.addEventListener("transitionend", () => toast.remove(), { once: true });
        setTimeout(() => toast.remove(), 500);
    }

    function activate(toast) {
        requestAnimationFrame(() => toast.classList.add("is-visible"));

        toast.querySelector(".toast__close")?.addEventListener("click", () => dismiss(toast));

        let timer = setTimeout(() => dismiss(toast), AUTO_DISMISS_MS);
        toast.addEventListener("mouseenter", () => clearTimeout(timer));
        toast.addEventListener("mouseleave", () => {
            timer = setTimeout(() => dismiss(toast), AUTO_DISMISS_MS);
        });
    }

    function init(root) {
        root.querySelectorAll(".toast:not([data-init])").forEach((toast) => {
            toast.dataset.init = "1";
            activate(toast);
        });
    }

    document.addEventListener("DOMContentLoaded", () => init(document));
})();
